"""Draft V15 data (UI clean-up): V13 data + tidier descriptions, one listing per scored vendor,
and AI tools grouped into 10 owner-facing groups."""
import json, pathlib, re, runpy
HERE = pathlib.Path(__file__).parent
runpy.run_path(str(HERE / 'build_data_v13.py'), run_name='__main__')
D = json.loads((HERE / 'assess_data.json').read_text())

# 1. descriptions: drop "Canada: ..." tails and leading "City, PROV | ticker." prefixes (the Based-in column shows them)
PREFIX = re.compile(r"^(?:[A-Z][\w'\-éè. ]+,\s*(?:[A-Z]{2}|Ontario|Quebec|Québec|BC|Alberta)\b[^.]*?\.\s+)")
n_d = 0
for e in D['dir']:
    d0 = e['d']
    d = re.sub(r'\.?\s*Canada:\s.*$', '', e['d']).strip()
    d = PREFIX.sub('', d).strip()
    if d and d[0].islower(): d = d[0].upper() + d[1:]
    if d != d0 and d: e['d'] = d if d.endswith(('.', '…', ')')) else d + '.'; n_d += 1

# 2. one listing per vendor: a WMS-scored entry duplicates the same vendor's ERP entry
erp_ids = {e['sc'].split(':')[1] for e in D['dir'] if e.get('sc', '').startswith('erp:')}
before = len(D['dir'])
D['dir'] = [e for e in D['dir'] if not (e.get('sc', '').startswith('wms:') and e['sc'].split(':')[1] in erp_ids)]
n_dup = before - len(D['dir'])

# 3. AI tool groups (owner-facing)
G = [('write', 'Writing and email', ['Writing & Content', 'Email / Inbox', 'SEO & Content', 'Translation & Language', 'Presentation']),
     ('meet', 'Meetings, notes and projects', ['Meeting & Notes', 'Personal Productivity', 'Project Management']),
     ('sales', 'Sales and marketing', ['Sales', 'Marketing', 'Brand / Creatives', 'E-commerce & Retail']),
     ('support', 'Customer support', ['Customer Support']),
     ('fin', 'Finance and legal', ['Finance & Legal']),
     ('hr', 'HR and training', ['HR & Recruiting', 'Education & Learning']),
     ('data', 'Data and research', ['Data & Analytics', 'Research']),
     ('auto', 'Automation and agents', ['Automation / Workflow', 'AI Agents']),
     ('sec', 'Security', ['Cybersecurity']),
     ('dev', 'Developer tools', ['Coding / Dev', 'Prompt-Only Code Gen', 'AI IDE', 'Async AI Agent', 'CLI AI Agent'])]
c2g = {c: gid for gid, _, cs in G for c in cs}
missing = sorted({t['c'] for t in D['ai_tools']} - set(c2g))
assert not missing, missing
for t in D['ai_tools']:
    t['grp'] = c2g[t['c']]
D['ai_groups'] = [[gid, name] for gid, name, _ in G]
PRFIX = {'Elpass AI': '$19.99/yr (7-day trial)', 'Hostinger Horizons': 'Low-cost plan bundled with Hostinger hosting'}
for t in D['ai_tools']:                        # reviewer notes left in two price fields
    if t['n'] in PRFIX: t['pr'] = PRFIX[t['n']]
    if t['n'] == 'Elpass AI': t['n'] = 'Elpass'
    if t['n'].startswith('Brex'): t['note'] = (t.get('note', '') + '. Serves mainly US businesses').strip('. '); t['d'] = t['d'].replace('AI password manager', 'Password manager')
for t in D['ai_tools']:                        # "Lex: AI document editor…" -> "AI document editor…"
    first = t['n'].split()[0].rstrip(':')
    if t['d'].startswith(first + ':'): t['d'] = t['d'][len(first) + 1:].strip()
    if t['n'] == 'Lex Email': t['n'] = 'Lex'
D['version'] = 'Draft V15'
(HERE / 'assess_data.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')))
print('V15: descriptions tidied', n_d, '| duplicate listings removed', n_dup, '| directory', len(D['dir']), '| AI groups', len(G))
