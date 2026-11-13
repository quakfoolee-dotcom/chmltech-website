"""Certificate signature image (V4.85).

Replaces the italic text placeholder on the 12 course certificates with assets/img/signature-quak-foo-lee.svg:
"Quak Foo Lee" drawn as vector paths from the open-licence font Mrs Saint Delafield (content/gen/fonts/), in ink blue.
To redraw:  python3 content/gen/signature_svg.py content/gen/fonts/MrsSaintDelafield-Regular.ttf "Quak Foo Lee" \
              > assets/img/signature-quak-foo-lee.svg
Idempotent. Run from the repo root:  python3 content/gen/cert_v485.py
"""
import glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import assetver

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OLD = '<span class="cert-sig-name">Quak Foo Lee</span>'
NEW = '<img class="cert-sig-img" src="../assets/img/signature-quak-foo-lee.svg" alt="Signature of Quak Foo Lee" width="240" height="66">'
changed = 0
for fp in sorted(glob.glob(os.path.join(ROOT, "challenge-page", "*.html"))):
    s = open(fp, encoding="utf-8").read()
    if OLD in s: open(fp, "w", encoding="utf-8").write(s.replace(OLD, NEW)); changed += 1
print("pages updated:", changed)
print("asset links re-stamped:", assetver.stamp_all(ROOT))
