"""AI OS diagram V3: 2D diagram with traceable paths, six-block core and governance ring."""

CX, CY = 360, 212          # core centre
GOV_R = 142                # governance ring radius

INPUTS = ["ERP & accounting", "CRM & sales", "Documents & SOPs", "Email & chat", "Spreadsheets"]
OUTPUTS = ["AI assistants", "Automated workflows", "Live KPIs", "Better decisions"]
# which results each system feeds (indices into OUTPUTS)
FEEDS = {0: [1, 2, 3], 1: [0, 1, 2], 2: [0, 1], 3: [0, 1], 4: [2, 3]}

IN_SENT = [
    "ERP and accounting data feeds automated workflows, live KPIs and better decisions.",
    "CRM and sales data feeds AI assistants, automated workflows and live KPIs.",
    "Your documents and SOPs become company knowledge for AI assistants and automated workflows.",
    "Email and chat give AI assistants and automated workflows the context of each conversation.",
    "Spreadsheets feed live KPIs and better decisions, without manual copying.",
]
OUT_SENT = [
    "AI assistants draw on CRM, documents and SOPs, and email and chat.",
    "Automated workflows draw on ERP, CRM, documents and email.",
    "Live KPIs draw on ERP, CRM and spreadsheets.",
    "Better decisions draw on ERP and spreadsheets, through the knowledge and dashboards in the core.",
]
CORE_SENT = ("The AI OS core joins your data, company knowledge, AI agents, workflows and dashboards "
             "into one system that every tool shares.")
GOV_SENT = ("Every connection passes through the governance ring: access controls, audit trails, "
            "privacy safeguards and human approval where judgement matters.")
DEFAULT_SENT = "Hover over or tap any part of the diagram to trace how your data becomes results."

IN_Y = [86, 154, 222, 290, 358]
OUT_Y = [120, 188, 256, 324]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def svg():
    o = []
    # links (input chips end at x=188, output chips start at x=528)
    for i, y in enumerate(IN_Y):
        d = f"M188 {y} C246 {y} 236 {CY} {CX-86} {CY}"
        o.append(f'<g class="aios-path" data-in="{i}"><path class="aios-link" d="{d}"/>'
                 + "".join(f'<circle class="aios-packet" r="4.5" fill="#8DC63F"><animateMotion dur="3.2s" '
                           f'begin="-{(i*0.45 + k*1.6):.2f}s" repeatCount="indefinite" path="{d}"/></circle>'
                           for k in range(2)) + "</g>")
    for j, y in enumerate(OUT_Y):
        d = f"M{CX+86} {CY} C{CX+150} {CY} 478 {y} 528 {y}"
        o.append(f'<g class="aios-path" data-out="{j}"><path class="aios-link" d="{d}"/>'
                 + "".join(f'<circle class="aios-packet" r="4.5" fill="#29B6F6"><animateMotion dur="2.8s" '
                           f'begin="-{(j*0.5 + k*1.4):.2f}s" repeatCount="indefinite" path="{d}"/></circle>'
                           for k in range(2)) + "</g>")
    # governance ring with its label running along the bottom arc
    o.append(f'''<g class="aios-gov" data-part="gov" tabindex="0" role="button" aria-label="Governance ring: {esc(GOV_SENT)}">
  <circle class="aios-gov-hit" cx="{CX}" cy="{CY}" r="{GOV_R}"/>
  <circle class="aios-gov-ring" cx="{CX}" cy="{CY}" r="{GOV_R}"/>
  <path id="aios-gov-arc" d="M{CX-GOV_R-16} {CY} A{GOV_R+16} {GOV_R+16} 0 0 0 {CX+GOV_R+16} {CY}" fill="none"/>
  <text class="aios-gov-text"><textPath href="#aios-gov-arc" startOffset="50%" text-anchor="middle">SECURITY · GOVERNANCE · HUMAN OVERSIGHT</textPath></text>
  <g class="aios-shield" transform="translate({CX-11} {CY-GOV_R-13})"><path d="M11 1l9 3.4v6.8c0 5.7-4 9.1-9 10.2-5-1.1-9-4.5-9-10.2V4.4z"/><path class="tick" d="M7 11.5l3 3 5-5.5"/></g>
</g>''')
    # chips
    for i, (t, y) in enumerate(zip(INPUTS, IN_Y)):
        o.append(f'<g class="aios-chip" data-in="{i}" tabindex="0" role="button" aria-label="{esc(t)}: {esc(IN_SENT[i])}">'
                 f'<rect x="12" y="{y-22}" width="176" height="44" rx="10"/><circle cx="30" cy="{y}" r="5" fill="#8DC63F"/>'
                 f'<text x="44" y="{y+5}">{esc(t)}</text></g>')
    for j, (t, y) in enumerate(zip(OUTPUTS, OUT_Y)):
        o.append(f'<g class="aios-chip aios-out" data-out="{j}" tabindex="0" role="button" style="animation-delay:{j*0.7:.1f}s" '
                 f'aria-label="{esc(t)}: {esc(OUT_SENT[j])}">'
                 f'<rect x="528" y="{y-22}" width="180" height="44" rx="10"/><circle cx="546" cy="{y}" r="5" fill="#29B6F6"/>'
                 f'<text x="560" y="{y+5}">{esc(t)}</text></g>')
    # core
    o.append(f'''<g class="aios-core" data-part="core" tabindex="0" role="button" aria-label="AI OS core: {esc(CORE_SENT)}">
  <circle class="aios-pulse" cx="{CX}" cy="{CY}" r="84"/>
  <circle class="aios-ring aios-ring-1" cx="{CX}" cy="{CY}" r="100"/>
  <circle class="aios-ring aios-ring-2" cx="{CX}" cy="{CY}" r="116"/>
  <circle class="aios-core-disc" cx="{CX}" cy="{CY}" r="84"/>
  <g class="aios-orbit"><circle cx="{CX}" cy="{CY-100}" r="7" fill="#071C3D" stroke="#8DC63F" stroke-width="4"/><circle cx="{CX+116}" cy="{CY}" r="7" fill="#071C3D" stroke="#29B6F6" stroke-width="4"/></g>
  <text class="aios-title" x="{CX}" y="{CY-14}" text-anchor="middle">AI OS</text>
  <text class="aios-sub" x="{CX}" y="{CY+10}" text-anchor="middle">data · knowledge</text>
  <text class="aios-sub" x="{CX}" y="{CY+26}" text-anchor="middle">agents · workflows</text>
  <text class="aios-sub" x="{CX}" y="{CY+42}" text-anchor="middle">dashboards</text>
</g>''')
    o.append('<text class="aios-label" x="12" y="46">YOUR SYSTEMS &amp; DATA</text>'
             '<text class="aios-label" x="708" y="80" text-anchor="end">WHAT YOUR TEAM GETS</text>')
    aria = ("Diagram of an AI Operating System: data from ERP, CRM, documents, email and spreadsheets flows into a "
            "central AI OS core of data, knowledge, agents, workflows and dashboards, which delivers AI assistants, "
            "automated workflows, live KPIs and better decisions. A governance ring of security, governance and human "
            "oversight surrounds the core. Select any part to read how it connects.")
    return (f'<figure class="aios aios-v3" id="aios">'
            f'<svg viewBox="0 0 720 {CY+GOV_R+40}" aria-label="{aria}" role="group" xmlns="http://www.w3.org/2000/svg">'
            + "".join(o) + '</svg>'
            f'<figcaption class="aios-cap" aria-live="polite">{esc(DEFAULT_SENT)}</figcaption></figure>')


CSS = """
/* AI OS diagram V3: traceable paths and governance ring */
.aios-v3 .aios-chip,.aios-v3 .aios-core,.aios-v3 .aios-gov{cursor:pointer;outline:none}
.aios-v3 .aios-chip,.aios-v3 .aios-path,.aios-v3 .aios-core,.aios-v3 .aios-gov{transition:opacity .25s ease}
.aios-v3 .aios-core-disc{fill:#0F3A74;stroke:#2D5FA0;stroke-width:2;transition:stroke .25s}
.aios-v3 .aios-pulse,.aios-v3 .aios-ring,.aios-v3 .aios-orbit{pointer-events:none}
.aios-v3 .aios-gov-text{pointer-events:bounding-box}
.aios-v3 .aios-gov-hit{fill:none;stroke:transparent;stroke-width:22;pointer-events:stroke}
.aios-v3 .aios-gov-ring{fill:none;stroke:#8DC63F;stroke-width:1.6;stroke-dasharray:7 6;opacity:.85;pointer-events:none;transition:stroke-width .25s,opacity .25s}
.aios-v3 .aios-gov-text{fill:#8DC63F;font-family:var(--font-body);font-size:11.5px;font-weight:600;letter-spacing:.16em}
.aios-v3 .aios-shield path{fill:#071C3D;stroke:#8DC63F;stroke-width:1.8;stroke-linejoin:round}
.aios-v3 .aios-shield .tick{fill:none;stroke-linecap:round}
.aios-v3.is-tracing .aios-chip,.aios-v3.is-tracing .aios-path{opacity:.22}
.aios-v3.is-tracing .is-on{opacity:1}
.aios-v3 .aios-path.is-on .aios-link{stroke:#6FA8E8;stroke-dasharray:none}
.aios-v3 .aios-path[data-in].is-on .aios-link{stroke:#8DC63F}
.aios-v3 .aios-path[data-out].is-on .aios-link{stroke:#29B6F6}
.aios-v3 .aios-chip.is-on rect{stroke:#FFFFFF;stroke-width:2}
.aios-v3 .aios-chip:focus-visible rect,.aios-v3 .aios-core:focus-visible .aios-core-disc{stroke:#FFFFFF;stroke-width:3}
.aios-v3 .aios-core.is-on .aios-core-disc{stroke:#29B6F6}
.aios-v3 .aios-gov.is-on .aios-gov-ring,.aios-v3 .aios-gov:focus-visible .aios-gov-ring{stroke-width:3.5;opacity:1;stroke-dasharray:none}
.aios-v3 .aios-cap{margin:6px 4px 2px;min-height:2.9em;color:#C9D5E6;font-size:14.5px;line-height:1.45;text-align:center}
@media (prefers-reduced-motion:reduce){.aios-v3 .aios-chip,.aios-v3 .aios-path{transition:none}}
"""

JS = """
(function(){
  var fig=document.getElementById('aios'); if(!fig) return;
  var FEEDS=%(feeds)s, IN=%(ins)s, OUT=%(outs)s, CORE=%(core)s, GOV=%(gov)s, DEF=%(dflt)s;
  var cap=fig.querySelector('.aios-cap'), pinned=null;
  function q(s){return Array.prototype.slice.call(fig.querySelectorAll(s));}
  function clear(){fig.classList.remove('is-tracing');q('.is-on').forEach(function(e){e.classList.remove('is-on');});}
  function on(s){q(s).forEach(function(e){e.classList.add('is-on');});}
  function show(el){
    clear(); if(!el){cap.textContent=DEF;return;}
    fig.classList.add('is-tracing');
    var i=el.getAttribute('data-in'), j=el.getAttribute('data-out'), p=el.getAttribute('data-part');
    if(i!==null){i=+i;on('[data-in="'+i+'"]');on('.aios-core');FEEDS[i].forEach(function(k){on('[data-out="'+k+'"]');});cap.textContent=IN[i];}
    else if(j!==null){j=+j;on('[data-out="'+j+'"]');on('.aios-core');Object.keys(FEEDS).forEach(function(k){if(FEEDS[k].indexOf(j)>=0)on('[data-in="'+k+'"]');});cap.textContent=OUT[j];}
    else if(p==='core'){fig.classList.remove('is-tracing');on('.aios-core');cap.textContent=CORE;}
    else if(p==='gov'){fig.classList.remove('is-tracing');on('.aios-gov');cap.textContent=GOV;}
  }
  q('.aios-chip,.aios-core,.aios-gov').forEach(function(el){
    el.addEventListener('mouseenter',function(){if(!pinned)show(el);});
    el.addEventListener('mouseleave',function(){if(!pinned)show(null);});
    el.addEventListener('focus',function(){show(el);});
    el.addEventListener('blur',function(){if(!pinned)show(null);});
    el.addEventListener('click',function(e){e.stopPropagation();pinned=(pinned===el)?null:el;show(pinned||el);});
    el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();el.click();}if(e.key==='Escape'){pinned=null;show(null);el.blur();}});
  });
  document.addEventListener('click',function(){if(pinned){pinned=null;show(null);}});
  var svg=fig.querySelector('svg');
  if('IntersectionObserver' in window&&svg.pauseAnimations){new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?svg.unpauseAnimations():svg.pauseAnimations();});}).observe(fig);}
})();
"""


def js():
    import json
    return JS % dict(feeds=json.dumps(FEEDS), ins=json.dumps(IN_SENT), outs=json.dumps(OUT_SENT),
                     core=json.dumps(CORE_SENT), gov=json.dumps(GOV_SENT), dflt=json.dumps(DEFAULT_SENT))


# ---------------------------------------------------------------------------
# Apply to the site: python3 content/gen/aios_diagram.py .   (then run seo_pass.py)
# Replaces the diagram in ai-operating-system.html, writes assets/js/aios.js and
# keeps one copy of the V3 CSS block at the end of styles.css. Safe to rerun.
if __name__ == "__main__":
    import os, re, sys
    site = sys.argv[1] if len(sys.argv) > 1 else "."
    page = os.path.join(site, "ai-operating-system.html")
    h = open(page, encoding="utf-8").read()
    a = h.index('<figure class="aios'); b = h.index("</figure>", a) + len("</figure>")
    h = h[:a] + svg() + h[b:]
    if "assets/js/aios.js" not in h:
        h = h.replace("</body>", '<script src="assets/js/aios.js" defer></script>\n</body>', 1)
    open(page, "w", encoding="utf-8").write(h)
    open(os.path.join(site, "assets/js/aios.js"), "w", encoding="utf-8").write(
        "/* AI OS diagram V3: traceable paths (generated by content/gen/aios_diagram.py) */" + js())
    css_p = os.path.join(site, "assets/css/styles.css"); css = open(css_p, encoding="utf-8").read()
    css = re.sub(r"\n/\* AI OS diagram V3:.*?(?=\n/\*(?! AI OS diagram V3)|\Z)", "", css, flags=re.S)
    open(css_p, "w", encoding="utf-8").write(css.rstrip("\n") + "\n" + CSS.strip("\n") + "\n")
    print("AI OS diagram V3 applied to", page)
