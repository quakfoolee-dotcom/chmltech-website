"""Write and check Vol. 106, Issues 19-23 (process and operations papers under uncertainty, Nov 27 2026).

Usage: python3 -I content/journal/proc/build.py [paper_v106_i19 ...]
Reuses the operations builder (content/journal/ops/build.py: TEX equations, CODE listings, DOWNLOADS) and the agentic checks.
  i19 Critical spare parts            i20 Cost contingency by Monte Carlo     i21 Feed preheater under fouling
  i22 AI agent calculation benchmark  i23 Hybrid digital twins for fouling
Models and downloadable code in content/journal/proc/models/<name>/.
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agentic"))
import jmark, build
spec = importlib.util.spec_from_file_location("opsbuild", os.path.join(HERE, "..", "ops", "build.py"))
ops = importlib.util.module_from_spec(spec); spec.loader.exec_module(ops)

PAPERS = ["paper_v106_i19", "paper_v106_i20", "paper_v106_i21", "paper_v106_i22", "paper_v106_i23"]
DATE = "2026-11-27"
AUTHOR = dict(build.AUTHOR, division="Division of Clean Energy Technology Innovation")
ASSETS = os.path.join(HERE, "..", "..", "..", "assets", "journal", "code")


def main(names):
    ok = True
    for name in names:
        sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
        mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
        sections = ops.parse(mod.BODY, getattr(mod, "CODE", {}))
        refs = jmark.number_refs(sections, {k: {"text": t, "url": u} for k, (t, u) in mod.REFS.items()})
        d = dict(slug=mod.SLUG, **mod.META, published=DATE, revised=DATE,
                 author=dict(AUTHOR, division=getattr(mod, "DIVISION", AUTHOR["division"])), abstract=mod.ABSTRACT,
                 sections=sections, references=refs, corrections=[], downloads=getattr(mod, "DOWNLOADS", []))
        d = {k: d[k] for k in ["slug", "volume", "issue", "published", "revised", "title", "short_title", "meta", "author",
                               "abstract", "keywords", "sections", "references", "corrections", "downloads"]}
        for f in d["downloads"]:
            if not os.path.exists(os.path.join(ASSETS, f["file"])): raise SystemExit(f"missing download {f['file']}")
        json.dump(d, open(os.path.join(HERE, "..", mod.SLUG + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        w, errs = ops.check(d)
        cnt = lambda k: sum(1 for s in sections for b in s["blocks"] if k in b)
        print(f"{d['volume']}({d['issue']}) {mod.SLUG}: {w} words, {len(refs)} refs, {cnt('fig')} figs, {cnt('table')} tables, "
              f"{cnt('tex') + cnt('eq')} eqs, {cnt('code')} listings -> {'OK' if not errs else errs}")
        ok &= not errs
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:] or PAPERS)
