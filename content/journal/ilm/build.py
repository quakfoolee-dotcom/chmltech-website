"""Write and check Vol. 106, Issues 16-18 (industrial LLMs for smart factory assessment and optimization; drafts V1, Nov 27 2026).

Usage: python3 -I content/journal/ilm/build.py [paper_v106_i16 ...]
Reuses the operations builder (content/journal/ops/build.py: TEX equations, CODE listings, DOWNLOADS) and the agentic checks.
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agentic"))
import jmark, build
spec = importlib.util.spec_from_file_location("opsbuild", os.path.join(HERE, "..", "ops", "build.py"))
ops = importlib.util.module_from_spec(spec); spec.loader.exec_module(ops)

PAPERS = ["paper_v106_i16", "paper_v106_i17", "paper_v106_i18"]
DATE = "2026-11-27"
AUTHOR = dict(build.AUTHOR, division="Division of Artificial Intelligence and Machine Learning")


def main(names):
    ok = True
    for name in names:
        sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
        mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
        sections = ops.parse(mod.BODY, getattr(mod, "CODE", {}))
        refs = jmark.number_refs(sections, {k: {"text": t, "url": u} for k, (t, u) in mod.REFS.items()})
        d = dict(slug=mod.SLUG, **mod.META, published=DATE, revised=DATE, author=AUTHOR, abstract=mod.ABSTRACT,
                 sections=sections, references=refs, corrections=[], downloads=getattr(mod, "DOWNLOADS", []))
        d = {k: d[k] for k in ["slug", "volume", "issue", "published", "revised", "title", "short_title", "meta", "author",
                               "abstract", "keywords", "sections", "references", "corrections", "downloads"]}
        json.dump(d, open(os.path.join(HERE, "..", mod.SLUG + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        w, errs = ops.check(d)
        cnt = lambda k: sum(1 for s in sections for b in s["blocks"] if k in b)
        print(f"{d['volume']}({d['issue']}) {mod.SLUG}: {w} words, {len(refs)} refs, {cnt('fig')} figs, {cnt('table')} tables, "
              f"{cnt('tex')} eqs, {cnt('code')} listings -> {'OK' if not errs else errs}")
        ok &= not errs
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:] or PAPERS)
