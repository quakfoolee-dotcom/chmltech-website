"""Animated hero illustrations for solution pages (V4.4)."""
import math
from course_art import STYLE, G, B, NV, PA, CARD, LINE, _gear


def ai_art():
    layers = [[(70, 70), (70, 150), (70, 230)], [(170, 50), (170, 115), (170, 185), (170, 250)], [(270, 90), (270, 150), (270, 210)]]
    out = ""
    k = 0
    for a, b in zip(layers, layers[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                d = f"M{x1} {y1} L{x2} {y2}"
                out += f'<path d="{d}" stroke="{LINE}" stroke-width="1.4"/>'
                if k % 3 == 0:
                    out += f'<circle r="3.5" fill="{G if k % 2 else B}"><animateMotion dur="2.2s" begin="-{(k % 7) * 0.3:.1f}s" repeatCount="indefinite" path="{d}"/></circle>'
                k += 1
    for L in layers:
        for i, (x, y) in enumerate(L):
            out += f'<circle class="ha-pulse" style="animation-delay:{(x + y) % 9 * 0.2:.1f}s" cx="{x}" cy="{y}" r="11" fill="{NV}" stroke="{G if x == 170 else B}" stroke-width="3"/>'
    for i, y in enumerate([90, 150, 210]):
        out += f'<path d="M270 {y} C300 {y} 300 150 322 150" stroke="{LINE}" stroke-width="1.4" fill="none"/>'
    out += f'<g class="ha-float"><rect x="318" y="112" width="74" height="60" rx="14" fill="{CARD}" stroke="{G}" stroke-width="2.5"/><path d="M336 172 l-6 14 l18 -14 z" fill="{CARD}" stroke="{G}" stroke-width="2.5" stroke-linejoin="round"/>'
    for j in range(3):
        out += f'<circle class="ha-pulse" style="animation-delay:{j * 0.25:.2f}s;animation-duration:1.2s" cx="{340 + j * 15}" cy="142" r="4.5" fill="{PA}"/>'
    out += '</g>'
    return out + '<text class="ha-small" x="200" y="306" text-anchor="middle">FROM DATA TO DECISIONS AND ANSWERS</text>'


def bpo_art():
    messy = "M40 150 C80 40 120 260 160 120 S220 40 200 200 S300 260 280 110 S360 60 360 150"
    clean = "M40 150 C80 150 120 150 160 150 S220 150 200 150 S300 150 280 150 S360 150 360 150"
    out = f'<path fill="none" stroke="{LINE}" stroke-width="10" stroke-linecap="round" opacity=".55"><animate attributeName="d" dur="6s" repeatCount="indefinite" values="{messy};{clean};{clean};{messy}" keyTimes="0;0.4;0.85;1" calcMode="spline" keySplines=".5 0 .2 1;0 0 1 1;.5 0 .2 1"/></path>'
    out += f'<path fill="none" stroke="{G}" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 12"><animate attributeName="d" dur="6s" repeatCount="indefinite" values="{messy};{clean};{clean};{messy}" keyTimes="0;0.4;0.85;1" calcMode="spline" keySplines=".5 0 .2 1;0 0 1 1;.5 0 .2 1"/><animate attributeName="stroke-dashoffset" values="0;-44" dur="1s" repeatCount="indefinite"/></path>'
    for i, (lbl, x) in enumerate([("IDENTIFY", 80), ("ANALYZE", 160), ("IMPLEMENT", 240), ("MONITOR", 320)]):
        out += f'<g class="ha-float" style="animation-delay:{i * 0.4:.1f}s"><rect x="{x - 40}" y="232" width="80" height="30" rx="15" fill="{NV}" stroke="{G if i % 2 else B}" stroke-width="2"/><text class="ha-small" x="{x}" y="251" text-anchor="middle" style="fill:{PA};font-weight:600">{lbl}</text></g>'
    out += f'<circle cx="40" cy="150" r="12" fill="{NV}" stroke="{B}" stroke-width="3"/><circle cx="360" cy="150" r="12" fill="{NV}" stroke="{G}" stroke-width="3"/>'
    out += f'<text class="ha-small" x="40" y="186" text-anchor="middle">REQUEST</text><text class="ha-small" x="360" y="186" text-anchor="middle">DONE</text>'
    return out + '<text class="ha-small" x="200" y="306" text-anchor="middle">SIMPLE, CLEAR, CONSISTENT PROCESSES</text>'


def pi_art():
    out = ""
    tops = []
    for i in range(5):
        x, y = 22 + i * 54, 236 - i * 38
        tops.append((x + 27, y))
        out += f'<rect x="{x}" y="{y}" width="54" height="{276 - y}" fill="{CARD}" stroke="{LINE}"/>'
    path = "M" + " L".join(f"{x} {y - 10}" for x, y in tops)
    out += f'<path d="{path}" fill="none" stroke="{G}" stroke-width="3" stroke-dasharray="4 6"/>'
    out += f'<circle r="10" fill="{G}"><animateMotion dur="5s" repeatCount="indefinite" path="{path}" keyPoints="0;1;1" keyTimes="0;0.8;1" calcMode="linear"/></circle>'
    for i, lbl in enumerate(["MAP", "MEASURE", "IMPROVE", "STANDARD", "SUSTAIN"]):
        x, y = tops[i]
        out += f'<text class="ha-small" x="{x}" y="{y + 20}" text-anchor="middle" style="fill:{PA};font-weight:600;font-size:9px">{lbl}</text>'
    cx, cy = 335, 210
    out += f'<path d="M{cx - 48} {cy} A48 48 0 0 1 {cx + 48} {cy}" fill="none" stroke="{LINE}" stroke-width="10" stroke-linecap="round"/>'
    out += f'<path d="M{cx - 48} {cy} A48 48 0 0 1 {cx + 48} {cy}" fill="none" stroke="{G}" stroke-width="10" stroke-linecap="round" stroke-dasharray="151" stroke-dashoffset="151"><animate attributeName="stroke-dashoffset" values="151;30;30;151" keyTimes="0;0.6;0.9;1" dur="5s" repeatCount="indefinite"/></path>'
    out += f'<line x1="{cx}" y1="{cy}" x2="{cx - 38}" y2="{cy}" stroke="{PA}" stroke-width="4" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};145 {cx} {cy};145 {cx} {cy};0 {cx} {cy}" keyTimes="0;0.6;0.9;1" dur="5s" repeatCount="indefinite"/></line>'
    out += f'<circle cx="{cx}" cy="{cy}" r="7" fill="{PA}"/><text class="ha-small" x="{cx}" y="{cy + 28}" text-anchor="middle">KPI</text>'
    out += f'<g class="ha-spin" style="animation-duration:14s"><path d="{_gear(330, 60, 22, 9, 7, 7)}" fill="none" stroke="{B}" stroke-width="2.5" fill-rule="evenodd"/></g>'
    return out + '<text class="ha-small" x="200" y="310" text-anchor="middle">LEAN IMPROVEMENT THAT STICKS</text>'


def lss_art():
    """DMAIC phases light up in turn; during Improve the process curve narrows inside the spec limits
    and the out-of-spec defects disappear; Control holds the gain. One shared 10 s timeline."""
    T = 10.0
    kt = lambda *t: ";".join(f"{x / T:.3f}" for x in t)
    o = '<line x1="40" y1="262" x2="360" y2="262" stroke="#2D5FA0" stroke-width="2"/>'
    # spec limits and target
    for x, t in ((110, "LSL"), (290, "USL")):
        o += (f'<line x1="{x}" y1="112" x2="{x}" y2="262" stroke="#F7B58A" stroke-width="2" stroke-dasharray="5 5"/>'
              f'<text class="ha-small" x="{x}" y="106" text-anchor="middle" style="fill:#F7B58A;font-weight:700;font-size:10px">{t}</text>')
    o += (f'<line x1="200" y1="112" x2="200" y2="262" stroke="{LINE}" stroke-width="1.5"/>'
          f'<text class="ha-small" x="200" y="106" text-anchor="middle" style="fill:{PA};font-weight:700;font-size:10px">TARGET</text>')
    wide = "M50 262 C125 262 145 168 200 168 C255 168 275 262 350 262"
    narrow = "M50 262 C160 262 180 120 200 120 C220 120 240 262 350 262"
    vals = f"{wide};{wide};{narrow};{narrow};{wide}"
    keys = kt(0, 6.0, 7.6, 9.7, T)
    o += (f'<path d="{wide}" fill="{G}" fill-opacity=".22" stroke="{G}" stroke-width="3">'
          f'<animate attributeName="d" values="{vals}" keyTimes="{keys}" dur="{T}s" repeatCount="indefinite"/></path>')
    # defects outside the spec limits, present until Improve
    for x, y in ((72, 256), (88, 252), (96, 257), (304, 257), (314, 252), (330, 256)):
        o += (f'<circle cx="{x}" cy="{y}" r="4" fill="#E07A3A">'
              f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="{kt(0, 6.2, 7.2, 9.7, T)}" dur="{T}s" repeatCount="indefinite"/></circle>')
    # DMAIC phase chips
    phases = ["Define", "Measure", "Analyze", "Improve", "Control"]
    for i, p in enumerate(phases):
        x = 110 + i * 45; t0, t1 = i * 2.0, i * 2.0 + 2.0
        on = f'values="0;0;1;1;0;0" keyTimes="{kt(0, max(t0, 0.001), t0 + 0.2, t1 - 0.05, t1, T) if i else kt(0, 0.001, 0.2, t1 - 0.05, t1, T)}"'
        o += (f'<circle cx="{x}" cy="46" r="17" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>'
              f'<circle cx="{x}" cy="46" r="17" fill="{G}" opacity="0"><animate attributeName="opacity" {on} dur="{T}s" repeatCount="indefinite"/></circle>'
              f'<text x="{x}" y="51" text-anchor="middle" style="fill:{PA};font:700 14px var(--font-head,Arial)">{p[0]}</text>'
              f'<text class="ha-small" x="200" y="84" text-anchor="middle" style="fill:{PA};font-weight:700;font-size:11px;letter-spacing:.12em" opacity="0">{p.upper()}'
              f'<animate attributeName="opacity" {on} dur="{T}s" repeatCount="indefinite"/></text>')
        if i: o += f'<line x1="{x - 28}" y1="46" x2="{x - 17}" y2="46" stroke="{LINE}" stroke-width="2"/>'
    o += (f'<text class="ha-small" x="200" y="292" text-anchor="middle" style="fill:{PA};font-weight:600;font-size:10px">LESS WASTE. LESS VARIATION. FEWER DEFECTS.</text>')
    return o


def svc_art(slug, title):
    fn = {"artificial-intelligence": ai_art, "business-process-optimization": bpo_art, "process-improvement": pi_art, "lean-six-sigma-training": lss_art,
          # V4.23 rewrites reuse the closest existing illustration
          "iso9001": pi_art, "leadership-operating-system": pi_art, "process-mapping": bpo_art, "scaling-up": bpo_art,
          "project-portfolio-management": bpo_art, "operational-efficiency": lss_art, "rapid-lean-assessment": lss_art}.get(slug)
    if not fn: return ""
    return (f'<div class="hero-art"><svg viewBox="0 0 400 320" role="img" aria-label="Animated illustration: {title}" xmlns="http://www.w3.org/2000/svg">{STYLE}{fn()}</svg></div>')
