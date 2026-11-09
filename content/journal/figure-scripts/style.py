"""Shared figure style for Chmltech Online Journal papers (V4.15).
Figures are drawn with matplotlib and saved as SVG with live text (fonttype none), so they use the site fonts,
stay sharp at any size and print cleanly. Colours follow the site palette."""
import io, os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, BRIGHT, GREEN, GREEN_D, ORANGE, GREY, LIGHT = "#0B2A5A", "#0B6FA4", "#0A9AD8", "#8DC63F", "#4D7F12", "#E07A3A", "#8A94A6", "#DCE4EE"
SERIES = [BLUE, GREEN_D, ORANGE, NAVY, BRIGHT, GREY]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "journal", "figures")

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": ["Inter", "DejaVu Sans"], "font.size": 10.5,
    "axes.edgecolor": "#9AA8BA", "axes.labelcolor": NAVY, "axes.titlecolor": NAVY, "axes.titlesize": 11.5, "axes.titleweight": "600",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#E6ECF3", "grid.linewidth": 0.8,
    "xtick.color": "#4A5568", "ytick.color": "#4A5568", "legend.frameon": False, "legend.fontsize": 9.5,
    "lines.linewidth": 2.2, "figure.dpi": 100, "savefig.bbox": "tight", "savefig.pad_inches": 0.08,
})


def save(fig, slug, fid):
    """Write figure as responsive inline-ready SVG: journal/figures/<slug>/<fid>.svg"""
    buf = io.StringIO(); fig.savefig(buf, format="svg", transparent=True); plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r'<svg([^>]*?) width="[^"]+" height="[^"]+"', r'<svg\1', s, count=1)
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"\n\s*", "\n", s)
    d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, fid + ".svg"), "w").write(s)
    return os.path.join(d, fid + ".svg")
