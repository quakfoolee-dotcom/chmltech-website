"""Draft V10 data: V9 data + red-team corrections to the vendor directory and AI tools.

Rule (same as V7): a finding is applied only when confidence is high or medium AND evidence is a URL.
Desk-only or low-confidence findings are counted as 'not applied' and listed in the report.
Findings files: content/assess/redteam_v10/findings_{A..E}.json (indices refer to the V9 directory / AI list).
"""
import json, pathlib, re, runpy, collections

HERE = pathlib.Path(__file__).parent
RT = HERE / 'redteam_v10'
runpy.run_path(str(HERE / 'build_data_v9.py'), run_name='__main__')
D = json.loads((HERE / 'assess_data.json').read_text())
DIR, AI = D['dir'], D['ai_tools']
GROUPS = {g['id'] for g in D['dir_groups']}
AICATS = set(D['ai_cats'])
TAGS = {t[0] for t in D['ai_tags']}
URL = re.compile(r'https?://[^\s,;)"\']+')

log, skipped, confirmed = [], [], {'dir': set(), 'ai': set()}
remove = {'dir': set(), 'ai': set()}


def ok(f):
    return f.get('confidence') in ('high', 'medium') and str(f.get('evidence', '')).startswith('http')


def new_name(text):
    t = re.sub(r'^(renamed|rename to|now)\s*:?\s*', '', text.strip(), flags=re.I)
    t = URL.sub('', t)
    t = re.split(r'\s+-\s+|;|,\s*(?=$)|\s+—\s+', t)[0]
    t = re.sub(r',\s*(custom|free.*)?$', '', t.strip(), flags=re.I).strip(' ,.')
    return t


def apply(scope, f, reviewer):
    rows = DIR if scope == 'dir' else AI
    i = f['idx']
    if not (0 <= i < len(rows)):
        skipped.append((reviewer, f, 'bad idx')); return
    e = rows[i]
    names = (e['n'] + ' ' + e.get('was', '')).lower()
    if f.get('name') and f['name'].split(' (')[0].lower()[:12] not in names and e['n'].split(' (')[0].lower()[:12] not in f['name'].lower():
        skipped.append((reviewer, f, 'name mismatch: ' + e['n'])); return
    fld, prop = f['field'], str(f.get('proposed', '')).strip()
    before = None
    if fld == 'duplicate' or (fld == 'status' and re.search(r'^\s*(remove|merge into)|;\s*remove\b|^\s*remove\b', prop, re.I)) or re.search(r'merge into idx', prop, re.I):
        remove[scope].add(i); log.append((reviewer, scope, i, e['n'], 'removed', f['why'][:160], f['evidence'])); return
    if fld == 'status' and re.match(r'^\s*acquired', prop, re.I):
        e['note'] = 'Acquired' + re.sub(r'^\s*acquired\s*(-\s*)?', ' ', prop, flags=re.I).split(';')[0].rstrip('. ') + '.'
        e['note'] = e['note'].replace('Acquired now', 'Acquired: now').replace('Acquired part', 'Acquired: part').replace('Acquired ' + e['n'], 'Acquired:')
        log.append((reviewer, scope, i, e['n'], 'note: ' + e['note'][:90], f['why'][:160], f['evidence'])); return
    m = re.search(r'\bis now ([^(;,]+)', prop)
    if fld == 'status' and m:
        prop = m.group(1).strip() + ' (formerly ' + e['n'] + ')'
    if fld == 'status':
        nm = new_name(prop); u = URL.search(prop)
        if nm and len(nm) <= 70 and nm.lower() != e['n'].lower():
            before = e['n']; e['was'] = e['n']; e['n'] = nm
        if u: e['u'] = u.group(0).rstrip('/.')
        note = f['why'].split('. ')[0][:140]
        e['note'] = note
        log.append((reviewer, scope, i, before or e['n'], 'status → ' + (nm or 'note'), f['why'][:160], f['evidence'])); return
    if fld == 'website':
        u = URL.search(prop)
        if not u: skipped.append((reviewer, f, 'no url in proposal')); return
        before = e['u']; e['u'] = u.group(0).rstrip('/.') if u.group(0).count('/') <= 3 else u.group(0)
    elif fld in ('hq',) and scope == 'dir':
        before = e['hq']; e['hq'] = prop[:60]
    elif fld == 'canadian' and scope == 'dir':
        before = e['ca']; e['ca'] = prop.lower().startswith('true')
    elif fld == 'group' and scope == 'dir':
        g = prop.split()[0].strip(" ,.'\"") if prop else ''
        if g not in GROUPS: skipped.append((reviewer, f, 'unknown group ' + prop[:30])); return
        before = e['g']; e['g'] = g
    elif fld == 'size' and scope == 'dir':
        sz = [z for z in 'sml' if re.search({'s': r'small|smb|\bs\b', 'm': r'mid|\bm\b', 'l': r'large|enterprise|\bl\b'}[z], prop, re.I)]
        if not sz: skipped.append((reviewer, f, 'size unparsed')); return
        before = e['sz']; e['sz'] = sz
    elif fld in ('price', 'pricing'):
        k = 'pr'; before = e[k]; e[k] = prop if len(prop) <= 90 else prop[:88].rsplit(' ', 1)[0] + '…'
    elif fld == 'desc':
        before = e['d']
        if prop.lower().startswith('add:'):
            add = prop[4:].strip(); org = re.search(r'\bby ([A-Z][\w&.-]+)', add)
            if org and org.group(1).lower() in e['d'].lower():
                log.append((reviewer, scope, i, e['n'], 'desc: already stated', f['why'][:160], f['evidence'])); return
            e['d'] = (e['d'].rstrip('. ') + '. ' + add[0].upper() + add[1:])[:260]
        else:
            e['d'] = prop[:240]
    elif fld == 'category' and scope == 'ai':
        if prop not in AICATS: skipped.append((reviewer, f, 'unknown ai cat')); return
        before = e['c']; e['c'] = prop
    elif fld == 'tag' and scope == 'ai':
        if prop not in TAGS: skipped.append((reviewer, f, 'unknown tag')); return
        before = e['t']; e['t'] = prop
    else:
        skipped.append((reviewer, f, 'unhandled field')); return
    log.append((reviewer, scope, i, e['n'], fld + ': ' + str(before)[:50] + ' → ' + prop[:70], f['why'][:160], f['evidence']))


stats = {}
for k in 'ABCDE':
    d = json.loads((RT / f'findings_{k}.json').read_text())
    scope = 'dir' if k in 'ABC' else 'ai'
    F = d.get('findings', [])
    stats[k] = {'findings': len(F), 'applied': 0, 'not_applied': 0, 'confirmed': len(d.get('confirmed', [])),
                'logic': len(d.get('logic', []))}
    for f in F:
        if ok(f):
            n0 = len(log); apply(scope, f, k)
            stats[k]['applied'] += len(log) > n0
        else:
            stats[k]['not_applied'] += 1
    confirmed[scope].update(i for i in d.get('confirmed', []) if isinstance(i, int))

# mark red-team-checked listings (confirmed, or corrected with evidence) before removal shifts indices
for i in confirmed['dir'] | {x[2] for x in log if x[1] == 'dir'}:
    if i < len(DIR): DIR[i]['chk'] = 1
for i in confirmed['ai'] | {x[2] for x in log if x[1] == 'ai'}:
    if i < len(AI): AI[i]['chk'] = 1
D['dir'] = [e for i, e in enumerate(DIR) if i not in remove['dir']]
D['ai_tools'] = [t for i, t in enumerate(AI) if i not in remove['ai']]
D['ai_cats'] = [c for c in D['ai_cats'] if any(t['c'] == c for t in D['ai_tools'])]

# AI problem map: reviewer D and E logic findings
P = D['ai_prob']
P['p6'] = ['Marketing']                                   # inbox tools are not customer email marketing
P['p9'] = ['Meeting & Notes', 'Writing & Content']        # 'Research' = academic search tools
P['p46'] = ['Automation / Workflow']; P['p72'] = ['Automation / Workflow']   # reminders, not helpdesks
P['p27'] = ['Writing & Content', 'Sales']; P['p44'] = ['Writing & Content', 'Presentation', 'Finance & Legal']
for pid in ('p48', 'p11', 'p15'):                        # charting needs clinical-grade privacy; backup and AI rules are not solved by AI tools
    P.pop(pid, None)
for pid, cs in P.items():
    P[pid] = [c for c in cs if c in D['ai_cats']]

NOTEFIX = {'Acquired: Inc., a Rand Group company': 'Acquired: now a Rand Group company', 'Acquired: is now part of': 'Acquired: now part of'}
for e in D['dir'] + D['ai_tools']:
    for k, v in NOTEFIX.items():
        if e.get('note'): e['note'] = e['note'].replace(k, v)
D['version'] = 'Draft V10'
D['rt10'] = {'date': '2026-11-20', 'stats': stats, 'applied': len(log), 'removed_dir': len(remove['dir']),
             'removed_ai': len(remove['ai']), 'checked_dir': sum(1 for e in D['dir'] if e.get('chk')),
             'checked_ai': sum(1 for t in D['ai_tools'] if t.get('chk'))}
(HERE / 'assess_data.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')))
(HERE / 'redteam_v10_log.json').write_text(json.dumps(
    {'applied': [dict(reviewer=r, list=s, idx=i, name=n, change=c, why=w, evidence=ev) for r, s, i, n, c, w, ev in log],
     'skipped': [dict(reviewer=r, idx=f.get('idx'), name=f.get('name'), field=f.get('field'), reason=why) for r, f, why in skipped],
     'stats': D['rt10']}, ensure_ascii=False, indent=1))
print('V10 applied', len(log), '| removed dir', len(remove['dir']), 'ai', len(remove['ai']), '| skipped', len(skipped))
print('directory now', len(D['dir']), 'Canadian', sum(e['ca'] for e in D['dir']), '| AI tools', len(D['ai_tools']), 'cats', len(D['ai_cats']))
print(json.dumps(stats))
