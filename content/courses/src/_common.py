"""Shared helpers for course source files in content/courses/src/."""
import json
import os
from collections import Counter


def step(title, minutes, body, takeaways, apply, q, opts, a, why):
    return dict(title=title, minutes=minutes, body=" ".join(body.split("\n")).strip(), takeaways=takeaways, apply=apply,
                check=dict(q=q, opts=opts, a=a, why=why))


def E(q, opts, a, why):
    return dict(q=q, opts=opts, a=a, why=why)


def balance_checks(course):
    """Move each knowledge check's correct option so answers cycle evenly through positions 0-3."""
    i = 0
    for m in course["modules"]:
        for st in m["steps"]:
            ch = st["check"]
            if len(ch["opts"]) == 4:
                correct = ch["opts"].pop(ch["a"])
                t = i % 4
                ch["opts"].insert(t, correct)
                ch["a"] = t
            i += 1


def write(course, name, src_file, balance=False):
    if balance:
        balance_checks(course)
    here = os.path.dirname(os.path.abspath(src_file))
    out = os.path.join(os.path.dirname(here), name + ".json")
    json.dump(course, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n = sum(len(m["steps"]) for m in course["modules"])
    print(name, "lessons", n, "exam", len(course["exam"]), dict(sorted(Counter(q["a"] for q in course["exam"]).items())),
          "checks", dict(sorted(Counter(s["check"]["a"] for m in course["modules"] for s in m["steps"]).items())),
          "minutes", sum(s["minutes"] for m in course["modules"] for s in m["steps"]))
