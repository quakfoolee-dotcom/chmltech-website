"""Cache-busting for stylesheets and scripts (V4.65).

Every link to assets/css/*.css or assets/js/*.js gets ?v=<first 8 hex of the file's MD5>, so a browser fetches the
file again as soon as its content changes and keeps its cached copy otherwise. stamp_all() runs at the end of
seo_pass.py, after every build. Generators that read an existing page as a template call strip() first, so their
string replacements still match the plain link text.
"""
import glob, hashlib, os, re

PAT = re.compile(r'((?:\.\./)*)(assets/(?:css|js)/[\w.-]+\.(?:css|js))(?:\?v=[\w.]+)?(?=")')
_cache = {}


def strip(s):
    return PAT.sub(r"\1\2", s)


def _ver(root, rel):
    if rel not in _cache:
        fp = os.path.join(root, rel)
        _cache[rel] = hashlib.md5(open(fp, "rb").read()).hexdigest()[:8] if os.path.exists(fp) else None
    return _cache[rel]


def stamp(s, root):
    def rep(m):
        v = _ver(root, m.group(2))
        return f"{m.group(1)}{m.group(2)}?v={v}" if v else m.group(1) + m.group(2)
    return PAT.sub(rep, s)


def stamp_all(root):
    _cache.clear(); changed = 0
    for fp in glob.glob(os.path.join(root, "**", "*.html"), recursive=True):
        if "/content/" in fp.replace(os.sep, "/") or "/node_modules/" in fp: continue
        s = open(fp, encoding="utf-8").read(); t = stamp(s, root)
        if t != s: open(fp, "w", encoding="utf-8").write(t); changed += 1
    return changed


if __name__ == "__main__":
    import sys
    print(stamp_all(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")), "pages stamped")
