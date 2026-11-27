"""Critical spare parts - Chmltech Online Journal (appendix script).
Cost-optimal stock of single-equipment spares from Palm's theorem, Eq. (1)-(2), and the screening indices of
Eqs. (3)-(4) for all 13 parts, at most likely values. Python 3 with SciPy."""
from scipy import stats

MARGIN, RATE_TH, CARRY = 300.0, 6.25, 0.25          # C$/t, t/h, carrying rate a year
CH = MARGIN * RATE_TH                               # C$ per hour of lost full-rate production
HOURS, OP = 8000.0, 8000.0 / 8760.0                 # operating hours a year; operating hours per calendar hour
# id, name, installed, needed, failures per running unit-year, lead time (weeks), unit cost (C$), repair h, capacity lost
PARTS = [("P1", "Feed pump seal", 2, 1, 0.20, 6, 4500, 12, 1.0), ("P2", "Feed pump bearings", 2, 1, 0.10, 2, 600, 12, 1.0),
         ("P3", "Transfer pump seal", 2, 1, 0.20, 6, 4000, 12, 1.0), ("P4", "Feed pump motor", 2, 1, 0.03, 10, 6000, 8, 1.0),
         ("P5", "Cooling water pump assembly", 3, 2, 0.15, 12, 18000, 24, 1.0), ("P6", "Agitator gearbox", 1, 1, 0.05, 20, 45000, 48, 1.0),
         ("P7", "Agitator double seal", 1, 1, 0.25, 8, 15000, 24, 1.0), ("P8", "Compressor valve set", 1, 1, 0.80, 4, 8000, 12, 1.0),
         ("P9", "Compressor motor", 1, 1, 0.02, 26, 90000, 72, 1.0), ("P10", "Preheater tube bundle", 1, 1, 0.02, 30, 120000, 96, 0.3),
         ("P11", "Control valve trim", 1, 1, 0.10, 8, 5000, 8, 0.1), ("P12", "Drive power module", 2, 1, 0.07, 8, 3000, 8, 1.0),
         ("P13", "Trip transmitter", 3, 2, 0.05, 3, 3500, 4, 1.0)]


def ebo(S, m):                                      # Eq. (1): expected backorders, Poisson demand of mean m in a lead time
    return sum((x - S) * stats.poisson.pmf(x, m) for x in range(S + 1, S + 60))


def cost(S, lam, K, L_h, cu, tr, f):                # Eq. (2): holding + expected lost production, single equipment
    return CARRY * cu * S + CH * f * (lam * K * tr + HOURS * ebo(S, lam * K * L_h / HOURS))


print(f'{"part":30s} {"m":>6s} {"index":>7s}  {"S*":>3s}  cost at S = 0..3 (C$/year)')
for pid, name, N, K, lam, lt, cu, tr, f in PARTS:
    L_h, tr = lt * 168 * OP, tr * OP               # lead time and repair in operating hours
    m = lam * (N if pid == "P13" else K) * L_h / HOURS   # P13 votes 2-out-of-3: all three transmitters are live
    if N == K:                                      # single equipment: Eq. (3) and the optimum of Eq. (2)
        idx = lam * K * L_h * CH * f / (CARRY * cu)
        c = [cost(S, lam, K, L_h, cu, tr, f) for S in range(4)]
        print(f'{pid + " " + name:30s} {m:6.3f} {idx:7.1f}  {c.index(min(c)):3d}  ' + "  ".join(f"{x:>10,.0f}" for x in c))
    else:                                           # one installed spare: Eq. (4); treat above 0.5 as worth a spare
        pair = (3 * lam) * (2 * lam) if pid == "P13" else (lam * K) ** 2   # first failure, then a second while it is out
        idx = pair * L_h ** 2 * CH * f / (2 * HOURS * CARRY * cu)
        print(f'{pid + " " + name:30s} {m:6.3f} {idx:7.2f}  {"1" if idx > 0.5 else "0":>3s}  (installed spare: simulate)')
