"""Grades benchmark answers (Chmltech Online Journal, AI-agent paper). Usage: python grade_V1.py reference_set1.json answers_set1
A negative tolerance is an absolute band; zero means an exact match."""
import json, glob, os, sys
REF = json.load(open(sys.argv[1])); folder = sys.argv[2]
for f in sorted(glob.glob(os.path.join(folder, "*.json"))):
    A = json.load(open(f)); ok_keys = n_keys = ok_tasks = 0
    for tid, r in REF.items():
        task_ok = True
        for k, a in r["answers"].items():
            v = A.get(tid, {}).get(k); ref, tol = a["value"], a["tol"]
            try:
                v = float(v)
                ok = abs(v - ref) < 1e-9 if tol == 0 else (abs(v - ref) <= -tol if tol < 0 else abs(v - ref) / abs(ref) <= tol)
            except (TypeError, ValueError):
                ok = False
            ok_keys += ok; n_keys += 1; task_ok &= ok
        ok_tasks += task_ok
    print(f"{os.path.basename(f)[:-5]:20s} tasks {ok_tasks}/{len(REF)}  answers {ok_keys}/{n_keys}")
