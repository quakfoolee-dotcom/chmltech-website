"""Monte Carlo reorder point and (s, Q) policy check - Chmltech Online Journal."""
import numpy as np

rng = np.random.default_rng(2026)

# Inputs (working days)
LAM = 1.2                      # customer orders per day (Poisson)
SIZE_MEAN, SIZE_CV = 12, 0.9   # pails per order (lognormal)
LT_MEAN, LT_SD = 30, 4         # normal supplier lead time (lognormal)
P_DELAY, DELAY = 0.15, (10, 25)  # disruption probability, extra days
Q, TARGET = 500, 0.95


def lognorm(mean, cv):
    s2 = np.log(1 + cv**2)
    return np.log(mean) - s2 / 2, np.sqrt(s2)


MU_S, SG_S = lognorm(SIZE_MEAN, SIZE_CV)
MU_L, SG_L = lognorm(LT_MEAN, LT_SD / LT_MEAN)


def lead_time(r):
    extra = r.uniform(*DELAY) if r.random() < P_DELAY else 0
    return max(1, round(r.lognormal(MU_L, SG_L) + extra))


def day_demand(r):
    n = r.poisson(LAM)
    return np.round(r.lognormal(MU_S, SG_S, n)).clip(1).sum()


# Steps 3-6: lead-time demand distribution and reorder point
ltd = np.array([sum(day_demand(rng) for _ in range(lead_time(rng)))
                for _ in range(20_000)])
rop = np.percentile(ltd, TARGET * 100)
print(f"Mean LTD {ltd.mean():.0f}, ROP@{TARGET:.0%} {rop:.0f}, "
      f"SS {rop - ltd.mean():.0f} pails")


# Step 8: day-by-day (s, Q) policy simulation with backorders
def simulate(s, years=100, seed=7):
    r = np.random.default_rng(seed)
    net, pipe = s + Q, []
    demand = short = cycles = bad = 0
    stocked_out = False
    for t in range(250 * years):
        arrived = [q for a, q in pipe if a == t]
        if arrived:
            net += sum(arrived)
            pipe = [(a, q) for a, q in pipe if a != t]
            cycles += len(arrived)
            bad += stocked_out * len(arrived)
            stocked_out = False
        x = day_demand(r)
        demand += x
        short += min(x, max(0, x - max(net, 0)))
        net -= x
        stocked_out |= net < 0
        while net + sum(q for _, q in pipe) <= s:
            pipe.append((t + lead_time(r) + 1, Q))  # arrives after L full days of demand
    return 1 - bad / cycles, 1 - short / demand


# Step 7: undershoot. With daily review, inventory position falls below s by about E[D^2]/(2E[D])
daily = np.array([day_demand(rng) for _ in range(50_000)])
under = (daily.var() + daily.mean()**2) / (2 * daily.mean())
for s_ in (rop, rop + under):
    csl, fill = simulate(round(s_))
    print(f"Policy check at s={s_:.0f}: cycle service {csl:.1%}, fill rate {fill:.1%}")
