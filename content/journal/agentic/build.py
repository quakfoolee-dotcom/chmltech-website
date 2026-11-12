"""Write the three agentic AI journal papers, Vol. 105, Issues 4-6 (V4.61), to content/journal/<slug>.json and check them.

Usage: python3 -I content/journal/agentic/build.py
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import jmark

JDIR = os.path.join(HERE, "..")
FIGS = os.path.join(JDIR, "figures")
PAPERS = ["paper_v105_i4", "paper_v105_i5", "paper_v105_i6"]
DATE = "2026-11-12"
AUTHOR = {"name": "Quak Foo Lee", "role": "Chief Technology Officer", "org": "Chmltech Ltd.",
          "division": "Division of Artificial Intelligence and Machine Learning", "location": "Vancouver, BC, Canada"}
ALLOWED = {"sub", "sup", "em", "strong", "i", "b"}


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def texts(d):
    yield d["abstract"]
    for s in d["sections"]:
        yield s["title"]
        for b in s["blocks"]:
            for k in ("p", "h3", "eq"):
                if k in b: yield b[k]
            if "list" in b: yield from b["list"]
            if "table" in b:
                t = b["table"]; yield t["caption"]; yield t.get("note", "")
                for r in [t["head"]] + t["rows"]: yield from r
            if "fig" in b: yield b["fig"]["caption"]; yield b["fig"]["source"]
    for r in d["references"]: yield r["text"]


def check(d):
    errs = []
    body = " ".join(texts(d))
    for tag in set(re.findall(r"</?([a-zA-Z0-9]+)", body)):
        if tag not in ALLOWED: errs.append(f"HTML tag not allowed: <{tag}>")
    if "[@" in body: errs.append("unresolved citation key")
    w = jmark.words(d["sections"]) + len(d["abstract"].split())
    if not 3000 <= w <= 4800: errs.append(f"body words {w} outside 3,000-4,800")
    if not 150 <= len(d["abstract"].split()) <= 250: errs.append(f"abstract {len(d['abstract'].split())} words")
    if not 120 <= len(d["meta"]) <= 170: errs.append(f"meta {len(d['meta'])} chars")
    if len(d["short_title"]) > 60: errs.append("short_title too long")
    if not 5 <= len(d["keywords"]) <= 8: errs.append("keywords count")
    if not 12 <= len(d["references"]) <= 30: errs.append(f"{len(d['references'])} references")
    paras = " ".join(b.get("p", "") + " ".join(b.get("list", [])) for s in d["sections"] for b in s["blocks"])
    blocks = [b for s in d["sections"] for b in s["blocks"]]
    for kind, word in (("fig", "Figure"), ("table", "Table")):
        ns = [b[kind]["n"] for b in blocks if kind in b]
        if ns != list(range(1, len(ns) + 1)): errs.append(f"{kind} numbering {ns}")
        for n in ns:
            if not re.search(rf"\b{word} {n}\b", paras): errs.append(f"{word} {n} not referred to in the text")
    eqs = [b["n"] for b in blocks if "eq" in b]
    for n in eqs:
        if f"Eq. ({n})" not in paras: errs.append(f"Eq. ({n}) not referred to")
    for b in blocks:
        if "fig" in b:
            F = b["fig"]
            if len(F["alt"]) < 40: errs.append(f"alt text short for {F['id']}")
            if not os.path.exists(os.path.join(FIGS, d["slug"], F["id"] + ".svg")): errs.append(f"missing svg {F['id']}")
    cited = set()
    for m in re.finditer(r"\[(\d+(?:\s*[,–]\s*\d+)*)\]", body):
        for part in re.split(r"\s*,\s*", m.group(1)):
            a, _, z = part.partition("–"); cited.update(range(int(a), int(z or a) + 1))
    if cited != set(range(1, len(d["references"]) + 1)): errs.append(f"citations {sorted(cited)} vs {len(d['references'])} references")
    return w, errs


def main():
    ok = True
    for name in PAPERS:
        m = load(name)
        sections = jmark.parse(m.BODY)
        refs = jmark.number_refs(sections, {k: {"text": t, "url": u} for k, (t, u) in m.REFS.items()})
        d = dict(slug=m.SLUG, **m.META, published=DATE, revised=DATE, author=AUTHOR, abstract=m.ABSTRACT,
                 sections=sections, references=refs, corrections=[])
        d = {k: d[k] for k in ["slug", "volume", "issue", "published", "revised", "title", "short_title", "meta", "author",
                               "abstract", "keywords", "sections", "references", "corrections"]}
        json.dump(d, open(os.path.join(JDIR, m.SLUG + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        w, errs = check(d)
        nf = sum(1 for s in sections for b in s["blocks"] if "fig" in b)
        nt = sum(1 for s in sections for b in s["blocks"] if "table" in b)
        ne = sum(1 for s in sections for b in s["blocks"] if "eq" in b)
        print(f"{d['volume']}({d['issue']}) {m.SLUG}: {w} words, {len(refs)} refs, {nf} figs, {nt} tables, {ne} eqs -> {'OK' if not errs else errs}")
        ok &= not errs
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
