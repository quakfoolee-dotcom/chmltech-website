"""Certificate of completion upgrade (V4.84).

Replaces the two-column certificate footer on the 12 course pages (challenge-page/*.html) with three columns:
date completed | signature line (Quak Foo Lee, CEO and Principal Consultant) | certificate number + website.
The certificate number itself is filled in by assets/js/course.js (initCert). Idempotent: re-running changes nothing.

Run from the repo root:  python3 content/gen/cert_v484.py
"""
import glob, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import assetver

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OLD = ('<div class="cert-foot"><span><strong data-cert-date></strong>Date completed</span>'
       '<span><strong>Chmltech Ltd.</strong>www.chmltech.com</span></div>')
NEW = ('<div class="cert-foot">'
       '<span class="cert-col"><strong data-cert-date></strong>Date completed<br>&nbsp;</span>'
       '<span class="cert-col cert-sign"><img class="cert-sig-img" src="../assets/img/signature-quak-foo-lee.svg" alt="Signature of Quak Foo Lee" width="240" height="66">'
       '<strong>Quak Foo Lee</strong>CEO and Principal Consultant<br>Chmltech Ltd.</span>'
       '<span class="cert-col"><strong data-cert-id>CHM-0000</strong>Certificate no.<br>www.chmltech.com</span>'
       '</div>')

changed = 0
for fp in sorted(glob.glob(os.path.join(ROOT, "challenge-page", "*.html"))):
    s = open(fp, encoding="utf-8").read()
    if NEW in s: continue
    if OLD not in s:
        print("certificate footer not found:", os.path.relpath(fp, ROOT)); continue
    open(fp, "w", encoding="utf-8").write(s.replace(OLD, NEW)); changed += 1
print("pages updated:", changed)
print("asset links re-stamped:", assetver.stamp_all(ROOT))
