"""Tiny markup for writing Chmltech Online Journal papers as text (V4.61), converted to the JSON in content/journal/SPEC.md.

Markup, one block per paragraph (blocks separated by a blank line):
  ## Title                 new numbered section (numbers assigned in order)
  ### 2.1 Title            subsection heading
  - item / 1. item         bullet / ordered list (one item per line)
  EQ <html>                numbered equation (numbers assigned in order)
  TABLE <caption> || <note>   followed by pipe rows; first row is the header
  FIG <id> || <caption> || <alt> || <source>   figure (numbers assigned in order)
  CALLOUT <text>           key-point box (at most 3 per paper; V4.67)
  anything else            a paragraph
Inline: **bold**, *italic*, citations [@key] or [@a, @b]. References are numbered in order of first citation
in the body, and consecutive numbers are written as ranges (3–6).
"""
import re


def inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def parse(src):
    sections, eq_n, tab_n, fig_n = [], 0, 0, 0
    for raw in [b.strip("\n") for b in re.split(r"\n\s*\n", src.strip())]:
        if not raw.strip(): continue
        if raw.startswith("## "):
            sections.append({"num": str(len(sections) + 1), "title": inline(raw[3:].strip()), "blocks": []}); continue
        blocks = sections[-1]["blocks"]
        lines = raw.split("\n")
        if raw.startswith("### "):
            blocks.append({"h3": inline(raw[4:].strip())})
        elif raw.startswith("EQ "):
            eq_n += 1; blocks.append({"eq": raw[3:].strip(), "n": eq_n})
        elif raw.startswith("TABLE "):
            tab_n += 1
            cap, _, note = lines[0][6:].partition("||")
            rows = [[inline(c.strip()) for c in ln.strip().strip("|").split("|")] for ln in lines[1:]]
            t = {"n": tab_n, "caption": inline(cap.strip()), "head": rows[0], "rows": rows[1:]}
            if note.strip(): t["note"] = inline(note.strip())
            blocks.append({"table": t})
        elif raw.startswith("CALLOUT "):
            blocks.append({"callout": inline(" ".join(ln.strip() for ln in lines)[8:].strip())})
        elif raw.startswith("FIG "):
            fig_n += 1
            fid, cap, alt, srcl = [x.strip() for x in raw[4:].split("||")]
            blocks.append({"fig": {"n": fig_n, "id": fid, "caption": inline(cap), "alt": alt, "source": inline(srcl)}})
        elif all(re.match(r"- ", ln) for ln in lines):
            blocks.append({"list": [inline(ln[2:].strip()) for ln in lines], "ordered": False})
        elif all(re.match(r"\d+\. ", ln) for ln in lines):
            blocks.append({"list": [inline(re.sub(r"^\d+\. ", "", ln).strip()) for ln in lines], "ordered": True})
        else:
            blocks.append({"p": inline(" ".join(ln.strip() for ln in lines))})
    return sections


def _ranges(nums):
    nums = sorted(set(nums)); out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ", ".join(str(x) for x in nums[i:j + 1]))
        i = j + 1
    return ", ".join(out)


def number_refs(sections, refs):
    """Replace [@key] citations with numbers in order of first use; return the ordered reference list."""
    order = []
    def walk(fn):
        for s in sections:
            for b in s["blocks"]:
                for k in ("p", "callout"):
                    if k in b: b[k] = fn(b[k])
                if "list" in b: b["list"] = [fn(x) for x in b["list"]]
                if "table" in b:
                    t = b["table"]; t["rows"] = [[fn(c) for c in r] for r in t["rows"]]
                    if "note" in t: t["note"] = fn(t["note"])
                    t["caption"] = fn(t["caption"])
                if "fig" in b: b["fig"]["source"] = fn(b["fig"]["source"]); b["fig"]["caption"] = fn(b["fig"]["caption"])
    pat = re.compile(r"\[(@[\w-]+(?:\s*,\s*@[\w-]+)*)\]")
    def collect(t):
        for m in pat.finditer(t):
            for k in re.findall(r"@([\w-]+)", m.group(1)):
                if k not in refs: raise KeyError(f"unknown reference key: {k}")
                if k not in order: order.append(k)
        return t
    walk(collect)
    num = {k: i + 1 for i, k in enumerate(order)}
    walk(lambda t: pat.sub(lambda m: "[" + _ranges([num[k] for k in re.findall(r"@([\w-]+)", m.group(1))]) + "]", t))
    unused = [k for k in refs if k not in num]
    if unused: raise ValueError(f"references never cited: {unused}")
    return [refs[k] for k in order]


def words(sections):
    n = 0
    for s in sections:
        for b in s["blocks"]:
            if "p" in b: n += len(re.sub("<[^>]+>", "", b["p"]).split())
            if "list" in b: n += sum(len(x.split()) for x in b["list"])
    return n
