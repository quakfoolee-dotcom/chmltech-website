"""Validation-study simulation for an LLM smart-factory assessor (Chmltech Online Journal, Vol. 106, Issue 16).

Plants are scored on 16 dimensions with 0-5 bands (the structure of the Smart Industry Readiness Index).
Two human assessors and one LLM assessor score each plant. The simulation asks how many plants a
validation study needs, and which agreement statistics expose which LLM failure modes.

Assumptions (stated in the paper): latent maturity = plant effect N(2.2, 0.7^2) + dimension effect N(0, 0.7^2);
an assessor's band = round(latent + bias + N(0, sigma^2)), clipped to 0-5; human sigma = 0.45.

Usage: python3 validation_sim.py  ->  results.json
"""
import json
import numpy as np

D, K = 16, 6                         # dimensions, bands 0..5
W = np.array([[(i - j) ** 2 for j in range(K)] for i in range(K)], float) / (K - 1) ** 2


def qwk(a, b):
    """Quadratic weighted kappa for two integer arrays (bands 0..5)."""
    O = np.zeros((K, K)); np.add.at(O, (a, b), 1)
    n = O.sum(); E = np.outer(O.sum(1), O.sum(0)) / n
    return 1 - (W * O).sum() / (W * E).sum()


def band(x): return np.clip(np.rint(x), 0, K - 1).astype(int)


SCEN = {
    'S1': dict(label='LLM as consistent as a human assessor', sigma=0.45, bias=0.0, gap=0.0, policy='score'),
    'S2': dict(label='LLM noisier than a human (sigma 0.65)', sigma=0.65, bias=0.0, gap=0.0, policy='score'),
    'S3': dict(label='LLM lenient by half a band', sigma=0.45, bias=0.5, gap=0.0, policy='score'),
    'S4': dict(label='30% of dimensions without evidence; LLM guesses', sigma=0.45, bias=0.0, gap=0.3, policy='guess'),
    'S5': dict(label='30% of dimensions without evidence; LLM abstains', sigma=0.45, bias=0.0, gap=0.3, policy='abstain'),
    'S6': dict(label='Calibration: LLM exactly at the margin (sigma 0.75)', sigma=0.75, bias=0.0, gap=0.0, policy='score'),
}


def study(r, n, sc, sig_h=0.45):
    lat = r.normal(2.2, 0.7, (n, 1)) + r.normal(0, 0.7, (n, D))
    h1 = band(lat + r.normal(0, sig_h, lat.shape)); h2 = band(lat + r.normal(0, sig_h, lat.shape))
    llm = band(lat + sc['bias'] + r.normal(0, sc['sigma'], lat.shape)).astype(float)
    gap = r.random(lat.shape) < sc['gap']
    if sc['policy'] == 'guess':      # no evidence: the model fills the band from the plant's other answers and a generic prior
        guess = band(0.5 * np.nanmean(np.where(gap, np.nan, llm), axis=1, keepdims=True) + 0.5 * 2.5 + r.normal(0, 0.6, lat.shape))
        llm = np.where(gap, guess, llm)
    elif sc['policy'] == 'abstain':
        llm = np.where(gap, np.nan, llm)
    return h1, h2, llm, gap


def stats(h1, h2, llm, gap=None):
    """Symmetric design: the model is compared with both assessors, on the dimensions it scored;
    the human-human kappa is computed on the same dimensions."""
    m = ~np.isnan(llm)
    a = llm[m].astype(int)
    k_l = 0.5 * (qwk(a, h1[m]) + qwk(a, h2[m]))
    out = dict(k_hh=qwk(h1[m], h2[m]), k_lh=k_l, exact=float(np.mean(a == h1[m])),
               within1=float(np.mean(np.abs(a - h1[m]) <= 1)), bias=float(np.mean(a - (h1[m] + h2[m]) / 2)),
               coverage=float(m.mean()), hh_exact=float(np.mean(h1 == h2)), hh_within1=float(np.mean(np.abs(h1 - h2) <= 1)))
    if gap is not None and gap.any() and m[gap].all():          # guessing model: agreement on gap and non-gap dimensions
        out['k_gap'] = qwk(llm[gap].astype(int), h1[gap]); out['k_nogap'] = qwk(llm[~gap].astype(int), h1[~gap])
        out['within1_gap'] = float(np.mean(np.abs(llm[gap] - h1[gap]) <= 1))
    return out


def power(r, n, sc, delta=0.10, studies=300, boots=400):
    """Non-inferiority: lower 95% bootstrap bound of (mean k(LLM,H) - k(H1,H2)) above -delta; plants resampled (percentile)."""
    ok, diffs = 0, []
    for _ in range(studies):
        h1, h2, llm, _g = study(r, n, sc)
        d0 = stats(h1, h2, llm); diffs.append(d0['k_lh'] - d0['k_hh'])
        bs = []
        for _ in range(boots):
            i = r.integers(0, n, n)
            s = stats(h1[i], h2[i], llm[i]); bs.append(s['k_lh'] - s['k_hh'])
        ok += np.percentile(bs, 2.5) > -delta
    return ok / studies, float(np.mean(diffs))


def main():
    r = np.random.default_rng(16)
    out = dict(scenarios={k: v['label'] for k, v in SCEN.items()}, big={}, power={})
    for k, sc in SCEN.items():   # large-sample values of each statistic
        h1, h2, llm, g = study(r, 4000, sc); out['big'][k] = stats(h1, h2, llm, g)
        print(k, {a: round(b, 3) for a, b in out['big'][k].items()})
    for k in SCEN:
        out['power'][k] = {}
        for n in (10, 20, 30, 50, 80):
            p, d = power(r, n, SCEN[k]); out['power'][k][n] = p
            print(k, n, round(p, 2), round(d, 3), flush=True)
    json.dump(out, open('results.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
