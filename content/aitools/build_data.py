"""Build the compact data file for the AI Tools Landscape page (ai-tools.html).

Input : content/aitools/source/ai_tools_V9.json   (the researched, reviewed catalogue; full fields)\n        content/aitools/public_text_overrides.json  (hand-written public wording per tool, applied last)
Output: assets/data/ai-tools.json                  (short keys, only what the page shows)

Run: python3 content/aitools/build_data.py   (from the site root), then content/gen/ai_tools_page.py, then seo_pass.py
"""
import json, os, re
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "source", "ai_tools_V9.json")
OUT = os.path.join(ROOT, "assets", "data", "ai-tools.json")
OVR_FILE = os.path.join(HERE, "public_text_overrides.json")

LAYERS = [
    ("L1", "Foundation Models & Assistants", "The model platforms and the general assistants built on them."),
    ("L2", "Builder Stack", "What developers use to build, run, test and secure AI applications and agents."),
    ("L3", "Agents & Automation", "Agents that do work, coding agents, voice agents and workflow automation."),
    ("L4", "Business Functions", "AI tools for sales, support, finance, HR, operations and the rest of the business."),
    ("L5", "Creative & Media", "Writing, images, video, voice, music, design and presentations."),
]
PM = {"free": "Free", "freemium": "Free plan + paid", "subscription": "Paid subscription", "usage": "Pay as you go",
      "open-source": "Open source", "open-core": "Open source + paid cloud", "enterprise": "Contact sales"}
DEP = {"saas": "Cloud (SaaS)", "api": "API", "self-hosted": "Self-hosted", "desktop": "Desktop app", "cli": "Command line",
       "ide-extension": "IDE extension", "browser-extension": "Browser extension", "mobile": "Mobile app"}


def domain(u):
    try:
        h = urlparse(u or "").hostname or ""
    except ValueError:
        return ""
    return re.sub(r"^www\.", "", h.lower())


# retired rows filed under a category that has since been renamed or merged -> the current category (for per-category churn)
OLD_CAT_NOW = {"Prompt Management": "Evaluation & Prompt Management", "Fine-tuning & Training": "Training, Fine-tuning & ML Frameworks",
               "Guardrails & AI Security": "Guardrails, AI Security & Governance"}
# retired statuses that are market events (acquired, renamed, sunsetting, shut down, folded in); "active" rows are list clean-ups
MARKET_EVENTS = ("shutdown", "merged", "acquired", "renamed", "sunsetting")

OLD_CAT_LAYER = {"Prompt Management": "L2", "Evaluation & Testing": "L2", "Fine-tuning & Training": "L2", "Guardrails & AI Security": "L2",
                 "Automation / Workflow": "L3", "Coding / Dev": "L3", "Prompt-Only Code Gen": "L3", "AI IDE": "L3", "Async AI Agent": "L3", "CLI AI Agent": "L3",
                 "SEO & Content": "L4", "Email / Inbox": "L4", "Meeting & Notes": "L4", "Finance & Legal": "L4", "Research": "L4",
                 "Brand / Creatives": "L5", "Writing & Content": "L5", "Presentation": "L5"}


def layer_of(cat, cmap):
    return cmap.get(cat) or OLD_CAT_LAYER.get(cat) or ""


INTERNAL = re.compile(r"\bred[ -]?team(?!ing)|v8 row|\bbudget\b|\(verify\)|\bverify\b|\bconfirm\b|not researched|egress|automated fetch|search budget|merged here|re-mapped|"
                      r"consolidates v8|research agent|previous list|\bv8\b|not re-?checked|separate row|combined row|see [^.;]*\brow\b|gap[ -]?list|prior knowledge|"
                      r"(?:repo|github) knowledge|not verified here|in this check|as read\b|bot check|from news|checked summary|consolidated here|homepage read|not tagged", re.I)
SUBS = [(re.compile(r"(?:not (?:shown|readable) )?(?:in|on) (?:the )?fetched page", re.I), "on the vendor's pricing page"),
        (re.compile(r"pricing page could not be fetched|pricing page disallows fetching|could not be fetched", re.I), "see the vendor's pricing page"),
        (re.compile(r"\s*\(WebFetch; curl blocked\)", re.I), ""),
        (re.compile(r"\(?(?:official )?(?:pricing page |site )?(?:could not be retrieved \()?(?:fetch|fetching) (?:failed|blocked)\)?(?:\s*\(\d+\))?", re.I), "see the vendor's pricing page"),
        (re.compile(r"(?:site |page )?blocked fetch(?:ing)?(?:\s*\(\d+\))?", re.I), "see the vendor's pricing page"),
        (re.compile(r"renders no text for fetching", re.I), "see the vendor's pricing page"),
        (re.compile(r"(?:the |a )?fetchable pages?", re.I), "the vendor's pricing page"),
        (re.compile(r"this pass|on page read", re.I), "at check time"),
        (re.compile(r"\bfetched\b", re.I), "checked"),
        (re.compile(r"\bpricing pricing page\b", re.I), "pricing page")]
# shared note fields where these words are research jargon (product names and descriptions may legitimately say "budgets" or "Fetch")
NOTE_ONLY = re.compile(r"\bbudget\b|fetch|\bcurl\b|\brow\b|(?:repo|github|prior) knowledge", re.I)
# the build fails if any of these reach the public file
BANNED = re.compile(r"\bred[ -]?team(?!ing)|per red-team|gap[ -]?list|prior knowledge|not re-?checked|previous list showed|in this check|as read\b|inferred by|"
                    r"see [^.;]*\brow\b|separate row|combined row|bot check|not verified here|prices from news|\bv8", re.I)


def public_text(s, field=""):
    """Research notes -> reader-facing text: drop sentences and brackets that are notes to the research team, soften tool-process wording."""
    if not s:
        return s
    if field == "can":
        s = re.sub(r"^SELF-HOST[^:]*:\s*", "", s, flags=re.I)  # SELF-HOST:, SELF-HOST/LOCAL:, SELF-HOST ONLY:, SELF-HOST (Enterprise): ...
    if field == "cbn" and s.startswith("Normalised:") and " | " in s:
        # "Normalised: $19 / 5,000 pages included x 1,000 = $3.8 per 1,000 pages (...) | Hobby $19 / 5,000 pages" -> one reader sentence
        calc, plan = s.split(" | ", 1)
        m = re.search(r"= \$([\d.,]+) (per [^(.|]+?)\s*(?:\(|\.|$)", calc)
        plan = plan.strip().rstrip(".")
        if m:
            v = float(m.group(1).replace(",", ""))
            val = f"${v:,.2f}" if 1 <= v < 100 and v % 1 else f"${v:,.0f}" if v >= 1 else f"${v:g}"
            s = f"{plan}: about {val} {m.group(2).strip()} at full use of the plan."
        else:
            m2 = re.search(r"rescaled to (per [^.(]+?) from", calc)
            s = plan + (f", shown {m2.group(1).strip()}." if m2 else ".")
    elif field == "cbn" and " | " in s:
        s = s.split(" | ", 1)[0].strip()  # the reader sentence comes first; the rest is the working
    s = re.sub(r"\s*\(([^()]*)\)", lambda m: "" if INTERNAL.search(m.group(1)) else m.group(0), s)  # internal asides in brackets
    parts = re.split(r"(?<=[.;])\s+|\s+-\s+(?=[A-Z])", s)
    keep = [p for p in parts if p and not INTERNAL.search(p)]
    out = " ".join(keep).strip(" ;-")
    for rx, rep in SUBS:
        out = rx.sub(rep, out)
    if out.count("(") > out.count(")"):
        out += ")"
    return out


def base_name(n):
    """'Phind (Coding/Dev duplicate)' -> 'phind': for matching the same product across entries."""
    return re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", "", n or "")).strip().lower()


ROW_MARKER = re.compile(r"\s*\([^)]*(?:duplicate|listing|\brow\b|entry)[^)]*\)", re.I)


def build():
    src = json.load(open(SRC, encoding="utf-8"))
    OVR = {k: v for k, v in json.load(open(OVR_FILE, encoding="utf-8")).items() if not k.startswith("_")}
    assert set(OVR) <= {r["id"] for r in src["tools"]}, set(OVR) - {r["id"] for r in src["tools"]}
    tools, cats = [], {}
    # domains shared by more than one vendor (github.com, huggingface.co ...) get no logo: a per-domain icon would be the host's, not the tool's
    vend = {}
    for r in src["tools"]:
        vend.setdefault(domain(r.get("website")), set()).add((r.get("vendor") or r["name"]).split(" (")[0].strip().lower())
    SHARED = {d for d, v in vend.items() if len(v) > 1} | {"github.com", "github.io", "huggingface.co", "pypi.org", "readthedocs.io", "gitlab.com"}
    for r in src["tools"]:
        for k in ("website", "pricing_source_url"):
            u = r.get(k)
            assert not u or urlparse(u).scheme == "https", (r["name"], k, u)
        for u in (r.get("canada_evidence_urls") or []) + (r.get("source_urls") or []):
            assert urlparse(u).scheme in ("https", "http"), (r["name"], u)
        lay = r["layer"].split(" ", 1)[0]
        cats.setdefault((lay, r["category"]), 0)
        cats[(lay, r["category"])] += 1
        ca = r.get("canada_data_residency") or "unknown"
        cev = [u for u in (r.get("canada_evidence_urls") or []) if u.startswith("https://")]
        if ca in ("yes", "self-host") and not cev:
            cev = [u for u in (r.get("source_urls") or []) if u.startswith("https://") and (ca == "self-host" and "github.com" in u or "canada" in u.lower() or "amazon-web-service" in u)]
            if not cev and ca == "yes":
                ca = "unknown"  # never show a Canada "yes" without evidence
        pm, oss = r.get("pricing_model") or "", bool(r.get("open_source"))
        lic = (r.get("license") or "")
        if pm in ("open-source", "open-core") and not oss and "source-available" not in lic.lower() and "elastic" not in lic.lower():
            oss = True
        if oss and pm not in ("open-source", "open-core"):
            pm = "open-core" if (r.get("entry_price_usd_month") or 0) > 0 or pm in ("subscription", "usage", "freemium", "enterprise") else "open-source"
        free = bool(r.get("free_tier")) or pm in ("free", "freemium", "open-source")
        t = {
            "id": r["id"], "n": r["name"], "v": r.get("vendor") or "", "l": lay, "c": r["category"],
            "c2": r.get("secondary_categories") or [], "d": r.get("description") or "", "u": r.get("website") or "",
            "dom": domain(r.get("website")), "logo": domain(r.get("website")) not in SHARED, "pm": pm, "free": free,
            "oss": oss, "lic": lic, "low": r.get("confidence") == "low",
            "dep": [x for x in (r.get("deployment") or []) if x in DEP],
            "pt": r.get("price_text") or "", "ep": r.get("entry_price_usd_month"),
            # pro (next paid tier) price: exported only for US-dollar prices, like the entry price is only used when cur == USD
            "pp": r.get("pro_price_usd_month") if (r.get("price_currency") or "USD") == "USD" and (r.get("pro_price_usd_month") or 0) > 0 else None,
            "bp": r.get("billing_period") or "unknown",
            "cur": r.get("price_currency") or "USD", "unit": r.get("unit_of_output") or "",
            "cpu": r.get("cost_per_unit_usd"), "cmp": bool(r.get("cost_comparable")), "cbn": r.get("cost_basis_note") or "",
            "promo": r.get("price_flag") == "promo",
            "fr": r.get("french_ui") or "unknown", "ca": ca, "can": r.get("canada_note") or "", "cav": bool(r.get("canadian_vendor")),
            "b": r.get("badge") or "", "sn": r.get("status_note") or "", "ch": r.get("change") or "",
            "ps": r.get("pricing_source_url") or "", "cs": cev[:3],
            "tags": r.get("use_case_tags") or [],
        }
        if not t["cmp"]:
            t["cpu"] = t["cpu"] if t["cur"] == "USD" else None
        for k in ("sn", "can", "cbn", "pt"):
            t[k] = public_text(t.get(k), k)
        if not t["b"]:
            t["sn"] = ""  # status notes are only shown with a badge (acquired, renamed, sunsetting)
        for k, v in OVR.get(t["id"], {}).items():  # hand-written public wording, applied last
            t[k] = v if v is not None else ""
        # "Yes, on some plans": Canadian hosting limited to certain plans, tiers or tenants (same rule as the detail drawer)
        t["cap"] = t["ca"] == "yes" and bool(re.search(r"enterprise|only|plan|eligible|tenant|standard and up", t["can"] or "", re.I))
        if t.get("cbn") == "Not comparable:":
            t["cbn"] = "Not comparable: the published price could not be turned into a cost per unit."
        tools.append({k: v for k, v in t.items() if v not in ("", [], None, False) or k in ("ep", "cpu", "free", "oss", "cmp", "cav", "logo", "low", "promo")})
    order = {k: i for i, (k, _, _) in enumerate(LAYERS)}
    catlist = sorted(cats, key=lambda x: (order[x[0]], x[1]))
    out = {
        "version": "V9", "as_of": "2026-11-23", "checked": "November 2026", "currency": "USD",
        "layers": [{"id": k, "name": n, "desc": d} for k, n, d in LAYERS],
        "categories": [{"l": l, "c": c, "n": cats[(l, c)]} for l, c in catlist],
        "pm": PM, "dep": DEP,
        "tools": sorted(tools, key=lambda t: (order[t["l"]], t["c"], t["n"].lower())),
        "retired": [dict(x, l=layer_of(x.get("category"), {c: l for l, c in catlist})) for x in src.get("retired", []) if x.get("name")],
    }
    # Retired entries. "cc": current category. "ev": a market event (acquired, renamed, sunsetting, shut down or folded in) that is
    # counted as a vendor change and listed under "Recently retired". Not events: list clean-ups (status "active": duplicates, not AI
    # products, out of scope) and any entry for the same product as a current tool or an earlier-kept event (base name match), so a
    # product is never counted twice. "prev": the entry was on the previous published list. "pn": the public name.
    now = {c for _, c in catlist}
    cur_names = {base_name(t["n"]) for t in tools}
    seen_ev = set()
    for x in out["retired"]:
        cc = OLD_CAT_NOW.get(x.get("category"), x.get("category"))
        if cc in now:
            x["cc"] = cc
        b = base_name(x["name"])
        x["ev"] = x.get("status") in MARKET_EVENTS and not ROW_MARKER.search(x["name"]) and b not in cur_names and b not in seen_ev
        if x["ev"]:
            seen_ev.add(b)
        x["pn"] = ROW_MARKER.sub("", x["name"]).strip()
        x["name"] = x["pn"]  # no internal row markers in the public file
        x["prev"] = bool(x.pop("v8_row", None))
        x.pop("category", None)
    assert all(x.get("cc") for x in out["retired"] if x["ev"]), [x["name"] for x in out["retired"] if x["ev"] and not x.get("cc")]
    assert all(OLD_CAT_NOW[k] in now for k in OLD_CAT_NOW)
    # public wording for the "Recently retired" list: research notes stay in the source files, the page shows a standard reason
    PUBLIC = {"shutdown": "Shut down", "merged": "Folded into another product", "acquired": "Acquired and folded into the buyer's products",
              "renamed": "Renamed; listed under its new name", "sunsetting": "Being retired by its vendor"}
    for x in out["retired"]:
        x["reason"] = PUBLIC.get(x.get("status")) if x["ev"] else "Removed as a duplicate or in list clean-up"
        for k in ("status_note", "rt_removal_reason", "source_urls"):
            x.pop(k, None)
    prev_removed = sum(1 for x in out["retired"] if x["prev"])
    out["flow"] = {"prev_total": sum(t["ch"] in ("kept", "updated") for t in tools) + prev_removed, "kept": sum(t["ch"] == "kept" for t in tools),
                   "updated": sum(t["ch"] == "updated" for t in tools), "prev_removed": prev_removed,
                   "prev_removed_ev": sum(1 for x in out["retired"] if x["prev"] and x["ev"]), "new": sum(t["ch"] == "new" for t in tools), "total": len(tools)}
    assert out["flow"]["prev_total"] == 475, out["flow"]  # the previous published list had 475 entries
    out.pop("version", None)
    # final public-wording gate: fail loudly if internal research wording reaches the public file
    hits = []
    def scan(obj, path, note):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if BANNED.search(k):
                    hits.append((path + "." + k, "key"))
                scan(v, path + "." + k, k in ("sn", "can", "cbn", "pt", "reason"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                scan(v, f"{path}[{i}]", note)
        elif isinstance(obj, str):
            if BANNED.search(obj) or (note and NOTE_ONLY.search(obj)):
                hits.append((path, obj))
    scan(out, "", False)
    assert not hits, "internal wording in the public data:\n" + "\n".join(f"  {p}: {v[:140]}" for p, v in hits)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"wrote {OUT}: {len(tools)} tools, {len(catlist)} categories, {os.path.getsize(OUT)//1024} KB")


if __name__ == "__main__":
    build()
