"""Summarize results.json for the paper and figures -> summary.json
main = every model warm-started from the best dispatching rule; nohint = sensitivity run without the warm start."""
import json
import numpy as np

R = json.load(open('results.json')); S = R['snapshots']
short = {'F0': 'F0 Reference model', 'F1': 'F1 No precedence', 'F2': 'F2 Capacity at weld only', 'F3': 'F3 Setups omitted',
         'F4': 'F4 Lateness, not tardiness', 'F5': 'F5 Makespan objective', 'F6': 'F6 Due-date units', 'F7': 'F7 Release times ignored',
         'F8': 'F8 Big-M too small'}
order = list(R['faults'])
best = [min(v['tard_h'] for v in s['rules'].values()) for s in S]
busy = [i for i, b in enumerate(best) if b > 0.05]


def block(key):
    out = dict(detect={}, any={}, total={}, total_nondelay={}, multiple={}, g4_alone={}, undetected={}, worse_than_rule={})
    ref_tot = sum(s[key]['F0']['tard_h'] for s in S)
    for f in order:
        g = [s[key][f]['gates'] for s in S]
        out['detect'][f] = {k: 100 * sum(1 for x in g if x[k]) / len(S) for k in ['G1', 'G2', 'G3', 'G4']}
        det = [any(v for v in x.values() if v) for x in g]
        out['any'][f] = 100 * sum(det) / len(S)
        out['g4_alone'][f] = sum(1 for x in g if x['G4'] and not any(x[k] for k in ('G1', 'G2', 'G3')))
        if f != 'F8' or all(s[key][f]['tard_h'] is not None for s in S):
            if any(s[key][f]['tard_h'] is None for s in S): continue
            out['total'][f] = sum(s[key][f]['tard_h'] for s in S)
            out['total_nondelay'][f] = sum(s[key][f]['nondelay_h'] for s in S)
            out['multiple'][f] = out['total'][f] / ref_tot if ref_tot else None
            und = [(i, s[key][f]['tard_h'] - s[key]['F0']['tard_h'], s[key][f]['tard_h'] - b)
                   for i, (s, d, b) in enumerate(zip(S, det, best)) if not d]
            out['undetected'][f] = dict(n=len(und), in_easy_weeks=sum(1 for i, _, _ in und if i not in busy),
                                        extra_vs_ref_h=sum(x for _, x, _ in und), worse_vs_ref=sum(1 for _, x, _ in und if x > 0.05),
                                        max_extra_h=max([x for _, x, _ in und] + [0]))
            out['worse_than_rule'][f] = sum(1 for s, b in zip(S, best) if s[key][f]['tard_h'] > b + 0.05)
    out['ref_total'] = ref_tot
    out['ref_optimal'] = sum(1 for s in S if s[key]['F0']['status'] == 'OPTIMAL')
    out['ref_better'] = sum(1 for s, b in zip(S, best) if s[key]['F0']['tard_h'] < b - 0.05)
    out['ref_worse'] = sum(1 for s, b in zip(S, best) if s[key]['F0']['tard_h'] > b + 0.05)
    out['ref_zero'] = sum(1 for s in S if s[key]['F0']['tard_h'] < 0.05)
    out['ref_late'] = float(np.mean([s[key]['F0']['late'] for s in S]))
    out['status'] = {f: {st: sum(1 for s in S if s[key][f]['status'] == st) for st in {s[key][f]['status'] for s in S}} for f in order}
    return out


out = dict(order=order, short=short, n=len(S), busy=len(busy), main=block('faults'), nohint=block('nohint'))
out['rules_total'] = {r: sum(s['rules'][r]['tard_h'] for s in S) for r in S[0]['rules']}
out['rules_late'] = {r: float(np.mean([s['rules'][r]['late'] for s in S])) for r in S[0]['rules']}
out['best_rule_total'] = sum(best)
out['orders'] = [min(s['n_orders'] for s in S), max(s['n_orders'] for s in S), float(np.mean([s['n_orders'] for s in S]))]
out['ops'] = [min(s['n_ops'] for s in S), max(s['n_ops'] for s in S), float(np.mean([s['n_ops'] for s in S]))]
out['weld_h'] = [min(s['weld_h'] for s in S), max(s['weld_h'] for s in S), float(np.mean([s['weld_h'] for s in S]))]
out['control_nondelay_total'] = sum(s['control_nondelay_h'] for s in S)
out['control_rightshift_total'] = sum(s['control_rightshift_h'] for s in S)
# figure keys (main run)
out['detect'] = out['main']['detect']; out['any'] = out['main']['any']; out['total'] = out['main']['total']
json.dump(out, open('summary.json', 'w'), indent=1)
for k in ('n', 'busy', 'orders', 'ops', 'weld_h', 'rules_total', 'rules_late', 'best_rule_total', 'control_nondelay_total', 'control_rightshift_total'):
    print(k, out[k])
for key in ('main', 'nohint'):
    print('=====', key)
    for k, v in out[key].items(): print(k, v)
