"""Draft V9 data: V7 data (red-team corrected) + vendor directory + AI tools + problem->AI-category links."""
import json, pathlib, runpy
HERE = pathlib.Path(__file__).parent
runpy.run_path(str(HERE / 'build_data_v7.py'), run_name='__main__')   # rewrites assess_data.json with V7 data
runpy.run_path(str(HERE / 'build_dir_v9.py'), run_name='__main__')    # writes directory_v9.json
D = json.loads((HERE / 'assess_data.json').read_text())
X = json.loads((HERE / 'directory_v9.json').read_text())
D['version'] = 'Draft V9'
D['dir'], D['dir_groups'], D['dir_sources'] = X['dir'], X['groups'], X['sources']
D['ai_tools'], D['ai_cats'], D['ai_tags'] = X['ai_tools'], X['ai_cats'], X['ai_tags']

# Which AI tool categories help with which problem (only where AI genuinely helps)
AIP = {
 'p1': ['Finance & Legal', 'Data & Analytics'], 'p2': ['Finance & Legal'], 'p3': ['Finance & Legal', 'Data & Analytics'],
 'p4': ['Sales'], 'p5': ['Sales', 'Data & Analytics'], 'p6': ['Marketing', 'Email / Inbox'],
 'p8': ['HR & Recruiting', 'Education & Learning'], 'p9': ['Meeting & Notes', 'Research'],
 'p11': ['Cybersecurity'], 'p12': ['Data & Analytics'], 'p13': ['Automation / Workflow'],
 'p14': ['Writing & Content', 'Email / Inbox', 'Presentation'], 'p15': ['Cybersecurity'],
 'p16': ['Data & Analytics'], 'p17': ['Sales', 'Writing & Content'], 'p27': ['Writing & Content'],
 'p31': ['E-commerce & Retail'], 'p32': ['Automation / Workflow'], 'p37': ['Data & Analytics'],
 'p38': ['Marketing'], 'p39': ['E-commerce & Retail'], 'p42': ['Project Management'], 'p44': ['Writing & Content', 'Finance & Legal'],
 'p45': ['Project Management'], 'p46': ['Customer Support'], 'p48': ['Meeting & Notes'], 'p51': ['HR & Recruiting'],
 'p57': ['Automation / Workflow'], 'p58': ['Customer Support'], 'p59': ['Automation / Workflow'], 'p63': ['Customer Support'],
 'p67': ['Data & Analytics'], 'p70': ['E-commerce & Retail', 'Marketing'], 'p72': ['Customer Support'], 'p74': ['Marketing'],
 'p89': ['Automation / Workflow'],
}
cats = set(D['ai_cats'])
for pid, cs in AIP.items():
    assert all(c in cats for c in cs), (pid, cs)
D['ai_prob'] = AIP

# Fill a missing website on scored products from the directory (never overwrites anything else)
site = {e['sc']: e['u'] for e in D['dir'] if e.get('sc') and e.get('u')}
n = 0
for p in D['products']:
    k = p['cat'] + ':' + p['id']
    if not p.get('url') and k in site: p['url'] = site[k]; n += 1
for v in D['erp']['vendors']:
    k = 'erp:' + v['id']
    if not v.get('url') and k in site: v['url'] = site[k]; n += 1
(HERE / 'assess_data.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')))
print('V9 data written | websites added', n, '| bytes', (HERE / 'assess_data.json').stat().st_size)
