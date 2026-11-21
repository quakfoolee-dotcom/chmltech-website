"""Write and check Vol. 106, Issues 10-15: the Multi-Agent AI Engineering series, Articles 2-7 (V5.62).

Usage: python3 -I content/journal/agentic/build_v106_mae.py [paper_v106_i10 ...]
Uses the operations builder's parser (content/journal/ops/build.py: TEX equations and CODE listings) and the agentic
checks. Each paper's interactive figure is named in LIVE: its fig block gets "live": <name>, which inserts
content/journal/live/<name>.html (drawn by content/journal/figure-scripts/mae_figs.py, which also writes the static SVG).
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import jmark, build
spec = importlib.util.spec_from_file_location("opsbuild", os.path.join(HERE, "..", "ops", "build.py"))
opsbuild = importlib.util.module_from_spec(spec); spec.loader.exec_module(opsbuild)

PAPERS = ["paper_v106_i10", "paper_v106_i11", "paper_v106_i12", "paper_v106_i13", "paper_v106_i14", "paper_v106_i15"]
DATE = "2026-11-21"
LIVE = {"fig1-patterns": "mae2", "fig1-gates": "mae3", "fig1-roles": "mae4", "fig3-action-states": "mae5",
        "fig1-skill-lifecycle": "mae6", "fig1-run": "mae7"}


def main(names):
    ok = True
    for name in names:
        sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
        mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
        sections = opsbuild.parse(mod.BODY, getattr(mod, "CODE", {}))
        for s in sections:
            for b in s["blocks"]:
                if "fig" in b and b["fig"]["id"] in LIVE: b["fig"]["live"] = LIVE[b["fig"]["id"]]
        refs = jmark.number_refs(sections, {k: {"text": t, "url": u} for k, (t, u) in mod.REFS.items()})
        d = dict(slug=mod.SLUG, **mod.META, published=getattr(mod, "PUBLISHED", DATE), revised=getattr(mod, "PUBLISHED", DATE),
                 author=build.AUTHOR, abstract=mod.ABSTRACT, sections=sections, references=refs, corrections=[], downloads=[])
        d = {k: d[k] for k in ["slug", "volume", "issue", "published", "revised", "title", "short_title", "meta", "author",
                               "abstract", "keywords", "sections", "references", "corrections", "downloads"]}
        json.dump(d, open(os.path.join(HERE, "..", mod.SLUG + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        w, errs = opsbuild.check(d)
        cnt = lambda k: sum(1 for s in sections for b in s["blocks"] if k in b)
        print(f"{d['volume']}({d['issue']}) {mod.SLUG[:60]}: {w} words, {len(refs)} refs, {cnt('fig')} figs, {cnt('table')} tables, "
              f"{cnt('tex') + cnt('eq')} eqs, {cnt('code')} listings -> {'OK' if not errs else errs}")
        ok &= not errs
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:] or PAPERS) else 1)
