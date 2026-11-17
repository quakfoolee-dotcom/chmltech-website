"""Write and check the operations papers, Vol. 106, Issues 3-7 (V5.41, V5.42), to content/journal/<slug>.json.

Usage: python3 -I content/journal/ops/build.py
Reuses the markup and checks in content/journal/agentic/ (jmark.py, build.py) and adds two block types:
  TEX <latex>        numbered display equation in LaTeX, typeset by KaTeX on the page (journal_pages.py)
  DOWNLOADS (module) files in assets/journal/code/ offered on the page (V5.42)
  CODE <name>        program listing taken from the paper module's CODE[name] (kept outside the markup so blank lines survive)
"""
import importlib.util, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agentic"))
import jmark, build

PAPERS = ["paper_v106_i3", "paper_v106_i4", "paper_v106_i5", "paper_v106_i6", "paper_v106_i7"]
DATE = "2026-11-16"
AUTHOR = dict(build.AUTHOR, division="Division of Operational Excellence")
_parse = jmark.parse


def parse(src, code):
    """Pre-pass for TEX and CODE blocks, then the standard parser for the rest."""
    marks, out = {}, []
    for raw in re.split(r"\n\s*\n", src.strip()):
        r = raw.strip()
        if r.startswith("TEX ") or r.startswith("CODE "):
            key = f"ZZBLOCK{len(marks)}ZZ"; marks[key] = r; out.append(key)
        else: out.append(raw)
    secs = _parse("\n\n".join(out))
    eq = 0
    for s in secs:
        nb = []
        for b in s["blocks"]:
            if "eq" in b: eq += 1; b["n"] = eq
            k = b.get("p", "")
            if k in marks:
                r = marks[k]
                if r.startswith("TEX "): eq += 1; b = {"tex": " ".join(r[4:].split()), "n": eq}
                else:
                    name, _, cap = r[5:].partition("||")
                    b = {"code": code[name.strip()]}
                    if cap.strip(): b["caption"] = jmark.inline(cap.strip())
            nb.append(b)
        s["blocks"] = nb
    return secs


def check(d):
    w, errs = build.check(d)
    paras = " ".join(b.get("p", "") + " ".join(b.get("list", [])) for s in d["sections"] for b in s["blocks"])
    for b in (b for s in d["sections"] for b in s["blocks"]):
        if "tex" in b and f"Eq. ({b['n']})" not in paras: errs.append(f"Eq. ({b['n']}) not referred to")
    return w, errs


def main():
    ok = True
    for name in PAPERS:
        spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        sections = parse(mod.BODY, getattr(mod, "CODE", {}))
        refs = jmark.number_refs(sections, {k: {"text": t, "url": u} for k, (t, u) in mod.REFS.items()})
        d = dict(slug=mod.SLUG, **mod.META, published=DATE, revised=DATE, author=AUTHOR, abstract=mod.ABSTRACT,
                 sections=sections, references=refs, corrections=getattr(mod, "CORRECTIONS", []),
                 downloads=getattr(mod, "DOWNLOADS", []))
        if getattr(mod, "REVISED", None): d["revised"] = mod.REVISED
        d = {k: d[k] for k in ["slug", "volume", "issue", "published", "revised", "title", "short_title", "meta", "author",
                               "abstract", "keywords", "sections", "references", "corrections", "downloads"]}
        for f in d["downloads"]:
            if not os.path.exists(os.path.join(HERE, "..", "..", "..", "assets", "journal", "code", f["file"])):
                raise SystemExit(f"missing download {f['file']}")
        json.dump(d, open(os.path.join(HERE, "..", mod.SLUG + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        w, errs = check(d)
        cnt = lambda k: sum(1 for s in sections for b in s["blocks"] if k in b)
        print(f"{d['volume']}({d['issue']}) {mod.SLUG}: {w} words, {len(refs)} refs, {cnt('fig')} figs, {cnt('table')} tables, "
              f"{cnt('tex') + cnt('eq')} eqs, {cnt('code')} listings -> {'OK' if not errs else errs}")
        ok &= not errs
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
