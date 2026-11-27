"""Grade a model's answers to the OEE test set (Chmltech Online Journal, Vol. 106, Issue 17).

answers.json: {"Q01": 77.7, "Q20": "L2", ...}   (numbers in the unit of each question; ranks as text)
Usage: python3 grade.py answers.json   ->  score by question type, and every miss
"""
import json, os, sys
from collections import defaultdict

qs = {q['id']: q for q in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions.json')))}
SYN = {'speed': 'performance', 'downtime': 'availability', 'yield': 'quality'}
norm = lambda x: SYN.get(x.strip().lower().removeprefix('line ').strip(), x.strip().lower().removeprefix('line ').strip())
ans = json.load(open(sys.argv[1]))
by = defaultdict(lambda: [0, 0]); misses = []
for i, q in qs.items():
    a = ans.get(i); by[q['type']][1] += 1
    if isinstance(q['answer'], str): ok = isinstance(a, str) and norm(a) == q['answer'].lower()
    else:
        try: ok = abs(float(a) - q['answer']) <= q['tolerance']
        except (TypeError, ValueError): ok = False
    by[q['type']][0] += ok
    if not ok: misses.append(f"{i} expected {q['answer']} {q['unit']}, got {a}")
for t, (k, n) in by.items(): print(f"{t:10s} {k}/{n}")
print(f"total      {sum(v[0] for v in by.values())}/{len(qs)}")
for m in misses: print('  miss:', m)
