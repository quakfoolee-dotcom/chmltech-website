"""Figures for Vol. 102(1): Process Intensification and Efficiency Enhancement in Hydrogen Electrolysis Plants."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from style import *

SLUG = "chmltech-online-journal-volume-102-issue-1"
F, R = 96485.0, 8.314

# Figure 1 — polarization curve from Eqs. (10)–(13) with representative PEM parameters.
# The paper gives no kinetic or resistance parameters, so representative values are used and chosen so that
# the curve passes through the DOE 2022 PEM stack status point quoted in the paper (1.9 V at 2.0 A cm-2, Table 2).
T = 353.15                                   # 80 °C
E_rev = 1.229 - 0.85e-3 * (T - 298.15)       # Section 2.1: dE/dT ≈ −0.85 mV/K; 1 bar, a_H2O = 1
j0a, aa = 1e-6, 1.0                          # anode (OER) exchange current density, A cm-2; symmetric transfer coeff.
j0c, ac = 0.2, 1.0                           # cathode (HER on Pt)
ASR = 0.09                                   # ohm cm2
jL, Bc = 4.0, 0.04                           # empirical mass-transport term: Bc ln(jL/(jL − j))
def bv(j, j0, a):                            # Eq. (11) inverted for symmetric α_a = α_c = a
    return R * T / (a * F) * np.arcsinh(j / (2 * j0))
j = np.linspace(0.005, 3.0, 400)
ec, ea, eo, en = bv(j, j0c, ac), bv(j, j0a, aa), j * ASR, Bc * np.log(jL / (jL - j))
V = E_rev + ec + ea + eo + en
V2 = E_rev + bv(2, j0c, ac) + bv(2, j0a, aa) + 2 * ASR + Bc * np.log(jL / (jL - 2))
assert abs(V2 - 1.90) < 0.01, V2
fig, ax = plt.subplots(figsize=(7.4, 4.3))
base = 1.0
layers = [(np.full_like(j, E_rev) - base, r"$E_{\mathrm{rev}}$ (80 °C)", LIGHT), (ec, r"Cathode activation $|\eta_{\mathrm{act,c}}|$", "#9FD3EE"),
          (ea, r"Anode activation $\eta_{\mathrm{act,a}}$ (OER)", BLUE), (eo, r"Ohmic $j \cdot \mathrm{ASR}$", GREEN), (en, r"Mass transport $\eta_{\mathrm{conc}}$", ORANGE)]
lo = np.full_like(j, base)
for h, lab, col in layers:
    ax.fill_between(j, lo, lo + h, color=col, lw=0, label=lab); lo = lo + h
ax.plot(j, V, color=NAVY, lw=2.4, label=r"Cell voltage $V_{\mathrm{cell}}$, Eq. (10)")
ax.axhline(1.481, color=NAVY, ls="--", lw=1.1); ax.text(2.97, 1.488, r"$E_{\mathrm{tn}}$ = 1.481 V", color=NAVY, fontsize=9, va="bottom", ha="right", bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
ax.plot([2.0], [1.9], "o", ms=8, mfc="white", mec=NAVY, mew=2, zorder=6)
ax.annotate("DOE 2022 PEM stack status\n1.9 V at 2.0 A cm$^{-2}$", xy=(2.0, 1.9), xytext=(1.0, 1.97), fontsize=9, color=NAVY, ha="center",
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=1), bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax.set_xlim(0, 3.0); ax.set_ylim(1.0, 2.15)
ax.set_xlabel(r"Current density $j$ (A cm$^{-2}$)"); ax.set_ylabel("Cell voltage (V)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), fontsize=9, ncol=2)
ax.grid(axis="x", visible=False)
save(fig, SLUG, "fig1-polarization")
print("pol: E_rev %.3f  at 2 A/cm2: ec %.3f ea %.3f ohm %.3f conc %.3f V %.3f" % (E_rev, bv(2, j0c, ac), bv(2, j0a, aa), 2 * ASR, Bc * np.log(jL / (jL - 2)), V2))

# Figure 2 — SEC vs cell voltage, Eq. (9)
k = 2 * F / 2.016e-3 / 3.6e6                 # kWh kg-1 per volt = 26.59
v = np.linspace(1.15, 2.4, 200)
fig, ax = plt.subplots(figsize=(7.8, 4.4))
ax.plot(v, k * v, color=NAVY, lw=2.4, label=r"Stack SEC, Eq. (9), $\eta_F$ = 1")
ax.plot(v, k * v / 0.95, color=NAVY, lw=1.4, ls="--", label=r"Stack SEC, $\eta_F$ = 0.95 (illustrative)")
for vv in (1.229, 1.481, 1.9):
    ax.plot([vv], [k * vv], "o", color=NAVY, ms=6, zorder=5)
ax.text(1.26, 31.6, r"$E_{\mathrm{rev}}$ 1.229 V → 32.7 kWh kg$^{-1}$", fontsize=9, color=NAVY, va="top")
ax.text(1.52, 38.6, r"$E_{\mathrm{tn}}$ 1.481 V → 39.4 kWh kg$^{-1}$ (HHV)", fontsize=9, color=NAVY, va="top")
ax.annotate("DOE 2022 PEM stack status\n1.9 V → 51 kWh kg$^{-1}$", xy=(1.9, k * 1.9), xytext=(1.62, 66), fontsize=9, color=NAVY, ha="center",
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=1))
ax.axhline(33.3, color=GREY, ls=":", lw=1.1); ax.text(2.38, 33.9, "LHV 33.3", color="#4A5568", fontsize=8.5, ha="right", va="bottom")
for y, lab, col in [(55, "DOE 2022 PEM system status 55", ORANGE), (46, "DOE ultimate system target 46", GREEN_D)]:
    ax.axhline(y, color=col, ls="--", lw=1.2); ax.text(1.16, y + 0.6, lab, color=col, fontsize=8.5, va="bottom")
# IRENA 2020 system ranges as bars on the right (system values include BOP; not tied to a cell voltage)
for x0, (a, b), lab, col in [(2.47, (50, 78), "AEL", BLUE), (2.57, (50, 83), "PEM", NAVY), (2.67, (45, 55), "SOEC*", GREEN_D)]:
    ax.plot([x0, x0], [a, b], color=col, lw=7, solid_capstyle="butt")
    ax.text(x0, b + 1.2, lab, ha="center", va="bottom", fontsize=8.5, color=col)
ax.text(2.57, 90.5, "IRENA 2020\nsystem ranges", ha="center", va="bottom", fontsize=8.5, color="#4A5568")
ax.axvline(2.42, color="#C7D2DF", lw=1)
ax.set_xlim(1.15, 2.74); ax.set_ylim(26, 100)
ax.set_xticks([1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
ax.set_xlabel(r"Cell voltage $V_{\mathrm{cell}}$ (V)"); ax.set_ylabel(r"Specific energy consumption (kWh kg$^{-1}$ H$_2$)")
top = ax.secondary_xaxis("top", functions=(lambda x: x, lambda x: x))
ef = [100, 90, 80, 70, 65]; top.set_xticks([1.481 / (e / 100) for e in ef]); top.set_xticklabels([f"{e}%" for e in ef]); top.set_xlabel(r"Voltage efficiency $\eta_{V,\mathrm{HHV}}$ = $E_{\mathrm{tn}}/V_{\mathrm{cell}}$, Eq. (14)")
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.93), fontsize=9)
save(fig, SLUG, "fig2-sec-voltage")
print("k = %.2f; 1.9 V -> %.1f" % (k, k * 1.9))

# Figure 3 — electrolysis plant block diagram with balance of plant
C_E, C_H, C_O, C_W, C_Q = ORANGE, BLUE, GREY, BRIGHT, "#B4410C"
fig, ax = plt.subplots(figsize=(9.2, 5.0)); ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis("off")
def box(x0, y0, w, h, txt, fill=LIGHT, tc=NAVY, fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=fill, ec="#9AB0C8", lw=1))
    ax.text(x0 + w / 2, y0 + h / 2, txt, ha="center", va="center", fontsize=fs, color=tc, fontweight="600" if bold else "normal", linespacing=1.15)
    return (x0, y0, w, h)
def arr(p, q, col, lw=1.8, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=11, color=col, lw=lw, ls=ls, shrinkA=0, shrinkB=0))
def lab(x, y, t, col=NAVY, ha="center", va="center", fs=8.5):
    ax.text(x, y, t, ha=ha, va=va, fontsize=fs, color=col)
# power band
box(1, 50, 17, 9, "AC grid or\nrenewable power")
box(23, 50, 13, 9, "Transformer")
box(41, 50, 16, 9, "Rectifier\n(AC → DC)")
arr((18.6, 54.5), (22.4, 54.5), C_E); arr((36.6, 54.5), (40.4, 54.5), C_E)
arr((49, 49.4), (49, 42.6), C_E); lab(50, 46, "low-voltage,\nhigh-current DC", C_E, ha="left")
# process band
box(42, 28, 14, 14, "Electrolyzer\nstack", fill=BLUE, tc="white", fs=10, bold=True)
box(14, 30, 13, 10, "Water\ntreatment\n(RO + IX)")
box(29, 30, 10, 10, "O$_2$–water\nseparator")
box(60, 30, 11, 10, "H$_2$–water\nseparator")
box(74, 30, 10, 10, "Deoxidizer")
box(87, 30, 12, 10, "Dryer\n(TSA / PSA)")
arr((2, 35), (13.4, 35), C_W); lab(1, 37.4, "Raw water", C_W, ha="left"); lab(1, 31.2, "8.9 kg per\nkg H$_2$ (stoich.)", C_W, ha="left", va="top", fs=8)
arr((27.6, 35), (28.4, 35), C_W)
arr((41.4, 37), (39.6, 37), C_O); arr((56.6, 37), (59.4, 37), C_H)
arr((71.6, 35), (73.4, 35), C_H); arr((84.6, 35), (86.4, 35), C_H)
arr((34, 40.6), (34, 47.6), C_O); lab(32.8, 45.8, "O$_2$ vent\nor use", C_O, ha="right", fs=8)
arr((93, 29.4), (93, 22.6), C_H)
box(87, 13, 12, 9, "Compressor")
arr((93, 12.4), (93, 4.6), C_H); lab(93, 2.5, "H$_2$ product to storage", C_H, fs=8.5)
# thermal band (water loop + heat)
box(29, 13, 10, 9, "Circulation\npump")
box(42, 13, 14, 9, "Heat\nexchanger")
arr((34, 29.4), (34, 22.6), C_W); arr((39.6, 17.5), (41.4, 17.5), C_W); arr((49, 22.6), (49, 27.4), C_W)
lab(50, 25, "cooled water", C_W, ha="left", fs=8)
box(61, 16, 19, 8, "Heat recovery\n(heat consumers)")
box(61, 4, 19, 8, "Dry cooler or\ncooling tower")
arr((56.6, 17.5), (58.5, 17.5), C_Q, style="-"); ax.plot([58.5, 58.5], [8, 20], color=C_Q, lw=1.8)
arr((58.5, 20), (60.4, 20), C_Q); arr((58.5, 8), (60.4, 8), C_Q)
lab(68, 27, "heat at 50–80 °C", C_Q, fs=8)
# legend of streams
for i, (c, t) in enumerate([(C_E, "Electricity"), (C_W, "Water"), (C_H, "Hydrogen"), (C_O, "Oxygen"), (C_Q, "Heat")]):
    y = 23 - i * 4.2
    ax.plot([2, 7], [y, y], color=c, lw=2.2); lab(8.5, y, t, ha="left", fs=8.5)
ax.text(42, 5.5, "All units except the stack are balance of plant;\ntheir power demand is P$_{\\mathrm{BOP}}$ in Eq. (16)", fontsize=8.5, color="#4A5568", ha="center", va="center")
save(fig, SLUG, "fig3-plant-bop")
