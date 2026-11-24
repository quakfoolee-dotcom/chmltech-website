"""Put the "AI" dropdown (AI Models, AI Tools Landscape) into the main menu of every page (V5.78).

Also adds "AI tools landscape" to the footer's Explore column. Replaces the plain "AI Models" menu link, or an earlier copy of the dropdown, in every HTML page that has the site
header. Pages in sub-folders (post/, exams/...) get "../" links. The current page is marked: llm-leaderboard.html
marks AI Models, ai-tools.html marks AI Tools Landscape; on both the "AI" button is marked as the current section.
Styles: the "AI" dropdown block in assets/css/styles.css; behaviour: assets/js/main.js.
Safe to run any number of times. New pages copy their header from existing pages, so they inherit the dropdown.

Run from the site root: python3 content/gen/nav_ai_dropdown.py .   (then content/gen/seo_pass.py .)
"""
import json, os, re, sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
DATA = os.path.join(ROOT, "assets", "data", "ai-tools.json")


def markup(prefix, current, n):
    cur_btn = ' aria-current="page"' if current else ""
    m = ' aria-current="page"' if current == "models" else ""
    t = ' aria-current="page"' if current == "tools" else ""
    return ('<div class="nav-dd" data-nav-dd><button type="button" class="nav-dd-btn" aria-expanded="false" aria-controls="nav-dd-ai"' + cur_btn + '>AI'
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>'
            '<div class="nav-dd-menu" id="nav-dd-ai">'
            f'<a href="{prefix}llm-leaderboard"{m}><strong>AI Models</strong><span>LLM leaderboard: scores and cost</span></a>'
            f'<a href="{prefix}ai-tools"{t}><strong>AI Tools Landscape</strong><span>{n:,} tools mapped, with cost per output</span></a>'
            '</div></div>')


OLD_LINK = re.compile(r'<a href="((?:\.\./)*)llm-leaderboard(?:\.html)?"(?: aria-current="page")?>AI Models</a>')
OLD_DD = re.compile(r'<div class="nav-dd" data-nav-dd>.*?</div></div>', re.S)


def main():
    n = len(json.load(open(DATA, encoding="utf-8"))["tools"])
    changed = 0
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "WMS_demo", "wms_demo", "content")]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dirpath, f)
            s = open(p, encoding="utf-8").read()
            if 'id="site-nav"' not in s:
                continue
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            current = "models" if rel == "llm-leaderboard.html" else "tools" if rel == "ai-tools.html" else None
            prefix = "../" * rel.count("/")
            new = markup(prefix, current, n)
            out = OLD_DD.sub(lambda m: new, s, count=1) if OLD_DD.search(s) else OLD_LINK.sub(lambda m: new, s, count=1)
            # footer "Explore" column: link the landscape next to the funding finder
            fin = f'<a href="{prefix}funding">Funding finder</a>'
            if fin in out and f'<a href="{prefix}ai-tools">AI tools landscape</a>' not in out:
                out = out.replace(fin, fin + f'\n      <a href="{prefix}ai-tools">AI tools landscape</a>', 1)
            if out != s:
                open(p, "w", encoding="utf-8").write(out); changed += 1
    print(f"AI dropdown written in {changed} pages")


if __name__ == "__main__":
    main()
