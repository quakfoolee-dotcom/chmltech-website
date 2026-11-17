"""Intermittent demand forecasting scored on inventory outcomes. V2.

V2: adds long-history benchmarks (normal formula and bootstrap on the full history or the last 52/26 weeks)
and TSB with probability smoothing 0.10 and 0.20.

Simulated SKU population (weekly demand), six forecasting methods, periodic-review order-up-to policy.
Each method sets its order-up-to level from its own forecast; the safety factor is swept to trace
fill rate against average stock, so methods are compared at equal service.
"""
import numpy as np

L, R = 4, 1                      # lead time (weeks), review period (weeks)
PROT = L + R                     # protection period
WARM, EVAL = 52, 104             # weeks of history before evaluation; evaluated weeks
ALPHA = 0.1                      # smoothing constant for SES-type methods (ERP-typical)
BETA = 0.05                      # TSB probability smoothing
MA_N = 13                        # moving average window (one quarter)


def make_items(seed, n=1000):
    """Each item: demand occurs with probability p per week; size lognormal with mean mu and CV cv.
    Parameters spread across the four Syntetos-Boylan-Croston classes."""
    r = np.random.default_rng(seed)
    items = []
    for i in range(n):
        adi = np.exp(r.uniform(np.log(1.0), np.log(4.0)))     # average inter-demand interval, weeks
        p = min(1.0, 1 / adi)
        cv = r.uniform(0.2, 1.3)                              # CV of non-zero demand sizes
        mu = np.exp(r.uniform(np.log(2), np.log(60)))          # mean size when demand occurs
        items.append(dict(p=p, cv=cv, mu=mu))
    return items


def demand_series(item, r, weeks, stop=None, shift=None):
    """shift = (week, factor): from that week the chance of demand is multiplied by factor."""
    s2 = np.log(1 + item['cv'] ** 2)
    p = np.full(weeks, item['p'])
    if shift is not None:
        p[shift[0]:] = np.minimum(1.0, p[shift[0]:] * shift[1])
    occ = r.random(weeks) < p
    size = np.maximum(1, np.round(r.lognormal(np.log(item['mu']) - s2 / 2, np.sqrt(s2), weeks)))
    d = occ * size
    if stop is not None:
        d[stop:] = 0
    return d.astype(float)


def classify(hist):
    nz = hist[hist > 0]
    if len(nz) < 2:
        return 'lumpy'
    adi = len(hist) / len(nz); cv2 = (nz.std() / nz.mean()) ** 2
    if adi < 1.32:
        return 'smooth' if cv2 < 0.49 else 'erratic'
    return 'intermittent' if cv2 < 0.49 else 'lumpy'


# ---------------- forecasting methods: return per-week forecast of mean demand for the NEXT week ----------------
def f_ma(d):
    out = np.zeros(len(d))
    for t in range(1, len(d)):
        out[t] = d[max(0, t - MA_N):t].mean()
    return out

def f_ses(d, a=ALPHA):
    out = np.zeros(len(d)); f = d[:MA_N].mean()
    for t in range(len(d)):
        out[t] = f; f = f + a * (d[t] - f)
    return out

def _croston(d, a=ALPHA, sba=False):
    out = np.zeros(len(d)); nz = np.flatnonzero(d[:MA_N] > 0)
    z = d[:MA_N][nz].mean() if len(nz) else 1.0
    pp = MA_N / max(1, len(nz)); q = 1
    for t in range(len(d)):
        fc = z / pp
        out[t] = fc * (1 - a / 2) if sba else fc
        if d[t] > 0:
            z = z + a * (d[t] - z); pp = pp + a * (q - pp); q = 1
        else:
            q += 1
    return out

def f_croston(d): return _croston(d)
def f_sba(d): return _croston(d, sba=True)

def f_tsb(d, a=ALPHA, b=BETA):
    out = np.zeros(len(d)); nz = d[:MA_N] > 0
    pr = max(nz.mean(), 1 / MA_N); z = d[:MA_N][nz].mean() if nz.any() else 1.0
    for t in range(len(d)):
        out[t] = pr * z
        if d[t] > 0:
            pr = pr + b * (1 - pr); z = z + a * (d[t] - z)
        else:
            pr = pr + b * (0 - pr)
    return out

FORECASTS = dict(ma=f_ma, ses=f_ses, croston=f_croston, sba=f_sba, tsb=f_tsb,
                 tsb10=lambda d: f_tsb(d, b=0.10), tsb20=lambda d: f_tsb(d, b=0.20))


def order_up_to_levels(d, method, k):
    """Order-up-to level S_t for each week t, set at the start of week t from data before t.
    Parametric methods: S = PROT * f + k * sigma * sqrt(PROT), sigma from smoothed MSE of one-week errors.
    Bootstrap: S = k-th quantile of PROT-week demand sums resampled from all history (k in (0,1))."""
    n = len(d); S = np.zeros(n)
    if method in ('normfull', 'norm52'):
        S = np.zeros(n); lvl = 0.0
        for t in range(WARM, n):
            if t % 4 == 0 or t == WARM:
                h = d[:t] if method == 'normfull' else d[max(0, t - 52):t]
                lvl = PROT * h.mean() + k * np.sqrt(PROT * h.var())
            S[t] = lvl
        return S
    if method in ('boot', 'boot52', 'boot26'):
        r = np.random.default_rng(12345)
        for t in range(WARM, n):
            if t % 4 == 0 or t == WARM:                      # refresh monthly
                h = d[:t] if method == 'boot' else d[max(0, t - (52 if method == 'boot52' else 26)):t]
                sims = h[r.integers(0, len(h), size=(400, PROT))].sum(axis=1)
                lvl = np.quantile(sims, k)
            S[t] = lvl
        return S
    base, sig = parametric_parts(d, method)
    return base + k * sig


def parametric_parts(d, method):
    """Mean protection-period demand PROT*f_t and its standard deviation sqrt(PROT*MSE_t), both known at week t."""
    f = FORECASTS[method](d); n = len(d)
    mse = np.var(d[:MA_N]) + 1e-9; sig = np.zeros(n)
    for t in range(n):
        sig[t] = np.sqrt(mse * PROT)
        e = d[t] - f[t]
        mse = mse + ALPHA * (e * e - mse)
    return PROT * f, sig


def simulate_inventory(d, S):
    """Periodic review at the start of each week, order-up-to S, lead time L, unmet demand backordered.
    Returns (units demanded, units filled from stock on demand, average on-hand, on-hand at end) over evaluation."""
    n = len(d); pipeline = np.zeros(n + L + 2); onhand = max(S[WARM], 0.0); back = 0.0
    dem = fill = oh_sum = 0.0
    for t in range(WARM, n):
        onhand += pipeline[t]
        c = min(back, onhand); onhand -= c; back -= c
        ip = onhand - back + pipeline[t + 1:t + L].sum()
        pipeline[t + L] += max(0.0, S[t] - ip)
        x = d[t]; served = min(x, onhand)
        onhand -= served; back += x - served
        dem += x; fill += served; oh_sum += onhand
    return dem, fill, oh_sum / (n - WARM), onhand
