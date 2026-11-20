"""Draft V13 data: V11 data + an official website for every scored product (scored_urls_v13.json,
each checked to load on 2026-11-20), copied to the product profile and its Vendor Directory listing."""
import json, pathlib, runpy
HERE = pathlib.Path(__file__).parent
runpy.run_path(str(HERE / 'build_data_v11.py'), run_name='__main__')
D = json.loads((HERE / 'assess_data.json').read_text())
U = json.loads((HERE / 'scored_urls_v13.json').read_text())
n = 0
for p in D['products']:
    k = p['cat'] + ':' + p['id']
    if not p.get('url') and k in U: p['url'] = U[k]; n += 1
for key, lst in (('erp', D['erp']['vendors']), ('wms', D['wms']['vendors'])):
    for v in lst:
        k = key + ':' + v['id']
        if not v.get('url') and k in U: v['url'] = U[k]; n += 1
pmap = {p['cat'] + ':' + p['id']: p for p in D['products']}
pmap.update({'erp:' + v['id']: v for v in D['erp']['vendors']}); pmap.update({'wms:' + v['id']: v for v in D['wms']['vendors']})
d = 0
for e in D['dir']:
    if not e.get('u') and e.get('sc') and pmap.get(e['sc'], {}).get('url'):
        e['u'] = pmap[e['sc']]['url']; d += 1
for e in D['dir']:   # product profile takes the listing's website when the product has none
    p = pmap.get(e.get('sc', ''))
    if p is not None and not p.get('url') and e.get('u'): p['url'] = e['u']; n += 1
# fix moved or wrong links found by the full link check (url_fixes_v13.json)
FIX = {k.rstrip('/'): v for k, v in json.loads((HERE / 'url_fixes_v13.json').read_text()).items()}
f = 0
for e in D['dir'] + D['ai_tools']:
    if e.get('u') and e['u'].rstrip('/') in FIX: e['u'] = FIX[e['u'].rstrip('/')]; f += 1
for p in D['products'] + D['erp']['vendors'] + D['wms']['vendors']:
    if p.get('url') and p['url'].rstrip('/') in FIX: p['url'] = FIX[p['url'].rstrip('/')]; f += 1
print('links fixed', f)
D['version'] = 'Draft V13'
(HERE / 'assess_data.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')))
miss_p = [p['name'] for p in D['products'] + D['erp']['vendors'] + D['wms']['vendors'] if not p.get('url')]
miss_d = [e['n'] for e in D['dir'] if not e.get('u')]; miss_a = [t['n'] for t in D['ai_tools'] if not t.get('u')]
print('V13 websites: products', n, '| directory', d, '| still missing: products', miss_p, 'directory', miss_d, 'AI', miss_a)
