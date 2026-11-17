"""Intermittent demand: forecasting methods scored on stock for a target fill rate - Chmltech Online Journal.
One population of 1,000 simulated items (the paper averages five). Python 3 with NumPy; runs in about a minute."""
import numpy as np

L, PROT, WARM, EVAL, A, B, N = 4, 5, 52, 104, 0.1, 0.05, 13   # lead time, lead+review, history, scored weeks, alpha, beta, MA window


def items(seed, n=1000):
    r = np.random.default_rng(seed)
    return [dict(p=1 / np.exp(r.uniform(0, np.log(4))), cv=r.uniform(.2, 1.3), mu=np.exp(r.uniform(np.log(2), np.log(60))))
            for _ in range(n)]


def demand(it, r, weeks=WARM + EVAL):
    s2 = np.log(1 + it['cv'] ** 2)
    occurs = r.random(weeks) < it['p']
    return occurs * np.maximum(1, np.round(r.lognormal(np.log(it['mu']) - s2 / 2, np.sqrt(s2), weeks)))


def forecast(d, method):
    """One-week-ahead forecast available at the start of each week."""
    out = np.zeros(len(d)); nz = d[:N][d[:N] > 0]
    f = d[:N].mean(); z = nz.mean() if len(nz) else 1.0; p = N / max(1, len(nz)); q = 1; pr = max(len(nz) / N, 1 / N)
    for t in range(len(d)):
        if method == 'MA':        out[t] = d[max(0, t - N):t].mean() if t else 0.0
        elif method == 'SES':     out[t] = f; f += A * (d[t] - f)
        elif method in ('Croston', 'SBA'):
            out[t] = z / p * ((1 - A / 2) if method == 'SBA' else 1)
            if d[t] > 0: z += A * (d[t] - z); p += A * (q - p); q = 1
            else: q += 1
        elif method == 'TSB':
            out[t] = pr * z
            if d[t] > 0: pr += B * (1 - pr); z += A * (d[t] - z)
            else: pr -= B * pr
    return out


def levels(d, method, k):
    """Order-up-to level by week: PROT x forecast + k x sigma, or the k-th quantile of bootstrapped demand."""
    if method == 'Bootstrap':
        r = np.random.default_rng(12345); S = np.zeros(len(d))
        for t in range(WARM, len(d)):
            if t == WARM or t % 4 == 0:
                lvl = np.quantile(d[:t][r.integers(0, t, size=(400, PROT))].sum(axis=1), k)
            S[t] = lvl
        return S
    f = forecast(d, method); mse = d[:N].var() + 1e-9; S = np.zeros(len(d))
    for t in range(len(d)):
        S[t] = PROT * f[t] + k * np.sqrt(mse * PROT)
        mse += A * ((d[t] - f[t]) ** 2 - mse)
    return S


def run_policy(d, S):
    """Weekly review, order up to S, lead time L, backorders. Returns units demanded, units filled, average on hand."""
    pipe = np.zeros(len(d) + L + 1); oh = max(S[WARM], 0.0); back = dem = fill = ohs = 0.0
    for t in range(WARM, len(d)):
        oh += pipe[t]; c = min(back, oh); oh -= c; back -= c
        pipe[t + L] += max(0.0, S[t] - (oh - back + pipe[t + 1:t + L].sum()))
        served = min(d[t], oh); oh -= served; back += d[t] - served
        dem += d[t]; fill += served; ohs += oh
    return dem, fill, ohs / EVAL


r = np.random.default_rng(111); D = [demand(it, r) for it in items(11)]
weekly = sum(d[WARM:].mean() for d in D)
grid = {'Bootstrap': [.5, .6, .7, .8, .85, .9, .93, .95, .96, .97, .98, .99, .995]}
for m in ['MA', 'SES', 'Croston', 'SBA', 'TSB', 'Bootstrap']:
    pts = []
    for k in grid.get(m, [0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 3, 3.5, 4]):
        tot = np.sum([run_policy(d, levels(d, m, k)) for d in D], axis=0)
        pts.append((tot[1] / tot[0] * 100, tot[2] / weekly))
    (f0, w0), (f1, w1) = next((a, b) for a, b in zip(pts, pts[1:]) if a[0] < 95 <= b[0])
    print(f"{m:10s} weeks of stock for 95% fill: {w0 + (95 - f0) / (f1 - f0) * (w1 - w0):5.2f}")
