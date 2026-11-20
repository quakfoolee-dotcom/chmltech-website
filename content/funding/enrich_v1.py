"""Funding Match Draft V1: structured eligibility rules for content/grants.json.

Auto-extracted from each program's eligibility text with conservative patterns, plus manual overrides
(OVERRIDES) for high-traffic programs. A rule is only set when the text states it plainly; unknown stays
None, and the matcher never rules a program out on an unknown. Phase 1 (agents + red team against the
official pages) replaces this file's output before publication.

Output: content/funding/rules_v1.json  {id: {inc, forprofit, emp_min, emp_max, rev_min, rev_max, yrs_min,
         pct, stack, pre, multi, src}}
"""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "grants.json")
OUT = os.path.join(HERE, "rules_v1.json")

WORDN = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "ten": 10}
GUARD = re.compile(r"\b(preference|priority|prioriti\w*|partners?|example|e\.g\.|for loans|streams?|tracks?|tiers?|components?|stage|rural|jobs|new entrants|commercial|1[ABC]|or demonstrated|depending)\b|\(\d|\(or ", re.I)
EMPW = r"(?:full[- ]time(?:[- ]equivalent)?|FTEs?|employees?|people|staff|workers)"

def num(s):
    s = s.lower().replace(",", "").strip()
    if s in WORDN: return WORDN[s]
    return int(float(s))

def money(n, unit):
    v = float(n.replace(",", ""))
    u = (unit or "").lower()
    if u in ("m", "million"): v *= 1e6
    elif u in ("k", "thousand"): v *= 1e3
    elif u in ("b", "billion"): v *= 1e9
    return int(v)

def clauses(t):
    return [c.strip() for c in re.split(r";|\.\s+(?=[A-Z])|\n", t) if c.strip()]

def extract(r):
    t = r.get("eligibility") or ""
    out = dict(inc=None, forprofit=None, emp_min=None, emp_max=None, rev_min=None, rev_max=None, yrs_min=None,
               pct=None, stack=None, pre=None, multi=False, src="auto")
    out["multi"] = bool(re.search(r"\b(streams?|tracks?|tiers?|components?)\b", t, re.I))
    for c in clauses(t):
        if GUARD.search(c):
            continue
        # employees
        m = re.search(r"(\d[\d,]*)\s*(?:to|-|–)\s*<?\s*(\d[\d,]*)\s*" + EMPW, c, re.I)
        if m:
            out["emp_min"] = out["emp_min"] or num(m.group(1)); out["emp_max"] = out["emp_max"] or num(m.group(2)) - (1 if "<" in m.group(0) else 0)
        m = re.search(r"(?:fewer than|less than|under)\s+(\d[\d,]*)\s*" + EMPW, c, re.I)
        if m and out["emp_max"] is None: out["emp_max"] = num(m.group(1)) - 1
        m = re.search(r"(?:up to|no more than|maximum of|a maximum of)\s+(\d[\d,]*)\s*" + EMPW, c, re.I) or \
            re.search(r"(\d[\d,]*)\s+or fewer\s*" + EMPW, c, re.I) or re.search(r"(\d[\d,]*)\s*" + EMPW + r"\s+or (?:fewer|less)", c, re.I)
        if m and out["emp_max"] is None: out["emp_max"] = num(m.group(1))
        m = re.search(r"at least\s+(\d+|one|two|three|four|five|ten)\s*" + EMPW, c, re.I) or re.search(r"(\d+)\+\s*" + EMPW, c, re.I)
        if m and out["emp_min"] is None: out["emp_min"] = num(m.group(1))
        # revenue
        m = re.search(r"\$(\d[\d,.]*)\s*(million|M|K|thousand)?\s*(?:to|-|–)\s*\$(\d[\d,.]*)\s*(million|M|K|billion|B)?\s*(?:in\s+)?(?:annual|gross|consolidated)?\s*(?:annual\s+)?(?:revenue|sales)", c, re.I)
        if m:
            out["rev_min"] = money(m.group(1), m.group(2) or m.group(4)); out["rev_max"] = money(m.group(3), m.group(4))
        m = re.search(r"(?:at least|over|more than|minimum of)\s+\$(\d[\d,.]*)\s*(million|M|K|thousand)?\s*(?:in\s+)?(?:annual|gross)?\s*(?:annual\s+)?(?:revenue|sales)", c, re.I) or \
            re.search(r"(?:revenues?|sales)\s+(?:of\s+)?(?:at least|over|more than)\s+\$(\d[\d,.]*)\s*(million|M|K|thousand)?", c, re.I)
        if m and out["rev_min"] is None: out["rev_min"] = money(m.group(1), m.group(2))
        m = re.search(r"(?:revenues?|sales)\s+of\s+\$(\d[\d,.]*)\s*(million|M|K)?\s+or less", c, re.I) or \
            re.search(r"(?:under|less than|below)\s+\$(\d[\d,.]*)\s*(million|M|K)?\s*(?:in\s+)?(?:annual\s+)?(?:gross\s+)?(?:revenue|sales)", c, re.I)
        if m and out["rev_max"] is None: out["rev_max"] = money(m.group(1), m.group(2))
        # years operating
        m = re.search(r"at least\s+(?:the past\s+)?(\d+|one|two|three|four|five)\s+(years?|months?)\s+(?:of\s+)?(?:operation|operating|in operation|in business|of operations)", c, re.I) or \
            re.search(r"in (?:business|operation)\s+(?:for\s+)?at least\s+(\d+|one|two|three|four|five)\s+(years?|months?)", c, re.I) or \
            re.search(r"(\d+)\+\s*(years?|months?)\s+(?:operating|in business|of operation)", c, re.I) or \
            re.search(r"(\d+|one|two|three)\s+(years?|months?)\s+(?:of\s+)?operating history", c, re.I) or \
            re.search(r"(?:incorporated|registered)[^,]*?for at least the past\s+(\d+|one|two|three|four|five)\s+(years?)", c, re.I) or \
            re.search(r"operating\s+(\d+|one|two|three)\+?\s+(months?|years?)", c, re.I)
        if m and out["yrs_min"] is None:
            n = num(m.group(1)); out["yrs_min"] = round(n / 12, 2) if m.group(2).lower().startswith("month") else n
    # minimum project size (stated plainly)
    for c in clauses(t):
        if re.search(r"gross commodity income|per (?:farm|applicant)", c, re.I):
            continue
        m = re.search(r"(?:total eligible (?:project )?costs of at least|at least|minimum project(?: size)?(?: of)?|minimum of)\s+\$(\d[\d,.]*)\s*(million|M|K)?\s*(?:in\s+)?(?:eligible (?:costs|expenses)|total investment|project investment|eligible project costs)?", c, re.I)
        if m and re.search(r"project|eligible (?:costs|expenses)|investment", c, re.I) and not re.search(r"revenue|sales|income", c[max(0, m.start() - 5):m.end() + 25], re.I):
            v = money(m.group(1), m.group(2))
            if v >= 20000 and out.get("proj_min") is None and not GUARD.search(c):
                out["proj_min"] = v
    tl = t.lower()
    # legal form
    if re.search(r"\bincorporated\b", tl) and not re.search(r"unincorporated|sole proprietor(?!ships? (?:or|and) (?:llps|partnerships) (?:are )?(?:not|in))|or registered|registered or incorporated|incorporated or registered|individuals|self-employed|partnership", tl):
        out["inc"] = True
    if re.search(r"no sole proprietorships|sole proprietorships?(?:,| and| or)[^.]*?(?:are )?(?:ineligible|not eligible)", tl):
        out["inc"] = True
    ap = set(r.get("applicant_types") or [])
    if ap and ap <= {"Non-profit", "Co-operative", "Social enterprise"} and "Non-profit" in ap:
        out["forprofit"] = False
    elif re.search(r"\bfor-profit\b", tl) and not re.search(r"not-for-profit|non-profit|nonprofit", tl):
        out["forprofit"] = True
    cs = (r.get("cost_share") or "")
    m = re.search(r"up to\s+(\d+(?:\.\d+)?)\s*%", cs, re.I) or re.search(r"(\d+(?:\.\d+)?)\s*%\s+of\s+(?:eligible|total|capital)", cs, re.I)
    if m: out["pct"] = float(m.group(1))
    elif re.search(r"two-thirds", cs, re.I): out["pct"] = 66.7
    m = re.search(r"(?:total government funding|stacking)[^%]{0,40}?(\d+)\s*%", cs + " " + (r.get("notes") or "") + " " + t, re.I)
    if m: out["stack"] = int(m.group(1))
    ft = set(r.get("funding_types") or [])
    if ft & {"Grant", "Repayable contribution", "Voucher", "Wage subsidy"} and not ft & {"Tax credit"}:
        out["pre"] = True   # usually only costs after approval are eligible: shown as a check, never a knock-out
    return out

# Manual overrides, checked against the official pages listed (Nov 2026).
OVERRIDES = {
    "CanExport SMEs": dict(inc=True, forprofit=True, emp_min=3, emp_max=500, rev_min=300000, rev_max=100000000, pct=50, stack=75, pre=True),
    "NRC IRAP": dict(inc=True, forprofit=True, emp_max=500, pre=True),
    "Scientific Research and Experimental Development": dict(inc=None, forprofit=True, pre=False),
}

def main():
    recs = json.load(open(DATA, encoding="utf-8"))
    cp = os.path.join(HERE, "redteam_corrections_v2.json")
    global CORR
    CORR = json.load(open(cp, encoding="utf-8")) if os.path.exists(cp) else {}
    rules = {}
    for r in recs:
        x = extract(r)
        for k, ov in OVERRIDES.items():
            if r["name"].startswith(k) or k in r["name"]:
                x.update(ov); x["src"] = "manual"
        for batch, fixes in CORR.items():
            if batch.startswith("_") or r["id"] not in fixes: continue
            for k, v in fixes[r["id"]].items():
                if v is None: x[k] = None
                else: x[k] = v
            x["src"] = "redteam"
        # sanity: discard impossible ranges
        if x["emp_min"] and x["emp_max"] and x["emp_min"] > x["emp_max"]: x["emp_min"] = x["emp_max"] = None
        if x["rev_min"] and x["rev_max"] and x["rev_min"] > x["rev_max"]: x["rev_min"] = x["rev_max"] = None
        rules[r["id"]] = {k: v for k, v in x.items() if v is not None and (v is not False or k == "forprofit")}
    json.dump(rules, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    keys = ["proj_min", "inc", "forprofit", "emp_min", "emp_max", "rev_min", "rev_max", "yrs_min", "pct", "stack", "pre", "multi"]
    print({k: sum(1 for v in rules.values() if k in v) for k in keys})

if __name__ == "__main__":
    main()
