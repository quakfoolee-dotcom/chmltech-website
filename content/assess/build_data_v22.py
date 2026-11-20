"""Draft V22 data: V21 data + final confirmation pass before publication.
Inputs in content/assess/confirm_v22/: result_ai1.json, result_ai2.json (AI matrix), result_sw.json (Software Finder
unconfirmed items), result_dir.json (vendor directory findings not applied in V10).
Rule: apply only results with a URL and high/medium confidence. Unresolved items stay flagged as unconfirmed."""
import json, pathlib, runpy
HERE = pathlib.Path(__file__).parent
C = HERE / 'confirm_v22'
runpy.run_path(str(HERE / 'build_data_v21.py'), run_name='__main__')
D = json.loads((HERE / 'assess_data.json').read_text())
log = {'ai_confirmed': 0, 'ai_corrected': [], 'ai_unresolved': 0, 'sw_confirmed': 0, 'sw_corrected': [], 'sw_unresolved': 0,
       'dir_applied': [], 'dir_rejected': 0, 'dir_unresolved': 0}

def good(r):
    return r.get('confidence') in ('high', 'medium') and str(r.get('evidence', '')).startswith('http')

# 1. AI matrix
for f in ('result_ai1.json', 'result_ai2.json'):
    p = C / f
    if not p.exists(): continue
    for r in json.loads(p.read_text()):
        m = D['ai_matrix'].get(r['job']); t = next((x for x in (m or {}).get('tools', []) if x['n'] == r['tool']), None)
        if not t: continue
        keys = [c['k'] for c in m['caps']]
        if r['key'] not in keys: continue
        i = keys.index(r['key'])
        if r['result'] in ('confirmed', 'corrected') and good(r):
            if r['result'] == 'corrected' and int(r['score']) != t['s'][i]:
                log['ai_corrected'].append([r['job'], t['n'], r['key'], t['s'][i], int(r['score'])])
                t['s'][i] = max(0, min(3, int(r['score'])))
            else:
                log['ai_confirmed'] += 1
            t['ev'][i] = r['evidence']
            if r.get('note'): t['notes'][i] = r['note'][:90]
            if r['key'] in t['unv']: t['unv'].remove(r['key'])
        else:
            log['ai_unresolved'] += 1

# 2. Software Finder unconfirmed items (product 'unv' lists hold "Workflow: Capability" labels or category capability names)
p = C / 'result_sw.json'
if p.exists():
    prods = {x['name']: x for x in D['products'] + D['erp']['vendors']}
    WFN = {w['name']: w for w in D['erp']['workflows']}
    CATS = {c['id']: c for c in D['categories']}
    def locate(prod, item):
        if ': ' in item:
            wn, cap = item.split(': ', 1); w = WFN.get(wn)
            if w and w['id'] in prod.get('s', {}):
                names = [c['n'] for c in w['caps']]
                if cap in names: return prod['s'][w['id']], names.index(cap)
        else:
            names = [c['n'] for c in CATS.get(prod.get('cat'), {}).get('caps', [])]
            if item in names: return prod['s'], names.index(item)
        return None, None
    for r in json.loads(p.read_text()):
        prod = prods.get(r['product'])
        if not prod or r['item'] not in prod.get('unv', []): continue
        arr, i = locate(prod, r['item'])
        found = r.get('score')
        if arr is not None and found is not None and int(found) != arr[i]:
            # apply when sourced at high/medium confidence; a low-confidence LOWER score is also applied (never overstate) but stays flagged
            if good(r) or (str(r.get('evidence', '')).startswith('http') and int(found) < arr[i]):
                log['sw_corrected'].append([prod['name'], r['item'], arr[i], int(found), r['confidence']])
                arr[i] = int(found)
        if good(r):
            prod['unv'].remove(r['item'])
            if r.get('fact') and 'Canadian' in r['item'] and str(r['fact']).lower() == 'true':
                pass   # Canadian hosting confirmed; the product's canada text already states it
            if found is None or arr is None or int(found) == arr[i]: log['sw_confirmed'] += 1
        else:
            log['sw_unresolved'] += 1

# 3. Vendor directory findings
GROUPS = {g['id'] for g in D['dir_groups']}
p = C / 'result_dir.json'
if p.exists():
    remove = set()
    for r in json.loads(p.read_text()):
        if r['decision'] != 'accept' or not good(r):
            log['dir_rejected' if r['decision'] == 'reject' else 'dir_unresolved'] += 1; continue
        key = (r['name'] or '').split(' (')[0].lower()[:14]
        e = next((x for x in D['dir'] if key and (key in x['n'].lower() or key in x.get('was', '').lower())), None)
        if not e: continue
        f, v = r['field'], r['value']
        if f in ('status', 'duplicate') and str(v).lower() in ('remove', 'closed'):
            remove.add(id(e)); log['dir_applied'].append([e['n'], 'removed']); continue
        if f == 'duplicate':
            remove.add(id(e)); log['dir_applied'].append([e['n'], 'duplicate of ' + str(v)]); continue
        if f == 'status':
            e['was'] = e['n']; e['n'] = str(v)[:70]
        elif f == 'group' and v in GROUPS: e['g'] = v
        elif f == 'canadian': e['ca'] = str(v).lower() in ('true', 'yes', '1')
        elif f == 'hq': e['hq'] = str(v)[:60]
        elif f == 'website' and str(v).startswith('http'): e['u'] = v
        elif f == 'desc': e['d'] = str(v)[:240]
        elif f == 'price': e['pr'] = str(v)[:90]
        elif f == 'size':
            e['sz'] = [z for z in 'sml' if z in str(v).lower()[:3] or {'s': 'small', 'm': 'mid', 'l': 'large'}[z] in str(v).lower()]
        else: continue
        log['dir_applied'].append([e['n'], f, str(v)[:60]])
    D['dir'] = [x for x in D['dir'] if id(x) not in remove]

# editorial decisions on reviewer judgement calls and renames (2026-11-20)
for t in D['ai_matrix'].get('sec', {}).get('tools', []):
    if t['n'].startswith('1Password'):
        keys = [c['k'] for c in D['ai_matrix']['sec']['caps']]; i = keys.index('suite')
        if t['s'][i] == 3:
            t['s'][i] = 2; t['notes'][i] = 'Sign-in through Entra ID or Google; no Outlook or Gmail add-in'
            log['ai_corrected'].append(['sec', t['n'], 'suite', 3, 2])
for e in D['dir']:
    if e['n'].startswith('iLobby'):
        e['was'] = e['n']; e['n'] = 'FacilityOS (formerly iLobby)'; e['u'] = 'https://www.facilityos.com/'
        log['dir_applied'].append([e['n'], 'renamed'])
    if e['n'].startswith('CRM Dynamics'):
        e['was'] = e['n']; e['n'] = 'HSO (formerly CRM Dynamics)'; e['u'] = 'https://www.hso.com/'; e['ca'] = False
        log['dir_applied'].append([e['n'], 'renamed'])
D['version'] = 'Draft V22'
(HERE / 'assess_data.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')))
(C / 'confirm_log_v22.json').write_text(json.dumps(log, indent=1, ensure_ascii=False))
print('V22 confirm: AI confirmed', log['ai_confirmed'], 'corrected', len(log['ai_corrected']), 'unresolved', log['ai_unresolved'],
      '| software confirmed', log['sw_confirmed'], 'corrected', len(log['sw_corrected']), 'unresolved', log['sw_unresolved'],
      '| directory applied', len(log['dir_applied']), 'rejected', log['dir_rejected'], 'unresolved', log['dir_unresolved'],
      '| AI still unconfirmed', sum(len(t['unv']) for m in D['ai_matrix'].values() for t in m['tools']),
      '| software still unconfirmed', sum(len(x.get('unv', [])) for x in D['products'] + D['erp']['vendors']))
