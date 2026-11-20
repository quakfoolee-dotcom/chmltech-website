"""Draft V11 data: V10 data + (1) every scored product listed in the Vendor Directory,
(2) per-listing industry tags so the directory's industry filter narrows within a category.

Industry tags ('i'): a list of industry ids the listing is built for; [] = general (all industries).
- Scored products: their scored industry list (all 11 = general).
- Directory listings: keyword rules on name + description + subcategory, with a fallback for
  inherently vertical groups (clinic -> health, farm -> agri, ...). Service partners are only tagged
  on strong industry words.
"""
import json, pathlib, re, runpy, collections

HERE = pathlib.Path(__file__).parent
runpy.run_path(str(HERE / 'build_data_v10.py'), run_name='__main__')
D = json.loads((HERE / 'assess_data.json').read_text())
IND = [i['id'] for i in D['industries']]

KW = {
    'mfg': r'manufactur|factory|shop floor|\bcnc\b|\bmes\b|\boee\b|machine shop|production line|fabricat|\bplant floor|process manufactur|food (and|&) beverage processing',
    'con': r'construct|contractor|\bbuilders?\b|home build|job ?site|subcontract|renovat|\bbim\b|\bvdc\b|rfis?\b|submittals?',
    'dist': r'distribut|wholesal|\b3pl\b|fulfil+ment centre|b2b order',
    'retail': r'\bretail|\bstores?\b|cannabis|apparel|\bdtc\b|direct-to-consumer|shopify|e-?commerce brand|merchants?\b',
    'prof': r'law firm|legal|lawyer|accounting firm|\bcpas?\b|bookkeep|professional services|architect|engineering firm|agenc(y|ies) (project|management)',
    'health': r'health|clinic|patient|dental|physio|chiropract|pharmac|medical|\bemr\b|\behr\b|long-term care|home care|virtual care',
    'food': r'restaurant|hospitality|food ?service|\bcaf[eé]s?\b|\bbars?\b|\bmenu|kitchen|hotel|delivery app',
    'trans': r'truck|\bfleet|freight|carrier|transport|dispatch|last[- ]mile|courier|\beld\b|telematic|logistics',
    're': r'propert|real estate|tenant|landlord|\bcondo|\blease|strata|\bhoa\b',
    'agri': r'\bfarm|agri|\bcrop|grain|livestock|greenhouse|agronom',
    'svc': r'salon|\bspa\b|fitness|\bgyms?\b|home service|\bhvac\b|plumb|cleaning|auto repair|landscap|pet groom|field service',
}
STRONG = {'mfg', 'con', 'health', 'food', 'trans', 're', 'agri'}   # used for service partners
FALLBACK = {'clinic': ['health'], 'farm': ['agri'], 'cpm': ['con'], 'prop': ['re'], 'tms': ['trans'],
            'mes': ['mfg'], 'mrp': ['mfg'], 'eng': ['mfg', 'con'], 'pos': ['retail', 'food'],
            'ship': ['retail', 'dist', 'trans'], 'auto': ['dist', 'mfg', 'trans'], 'booking': ['svc', 'health'],
            'fsm': ['svc', 'con'], 'psa': ['prof']}
PARTNER = {'integ', 'msp', 'web', 'aidev'}


def tag(e):
    text = ' '.join([e['n'], e['d'], e.get('sub', '')])
    hits = [k for k, pat in KW.items() if re.search(pat, text, re.I)]
    if e['g'] in PARTNER:
        hits = [h for h in hits if h in STRONG]
    # 'logistics' alone in a WMS/3PL description means distribution and logistics, not trucking only
    if e['g'] in ('wms', 'inv', 'scm') and 'trans' in hits and 'dist' not in hits:
        hits.append('dist')
    if e['g'] in ('auto', 'mes', 'eng', 'tms', 'ship', 'clinic', 'farm', 'prop', 'cpm'):
        hits = [h for h in hits if h in FALLBACK[e['g']] + (['dist'] if e['g'] in ('auto', 'ship') else [])]
    if not hits:
        hits = FALLBACK.get(e['g'], [])
    hits = [h for h in IND if h in hits]
    return [] if len(hits) >= 6 else hits      # tagged with most industries = general


for e in D['dir']:
    e['i'] = tag(e)

# --- every scored product appears in the directory ---
PRICE = {1: 'Under $25K first year', 2: '$25K–100K first year', 3: '$100K–300K first year', 4: 'Over $300K first year'}
linked = {e['sc'] for e in D['dir'] if e.get('sc')}
added = 0
def add(p, cid):
    global added
    k = cid + ':' + p['id']
    inds = p.get('inds') or []
    e = {'n': p['name'], 'g': cid, 'd': p.get('best', ''), 'u': p.get('url', ''), 'hq': '', 'sz': [z for z in 'sml' if z in p.get('size', [])],
         'dep': ' / '.join(p.get('deploy', [])), 'pr': PRICE.get(p.get('price'), ''), 'ca': bool(p.get('ca')),
         'src': ['Software Finder (scored)'], 'sub': '', 'sc': k, 'chk': 1 if p.get('v') else 0,
         'i': [] if len(set(inds)) >= len(IND) - 1 else [i for i in IND if i in inds]}
    if p.get('canada'): e['d'] = (e['d'] + '. ' if e['d'] else '') + 'Canada: ' + p['canada']
    D['dir'].append(e); linked.add(k); added += 1
for p in D['products']:
    if p['cat'] + ':' + p['id'] not in linked: add(p, p['cat'])
for v in D['erp']['vendors']:
    if 'erp:' + v['id'] not in linked: add(v, 'erp')
for v in D['wms']['vendors']:
    if 'wms:' + v['id'] not in linked: add(v, 'wms')
# linked listings take the scored industry fit as well
pmap = {p['cat'] + ':' + p['id']: p for p in D['products']}
pmap.update({'erp:' + v['id']: v for v in D['erp']['vendors']}); pmap.update({'wms:' + v['id']: v for v in D['wms']['vendors']})
for e in D['dir']:
    p = pmap.get(e.get('sc', ''))
    if p and p.get('inds'):
        inds = p['inds']; e['i'] = [] if len(set(inds)) >= len(IND) - 1 else [i for i in IND if i in inds]

D['version'] = 'Draft V11'
(HERE / 'assess_data.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')))
c = collections.Counter(i for e in D['dir'] for i in e['i'])
print('V11: scored products added to directory', added, '| directory', len(D['dir']),
      '| general', sum(1 for e in D['dir'] if not e['i']), '| tagged', dict(c))
