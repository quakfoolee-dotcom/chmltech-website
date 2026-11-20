"""Draft V9: vendor directory + AI tools, built from Chmltech's research master lists.

Inputs (copied to content/assess/sources/):
  ERP_Master_List_2025_v2.xlsx, WMS_Master_List_2025_V2.xlsx, WMS_Canada_Master_List_2026_V1.xlsx,
  Canadian_Software_IT_AI_Companies_Master_List_2026_V2.xlsx, Canadian_Technology_Companies_Master_List_V5.xlsx,
  AI_Tools_Master_List_v8.xlsx
Output: content/assess/directory_v9.json  (merged into assess_data.json by build_data_v9.py)

Directory entries are listings, not scores: they are never used to change a capability score,
and they never overwrite red-team-corrected product facts. They only add a website to a scored
product when it had none.
"""
import json, re, pathlib, collections
import openpyxl

HERE = pathlib.Path(__file__).parent
SRC = HERE / 'sources'

LISTS = {
    'erp':   ('ERP_Master_List_2025_v2.xlsx', 'Top ERP Tools 2025', 'ERP Master List 2025'),
    'wms':   ('WMS_Master_List_2025_V2.xlsx', 'WMS Master List 2025', 'WMS Master List 2025'),
    'wmsca': ('WMS_Canada_Master_List_2026_V1.xlsx', 'WMS Canada 2026', 'WMS Canada 2026'),
    'casw':  ('Canadian_Software_IT_AI_Companies_Master_List_2026_V2.xlsx', 'Canadian Companies', 'Canadian Software, IT & AI 2026'),
    'catech':('Canadian_Technology_Companies_Master_List_V5.xlsx', 'V5 Master Data', 'Canadian Technology Companies V5'),
    'ai':    ('AI_Tools_Master_List_v8.xlsx', 'AI Tools Master List', 'AI Tools Master List v8'),
}

# Directory groups. 'cat' links a group to an assessment category; kind s = software, p = service partner.
GROUPS = [
    # software that maps to assessment categories (labels come from the category)
    *[(c, c, 's') for c in ['acct', 'payroll', 'crm', 'mkt', 'ecom', 'pos', 'booking', 'clinic', 'psa', 'fsm', 'cpm',
                            'inv', 'mrp', 'erp', 'wms', 'tms', 'prop', 'farm', 'collab', 'bi', 'sec', 'ai']],
    # specialist software (directory only)
    ('mes', 'Manufacturing and frontline operations (MES, OEE, connected worker)', 's'),
    ('eng', 'Engineering, CAD and simulation', 's'),
    ('cmms', 'Maintenance and asset management (CMMS/EAM)', 's'),
    ('qms', 'Quality, safety and traceability', 's'),
    ('scm', 'Supply chain planning, yard and procurement', 's'),
    ('ship', 'Shipping, fulfilment and last mile', 's'),
    ('auto', 'Warehouse automation and robotics', 's'),
    ('pay', 'Payments and fintech', 's'),
    ('lms', 'Learning, training and recruiting', 's'),
    ('itops', 'IT operations and device management', 's'),
    ('energy', 'Energy and utilities software', 's'),
    ('vert', 'Other industry-specific software', 's'),
    # service partners
    ('integ', 'Implementation and integration partners', 'p'),
    ('msp', 'Managed IT and cloud services', 'p'),
    ('web', 'Website and digital agencies', 'p'),
    ('aidev', 'AI, data and robotics specialists', 'p'),
]
GROUP_INDS = {  # industries for directory-only groups ('' = all)
    'mes': ['mfg', 'food'], 'eng': ['mfg', 'con'], 'cmms': ['mfg', 'food', 'trans', 're', 'con'],
    'qms': ['mfg', 'food', 'health', 'dist'], 'scm': ['mfg', 'dist', 'retail', 'trans'],
    'ship': ['dist', 'retail', 'trans', 'mfg'], 'auto': ['dist', 'mfg', 'trans'],
}


def rows(key):
    f, sheet, _ = LISTS[key]
    ws = openpyxl.load_workbook(SRC / f, read_only=True, data_only=True)[sheet]
    return [[(str(c).strip() if c is not None else '') for c in r] for r in ws.iter_rows(values_only=True)]


def sectioned(key):
    """ERP / WMS sheets: '#01' rows under a category heading row."""
    out, cat = [], ''
    for x in rows(key)[1:]:
        a = x[0].strip()
        if a.startswith('#'):
            out.append([cat] + x[1:7])
        elif a and (not any(x[1:4]) or x[1].startswith('Tool')):
            cat = a
    return out


def url(u):
    u = (u or '').strip()
    if not u or ' ' in u:
        return ''
    return u if u.startswith('http') else 'https://' + u


def domain(u):
    m = re.match(r'https?://(?:www\.)?([^/]+)', u or '')
    return m.group(1).lower() if m else ''


STRIP = r'\b(inc|ltd|limited|corp|corporation|co|technologies|technology|software|solutions|systems|group|platform|the)\b'


def norm(n):
    n = re.sub(r'\(.*?\)', '', n.lower()).replace('&', ' and ')
    n = re.sub(r'[^a-z0-9 ]', ' ', n)
    n = re.sub(STRIP, ' ', n)
    return re.sub(r'\s+', ' ', n).strip()


def sizes(t):
    t = t.lower(); s = []
    if 'all sizes' in t: return ['s', 'm', 'l']
    if re.search(r'smb|micro|freelance|small|consumer', t): s.append('s')
    if 'mid' in t: s.append('m')
    if 'enterprise' in t: s.append('l')
    return s


def kw(text, rules, default):
    for pat, g in rules:
        if re.search(pat, text, re.I):
            return g
    return default


VERT = [(r'dental|clinic|physio|chiropract|patient|emr\b|pharmac|health', 'clinic'),
        (r'property|real estate|condo|tenant|landlord|strata', 'prop'),
        (r'\bfarm|agri|crop|grain|livestock', 'farm'),
        (r'restaurant|hospitality|bar\b|food service', 'pos'),
        (r'construct|contractor|builder', 'cpm'),
        (r'salon|spa\b|appointment|booking|fitness', 'booking'),
        (r'field service|hvac|plumb|dispatch', 'fsm'),
        (r'legal|law firm|accounting firm', 'psa')]


def classify_company(src, cat, sec, desc, tags):
    """Canadian company lists (casw, catech)."""
    t = ' '.join([cat, sec, desc, tags])
    if src == 'casw':
        m = {'ERP': 'erp', 'CRM': 'crm', 'HR / Payroll': 'payroll', 'Logistics / TMS': 'tms', 'E-Commerce': 'ecom',
             'WMS / Supply Chain': 'wms', 'AI / ML': 'aidev', 'Web Development': 'web', 'Integration': 'integ',
             'IT Services': 'msp', 'Accounting / Fintech': 'acct', 'Vertical SaaS': 'vert'}
        g = m.get(cat, 'vert')
    else:
        m = {'AI / ML / Robotics': 'aidev', 'Website Development / Digital Agencies': 'web',
             'IT Services / MSP / Cloud': 'msp', 'Software Integration / Digital Transformation': 'integ',
             'HR / Workforce / Learning': 'payroll', 'Sales / CRM / Marketing / CX': 'crm',
             'Finance / Accounting / FinTech': 'acct', 'Logistics / TMS / Fleet': 'tms', 'Ecommerce / Retail': 'ecom',
             'Data / Analytics / Automation': 'bi', 'Cybersecurity / IT Operations': 'sec',
             'Industry-Specific / Vertical Software': 'vert', 'ERP / Business Management': 'erp',
             'Project / Portfolio / Resource Management': 'psa', 'Healthcare / Clinical': 'clinic',
             'Manufacturing / Industrial Operations': 'mes', 'Engineering / Technical Software': 'eng',
             'Construction / PropTech': 'cpm', 'Operations Management / Operational Excellence': 'mes',
             'Quality / EHS / Compliance': 'qms', 'Warehouse / WMS': 'wms', 'Asset / Maintenance / Facilities': 'cmms',
             '3PL / Fulfillment / Distribution': 'ship', 'Energy / Utilities / Cleantech Software': 'energy',
             'Warehouse Automation / Material Handling': 'auto', 'Supply Chain Planning / APS': 'scm',
             'Procurement / Supplier Management': 'scm', 'Lab / Scientific / LIMS': 'qms',
             'Freight Forwarding / Trade Compliance': 'scm'}
        g = m.get(cat, 'vert')
    # refinements on the secondary category / description
    if g == 'crm' and re.search(r'marketing|email|seo|social|loyalty|review', sec + ' ' + desc, re.I) and not re.search(r'\bcrm\b', sec, re.I): g = 'mkt'
    if g == 'acct' and re.search(r'payment|banking|wealth|lending|card|fintech|payroll', sec + ' ' + desc, re.I) and not re.search(r'accounting|bookkeep|invoic|ap\b|ar\b|fp&a|audit|expense', sec + ' ' + desc, re.I): g = 'pay'
    if g == 'payroll' and re.search(r'learning|lms|training|course|education|recruit|job board|hiring|talent marketplace|student', sec + ' ' + desc, re.I) \
            and not re.search(r'payroll|hris|hcm|time and attendance|scheduling', sec + ' ' + desc, re.I): g = 'lms'
    if g == 'tms' and re.search(r'shipping|last mile|last-mile|courier|parcel|fulfil', sec if src == 'catech' else desc, re.I) \
            and not re.search(r'\btms\b|fleet|dispatch|transportation management|eld\b|telematics|trucking|carrier software|freight software', sec + ' ' + desc, re.I): g = 'ship'
    if g == 'bi' and re.search(r'data room|file shar|file transfer|digital asset|document', sec + ' ' + desc, re.I) and not re.search(r'analytic|dashboard|report', sec + ' ' + desc, re.I): g = 'collab'
    if g == 'bi' and re.search(r'backup', desc, re.I): g = 'sec'
    if g == 'vert' and re.search(r'social media|marketing', desc, re.I): g = 'mkt'
    if g == 'ecom' and re.search(r'\bpos\b|point of sale|point-of-sale', sec + ' ' + desc, re.I): g = 'pos'
    if g == 'cpm' and re.search(r'property|proptech|real estate|condo|tenant', sec + ' ' + desc, re.I): g = 'prop'
    if g == 'wms' and re.search(r'planning|procure|visibility|supply chain network', sec, re.I) and not re.search(r'warehouse', sec + desc, re.I): g = 'scm'
    if g == 'sec' and re.search(r'device management|mdm|it operations|monitoring|itsm|help desk', sec + ' ' + desc, re.I) and not re.search(r'security|cyber|threat|backup', sec, re.I): g = 'itops'
    if g == 'aidev' and re.search(r'robot|automation|material handling', sec, re.I) and re.search(r'warehouse|industrial|manufactur', sec + ' ' + desc, re.I): g = 'auto'
    tail = sec.split(' — ')[-1]
    if re.search(r'field service|dispatch|hvac|landscape|scheduling / dispatch', tail, re.I): g = 'fsm'
    elif re.search(r'construction', tail, re.I) and g not in ('erp', 'integ', 'web', 'msp'): g = 'cpm'
    elif re.search(r'field service', sec, re.I): g = 'fsm'
    if re.search(r'cmms|eam|maintenance', sec, re.I) and g not in ('integ', 'msp'): g = 'cmms'
    if g == 'vert' and not re.search(r'holding|portfolio of|acquir|operating group', desc, re.I): g = kw(t, VERT, 'vert')
    if g == 'pos' and re.search(r'holding|portfolio of|acquir|operating group', desc, re.I): g = 'vert'
    return g


def classify_listed(src, section, name):
    """ERP / WMS product lists."""
    n = name.lower()
    if src == 'erp':
        if section.startswith('Finance'): return 'bi' if re.search(r'prophix|planful', n) else 'acct'
        if section.startswith('HR'): return 'payroll'
        if section.startswith('Retail'):
            if re.search(r'lightspeed|revel|retail pro|eagle|ivend', n): return 'pos'
            if re.search(r'shopify|magento|commerce', n): return 'ecom'
            if 'wm' in n: return 'wms'
            return 'erp'
        if section.startswith('Construction'): return 'cpm' if re.search(r'procore|buildertrend|coconstruct', n) else 'erp'
        if section.startswith('Healthcare'): return 'vert'
        if re.search(r'katana', n): return 'mrp'
        if re.search(r'workday', n) and section.startswith('Cloud'): return 'payroll'
        if re.search(r'brightpearl|cin7', n): return 'inv'
        return 'erp'
    if src == 'wms':
        return 'wms'
    # Canadian WMS list
    if section.startswith('Canadian Enterprise'): return 'tms' if 'tms' in n else ('acct' if 'billing' in n else ('mes' if 'mes' in n else 'wms'))
    if section.startswith('Canadian SMB'):
        if 'inflow' in n: return 'inv'
        if 'nectari' in n: return 'bi'
        if 'poka' in n: return 'mes'
        if re.search(r'lightspeed|cova|greenline', n): return 'pos'
        if 'shopify' in n: return 'ecom'
        return 'erp'
    if section.startswith('Canadian Yard'):
        if re.search(r'geotab|isaac|fleet complete|cetaris|loadlink', n): return 'tms'
        if re.search(r'optel|trustbix|provision', n): return 'qms'
        if 'soti' in n: return 'itops'
        if 'rebus' in n: return 'wms'
        return 'scm'
    if section.startswith('Canadian Robotics'): return 'auto'
    if section.startswith('Canadian eCommerce'): return 'tms' if 'routific' in n else 'ship'
    if section.startswith('Canadian Implementation'): return 'integ'
    return 'vert'


def main():
    A = json.loads((HERE / 'assess_data.json').read_text())
    scored = {}
    for p in A['products']:
        scored.setdefault(norm(p['name']), []).append(p['cat'] + ':' + p['id'])
    for v in A['erp']['vendors']:
        scored.setdefault(norm(v['name']), []).append('erp:' + v['id'])
    for v in A['wms']['vendors']:
        scored.setdefault(norm(v['name']), []).append('wms:' + v['id'])
    # aliases: list name -> scored name (same product, different label)
    ALIAS = {'microsoft dynamics 365 bc': 'microsoft dynamics 365 business central', 'acumatica cloud erp': 'acumatica',
             'netsuite': 'oracle netsuite', 'oracle netsuite': 'oracle netsuite', 'katana mrp': 'katana',
             'cin7 core': 'cin7 core', 'epicor erp enterprise': None, 'odoo community': 'odoo', 'odoo com': 'odoo',
             'logiwa wms': 'logiwa', 'deposco bright suite': 'deposco', 'mecalux easy wms': 'mecalux easy wms',
             'extensiv 3pl warehouse manager': 'extensiv 3pl warehouse manager', 'ceridian dayforce': 'dayforce',
             'inflow inventory wms': 'inflow inventory', 'zoho inventory wms': 'zoho inventory',
             'lightspeed commerce': None, 'shopify + erp connectors': 'shopify', 'cin7 core dear': 'cin7 core',
             'sage intacct construction': 'sage intacct', 'jobboss eci': None, 'fishbowl manufacturing': 'fishbowl manufacturing'}

    entries, by_key, by_dom = [], {}, {}

    def add(src, name, group, desc='', site='', hq='', size=None, deploy='', price='', ca=False, sub=''):
        name = re.sub(r'\s+', ' ', name).strip()
        if not name or len(name) < 2:
            return
        k = norm(name); site = url(site); d = domain(site)
        e = by_key.get(k)
        if e is None and d and src in ('casw', 'catech') and d in by_dom:
            e = by_dom[d]          # same company listed under a slightly different name
        if e is None:
            e = {'n': name, 'g': group, 'd': desc, 'u': site, 'hq': hq, 'sz': size or [], 'dep': deploy,
                 'pr': price, 'ca': ca, 'src': [], 'sub': sub}
            entries.append(e); by_key[k] = e
            if d and src in ('casw', 'catech', 'wmsca'): by_dom.setdefault(d, e)
        else:
            if not e['d'] and desc: e['d'] = desc
            if not e['u'] and site: e['u'] = site
            if not e['hq'] and hq: e['hq'] = hq
            if not e['dep'] and deploy: e['dep'] = deploy
            if not e['pr'] and price: e['pr'] = price
            if size: e['sz'] = sorted(set(e['sz']) | set(size), key='sml'.index)
            e['ca'] = e['ca'] or ca
            # a Canadian company list's grouping is more specific than a generic list's
            if src in ('casw', 'catech', 'wmsca') and e['g'] in ('vert', 'erp') and group not in ('vert', 'integ', 'web', 'msp'):
                e['g'] = group
        lab = LISTS[src][2]
        if lab not in e['src']:
            e['src'].append(lab)

    # Canadian lists first, so Canadian descriptions and HQs win
    for x in sectioned('wmsca'):
        sec, name, sz, dep, pr, desc, site = x[:7]
        hq = desc.split('|')[0].split('.')[0].strip() if re.match(r'^[A-Z][a-zé\-\. ]+, (?:[A-Z]{2})\b', desc) else ''
        add('wmsca', name, classify_listed('wmsca', sec, name), desc, site, hq, sizes(sz), dep, pr, True, sec.replace('Canadian ', ''))
    for x in rows('catech')[1:]:
        if not x[0].isdigit(): continue
        _, ctype, dom, sec, name, desc, site, hq, tags = x[:9]
        add('catech', name, classify_company('catech', dom, sec, desc, tags), desc, site, hq, None, '', '', True,
            sec.split(' — ')[-1])
    for x in rows('casw')[1:]:
        if not x[0].isdigit(): continue
        _, cat, name, desc, site, hq, seg = x[:7]
        add('casw', name, classify_company('casw', cat, '', desc, ''), desc, site, hq, sizes(seg), '', '', True, cat)
    for src in ('erp', 'wms'):
        for x in sectioned(src):
            sec, name, sz, dep, pr, desc, site = x[:7]
            add(src, name, classify_listed(src, sec, name), desc, site, '', sizes(sz), dep, pr, False, sec)

    # explicit overrides where keyword rules misread the description (reviewed by hand)
    OVERRIDE = {'Jonas Software': 'vert', 'FreightPath': 'tms', 'BrainBox AI': 'energy', 'Fleetr': 'tms',
                'Kinaxis Maestro': 'scm', 'Nulogy MOS': 'mes', 'OpenText Business Network (EDI)': 'scm',
                'Euna Solutions': 'vert', 'Bonfire': 'scm', 'Convictional': 'ecom', 'Local Line': 'ecom',
                'Jesta I.S.': 'erp'}
    for e in entries:
        if e['n'] in OVERRIDE: e['g'] = OVERRIDE[e['n']]

    # link to scored products
    for e in entries:
        k = norm(e['n']); k = ALIAS.get(k, k) if k in ALIAS else k
        if k and k in scored:
            e['sc'] = scored[k][0]
    # one listing per scored product: merge duplicates that link to the same scored product
    seen, merged = {}, []
    for e in entries:
        k = e.get('sc')
        if k and k in seen:
            f = seen[k]
            for fld in ('d', 'u', 'hq', 'dep', 'pr'):
                if not f[fld] and e[fld]: f[fld] = e[fld]
            f['sz'] = sorted(set(f['sz']) | set(e['sz']), key='sml'.index); f['ca'] = f['ca'] or e['ca']
            f['src'] += [x for x in e['src'] if x not in f['src']]
            continue
        if k: seen[k] = e
        merged.append(e)
    entries[:] = merged

    # Canadian HQ known from scored data
    vmap = {p['cat'] + ':' + p['id']: p for p in A['products']}
    vmap.update({'erp:' + v['id']: v for v in A['erp']['vendors']})
    for e in entries:
        p = vmap.get(e.get('sc', ''))
        if p and p.get('ca'): e['ca'] = True

    # AI tools
    ai, cat = [], ''
    for x in rows('ai')[1:]:
        if x[0].isdigit():
            ai.append({'c': x[1], 'n': x[2], 'd': x[3], 'u': url(x[4]), 'pr': x[5], 't': x[6]})
    tags = [r[:2] for r in openpyxl.load_workbook(SRC / LISTS['ai'][0], read_only=True, data_only=True)['Use Case Tag Legend'].iter_rows(values_only=True)][1:]
    tags = [[str(a), str(b)] for a, b in tags if a]
    ai_cats = list(dict.fromkeys(t['c'] for t in ai))

    out = {'groups': [{'id': g, 'name': n, 'k': k, 'inds': GROUP_INDS.get(g, [])} for g, n, k in GROUPS],
           'dir': entries, 'ai_tools': ai, 'ai_cats': ai_cats, 'ai_tags': tags,
           'sources': [{'id': k, 'name': v[2], 'file': v[0]} for k, v in LISTS.items()]}
    (HERE / 'directory_v9.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')))
    c = collections.Counter(e['g'] for e in entries)
    print('directory entries', len(entries), '| Canadian', sum(e['ca'] for e in entries),
          '| linked to scored', sum(1 for e in entries if e.get('sc')), '| AI tools', len(ai))
    print(sorted(c.items(), key=lambda x: -x[1]))


if __name__ == '__main__':
    main()
