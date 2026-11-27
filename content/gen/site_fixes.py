"""Small sitewide fixes applied on every build (V5.82). Run by seo_pass.py before the page loop.

1. Plain email links. Pages used to print "info [at] chmltech [dot] com" in a js-mail link that
   assets/js/main.js rebuilt into a mailto link after load. Crawlers that do not run scripts
   (Brave, AI assistants) saw the "[at]" text, and the plain address is in the JSON-LD on every
   page anyway, so the hiding protected nothing. The link is now a normal mailto link.
   New pages that copy an old header or footer are fixed at the next build.

Library exams (exams/) and the WMS demo (WMS_demo/) are not touched.
"""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
JS_MAIL = re.compile(r'<a class="js-mail" href="[^"]*" data-u="([a-z0-9._-]+)" data-d="([a-z0-9.-]+)"'
                     r'(?: data-q="([^"]*)")?>[^<]*</a>')


def mail_link(m):
    addr = f"{m.group(1)}@{m.group(2)}"
    q = f"?{m.group(3)}" if m.group(3) else ""
    return f'<a href="mailto:{addr}{q}">{addr}</a>'


def run(root=ROOT):
    n = 0
    for d, dirs, files in os.walk(root):
        rel_d = os.path.relpath(d, root)
        if rel_d.split(os.sep)[0] in (".git", "exams", "WMS_demo", "wms_demo", "node_modules"):
            dirs[:] = []
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(d, f)
            s = open(p, encoding="utf-8").read()
            if "js-mail" not in s:
                continue
            new = JS_MAIL.sub(mail_link, s)
            if new != s:
                open(p, "w", encoding="utf-8").write(new)
                n += 1
    return n


if __name__ == "__main__":
    print(run())
