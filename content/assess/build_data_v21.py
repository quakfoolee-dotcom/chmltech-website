"""Draft V21 data: V15 data + AI tool comparison (6 tools per job, 4 shared Canada columns + 4 job columns),
from research files in content/assess/ai_research/research_{A,B,C}.json and the column guide ai_matrix_spec.json."""
import json, pathlib, re, runpy
HERE = pathlib.Path(__file__).parent
runpy.run_path(str(HERE / 'build_data_v15.py'), run_name='__main__')
D = json.loads((HERE / 'assess_data.json').read_text())
SPEC = json.loads((HERE / 'ai_matrix_spec.json').read_text())
M, n = {}, 0
for f in sorted((HERE / 'ai_research').glob('research_*.json')):
    for g, tools in json.loads(f.read_text())['jobs'].items():
        caps = [{'k': c['k'], 'n': c['n'], 'r': c['r']} for c in SPEC['jobs'][g]['caps']]
        out = []
        for t in tools:
            s = [max(0, min(3, int(x))) for x in t['s']]
            assert len(s) == len(caps), (g, t['name'])
            out.append({'id': re.sub(r'[^a-z0-9]+', '-', t['name'].lower()).strip('-'), 'n': t['name'], 'ex': t.get('match_existing') or '',
                        'u': t.get('url', ''), 'best': t.get('best', ''), 'price': t.get('price', ''), 's': s,
                        'ev': t.get('evidence', [''] * 8), 'notes': t.get('notes', [''] * 8), 'unv': t.get('unconfirmed', []),
                        'rc': t.get('rc', ''), 'canada': t.get('canada', '')})
            n += 1
        M[g] = {'caps': caps, 'tools': out, 'asof': 'November 2026'}
# independent review (verify_R1/R2): apply high/medium corrections with a source; confirmed scores lose the "unconfirmed" flag
log = {'applied': [], 'confirmed': 0, 'removed': []}
def tool(g, name):
    for t in M.get(g, {}).get('tools', []):
        if t['n'] == name: return t
for f in sorted((HERE / 'ai_research').glob('verify_*.json')):
    V = json.loads(f.read_text())
    for c in V['confirmed']:
        t = tool(c['job'], c['tool'])
        if not t: continue
        keys = [k['k'] for k in M[c['job']]['caps']]
        if c['key'] in keys:
            i = keys.index(c['key'])
            if c['key'] in t['unv']: t['unv'].remove(c['key']); log['confirmed'] += 1
            if c.get('evidence', '').startswith('http'): t['ev'][i] = c['evidence']
    for c in V['corrections']:
        if c['confidence'] not in ('high', 'medium') or not str(c.get('evidence', '')).startswith('http'): continue
        t = tool(c['job'], c['tool'])
        if not t: continue
        if c['key'] == 'price' and 'DISCONTINUED' in str(c['proposed']):
            M[c['job']]['tools'].remove(t); log['removed'].append(t['n']); continue
        if c['key'] == 'price':
            t['price'] = str(c['proposed'])[:140]; log['applied'].append((c['job'], t['n'], 'price')); continue
        keys = [k['k'] for k in M[c['job']]['caps']]
        if c['key'] not in keys: continue
        i = keys.index(c['key'])
        if t['s'][i] != int(c['proposed']):
            log['applied'].append((c['job'], t['n'], c['key'], t['s'][i], int(c['proposed'])))
        t['s'][i] = int(c['proposed']); t['ev'][i] = c['evidence']
        t['notes'][i] = c['why'][:90]
        if c['key'] in t['unv']: t['unv'].remove(c['key'])
# discontinued tools also leave the AI tools list
D['ai_tools'] = [x for x in D['ai_tools'] if x['n'] not in log['removed']]
D['ai_matrix'] = M
(HERE / 'ai_research' / 'review_log_v21.json').write_text(json.dumps(log, indent=1))
print('review: corrections applied', len(log['applied']), '| confirmed', log['confirmed'], '| removed', log['removed'],
      '| still unconfirmed', sum(len(t['unv']) for m in M.values() for t in m['tools']))
D['version'] = 'Draft V21'
(HERE / 'assess_data.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')))
print('V21: AI comparison jobs', len(M), '| tools', n)
