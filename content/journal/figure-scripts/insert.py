"""Place figures into a journal paper JSON (idempotent).
Each spec: section num, insert_after block index (in the paper as it is WITHOUT figures), the fig dict,
and the paragraph (section num, block index) that receives the text reference sentence."""
import json, sys

def apply(path, specs):
    d = json.load(open(path))
    for s in d["sections"]:                       # remove any previous figures first
        s["blocks"] = [b for b in s["blocks"] if "fig" not in b]
    for sp in specs:                              # add reference sentences (once)
        sec = next(s for s in d["sections"] if s["num"] == sp["ref"][0]); b = sec["blocks"][sp["ref"][1]]
        assert "p" in b, ("reference target is not a paragraph", sp["fig"]["id"])
        if sp["sentence"] not in b["p"]: b["p"] = b["p"].rstrip() + " " + sp["sentence"]
    for sp in sorted(specs, key=lambda x: (-int(x["sec"]), -x["after"])):   # insert from the end so indices stay valid
        sec = next(s for s in d["sections"] if s["num"] == sp["sec"])
        sec["blocks"].insert(sp["after"] + 1, {"fig": sp["fig"]})
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
