/* Funding Match (funding.html) — Draft V1.
   A five-step wizard that ranks the funding finder's programs for one business.
   Data: #grants-data (content/grants.json) and #fm-rules (content/funding/rules_v1.json: structured eligibility rules).
   Rules: a stated rule the business fails rules a program out (or makes it a near miss); an unknown rule never does.
   Report: same form and report service as the Digital Assessment (window.ChmlReportPdf / ChmlReportText). */
(function () {
  'use strict';
  var root = document.getElementById('fm'); if (!root) return;
  var DATA, RULES;
  try { DATA = JSON.parse(document.getElementById('grants-data').textContent); RULES = JSON.parse(document.getElementById('fm-rules').textContent); } catch (e) { return; }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function full(n) { return '$' + Math.round(n).toLocaleString('en-CA'); }
  function money(n) { if (n == null) return ''; if (n >= 999500) { var m = Math.floor(n / 1e5) / 10; return '$' + m + 'M'; } if (n >= 1e3) return '$' + Math.round(n / 1e3) + 'K'; return '$' + n; }
  var CLOSED = 'Closed to new applications';

  /* ---------- questions ---------- */
  var PROV = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'New Brunswick', 'Nova Scotia', 'Prince Edward Island', 'Newfoundland and Labrador', 'Yukon', 'Northwest Territories', 'Nunavut'];
  var IND = [['Manufacturing', 'Manufacturing'], ['Construction', 'Construction and trades'], ['Retail & wholesale', 'Retail, wholesale and distribution'], ['Transportation & logistics', 'Transportation, warehousing and logistics'],
    ['Technology & digital', 'Software, IT and digital'], ['Professional services', 'Professional and business services'], ['Life sciences & health', 'Health care and life sciences'], ['Tourism & hospitality', 'Tourism, food service and hospitality'],
    ['Agriculture & agri-food', 'Agriculture and farming'], ['food', 'Food and beverage processing', '', ['Agriculture & agri-food', 'Manufacturing']], ['Clean technology', 'Clean technology'], ['Mining & energy', 'Mining, oil, gas and energy'], ['Forestry', 'Forestry and wood products'],
    ['Fisheries & aquaculture', 'Fisheries and aquaculture'], ['Aerospace & defence', 'Aerospace and defence'], ['Automotive', 'Automotive'], ['Arts, culture & media', 'Arts, culture and media'], ['other', 'Something else']];
  var LEGAL = [['inc', 'Incorporated company', 'Federal or provincial corporation'], ['sole', 'Sole proprietor', 'Registered business name, not incorporated'], ['part', 'Partnership'], ['coop', 'Co-operative'], ['npo', 'Non-profit or charity'], ['none', 'Not registered yet', 'Planning to start a business']];
  var EMP = [['0', 'Just me', 1, 1], ['1', '1 to 2', 1, 2], ['3', '3 to 4', 3, 4], ['5', '5 to 9', 5, 9], ['10', '10 to 49', 10, 49], ['50', '50 to 99', 50, 99], ['100', '100 to 249', 100, 249], ['250', '250 to 499', 250, 499], ['500', '500 or more', 500, 1e6]];
  var REV = [['0', 'No revenue yet', 0, 0], ['1', 'Under $100,000', 1, 99999], ['2', '$100,000 to $299,999', 1e5, 299999], ['3', '$300,000 to $999,999', 3e5, 999999], ['4', '$1 million to $2.4 million', 1e6, 2499999],
    ['5', '$2.5 million to $9.9 million', 2.5e6, 9999999], ['6', '$10 million to $49.9 million', 1e7, 49999999], ['7', '$50 million to $100 million', 5e7, 1e8], ['8', 'Over $100 million', 1e8 + 1, 1e12]];
  var YRS = [['0', 'Not started yet', 0, 0], ['1', 'Less than 1 year', 0.1, 0.99], ['2', '1 to 2 years', 1, 1.99], ['3', '2 to 3 years', 2, 2.99], ['4', '3 to 5 years', 3, 4.99], ['5', 'More than 5 years', 5, 99]];
  var GOALS = [
    ['rd', 'Develop a new product, service or process', 'R&D, prototypes, testing', ['Research & development', 'Innovation & commercialization']],
    ['dig', 'Adopt digital tools, software or AI', 'ERP, e-commerce, automation, AI', ['Digital adoption & technology', 'Productivity & operations']],
    ['eq', 'Buy equipment or upgrade a facility', 'Machinery, technology, buildings', ['Equipment & capital investment', 'Manufacturing']],
    ['prod', 'Improve productivity and operations', 'Lean, process improvement, capacity', ['Productivity & operations', 'Manufacturing']],
    ['hire', 'Hire staff, students or interns', 'Wage subsidies and hiring grants', ['Hiring & wages']],
    ['train', 'Train employees', 'Courses, certifications, upskilling', ['Training & skills']],
    ['exp', 'Export or enter new markets', 'Trade shows, market research, certification', ['Export & trade']],
    ['clean', 'Cut energy use or emissions', 'Efficiency, clean technology, fuel switching', ['Clean technology & energy efficiency']],
    ['grow', 'Expand, relocate or open a new site', 'Growth and scale-up projects', ['Business expansion', 'Regional & community development']],
    ['start', 'Start a new business', 'Start-up financing and mentoring', ['Startup & early stage']]];
  var SHORT = { rd: 'new products and R&D', dig: 'digital tools, software and AI', eq: 'equipment and facilities', prod: 'productivity', hire: 'hiring', train: 'training', exp: 'exporting', clean: 'energy and emissions', grow: 'expansion', start: 'starting a business' };
  var SECTOR_PURPOSE = { 'Agriculture & agri-food': 'Agriculture & agri-food', 'Fisheries & aquaculture': 'Fisheries & ocean', 'Tourism & hospitality': 'Tourism', 'Arts, culture & media': 'Arts, culture & media', 'Manufacturing': 'Manufacturing' };
  var BUDGET = [['1', 'Under $25,000', 15000, 25000], ['2', '$25,000 to $100,000', 60000, 100000], ['3', '$100,000 to $500,000', 250000, 500000], ['4', '$500,000 to $2 million', 1e6, 2e6], ['5', 'Over $2 million', 4e6, 1e12]];
  var START = [['soon', 'In the next 3 months'], ['later', 'In 3 to 12 months'], ['started', 'It has already started']];
  var WHO = [['Indigenous-owned business', 'Indigenous-owned'], ['Women-owned business', 'Women-owned or led'], ['Black-owned business', 'Black-owned or led'], ['Youth entrepreneur', 'Owner aged 18 to 39'],
    ['Newcomer entrepreneur', 'Newcomer to Canada'], ['Rural business', 'Rural or remote location'], ['Exporter', 'Already exporting'], ['Social enterprise', 'Social enterprise'], ['none', 'None of these']];
  var PREF = [['grant', 'Grants and contributions', 'Money you do not repay'], ['tax', 'Tax credits', 'Claimed with your tax return after you spend'], ['loan', 'Loans and financing', 'Repayable, often on better terms than a bank'], ['adv', 'Advice and expert help', 'Advisors, coaching, subsidized consultants']];
  var CASH = [['25', 'About 25% or more'], ['50', 'About 50% or more'], ['75', '75% or more'], ['0', 'Not sure yet']];
  var READY = [['bn', 'A CRA business number'], ['fs', 'Financial statements for the last year'], ['plan', 'A written project plan and budget'], ['cash', 'Cash to pay costs first and claim them back later'], ['nil', 'None of these yet']];
  var TYPEGROUP = { 'Grant': 'grant', 'Repayable contribution': 'grant', 'Voucher': 'grant', 'Wage subsidy': 'grant', 'Rebate/Incentive': 'grant', 'Tax credit': 'tax', 'Loan': 'loan', 'Loan guarantee': 'loan', 'Equity investment': 'loan', 'Advisory service': 'adv' };
  var GROUPNAME = { grant: 'Grants and contributions', tax: 'Tax credits', loan: 'Loans and financing', adv: 'Advice and expert help' };

  var STEPS = ['Your business', 'Your project', 'About you', 'Funding type', 'Readiness'];
  function opt(a) { return a.map(function (x) { return [x[0], x[1], typeof x[2] === 'string' ? x[2] : '']; }); }
  var SCREENS = [
    { k: 'prov', st: 0, q: 'Where does your business operate?', hint: 'Pick the province or territory where the project will happen.', o: function () { return PROV.map(function (p) { return [p, p]; }); }, cols: 2 },
    { k: 'region', st: 0, q: 'Which part of Ontario?', hint: 'Some programs are only for one region.', o: function () { return [['north', 'Northern Ontario', 'Including Sudbury, Thunder Bay, Sault Ste. Marie, North Bay'], ['east', 'Eastern Ontario', 'Including Ottawa, Kingston, Belleville'], ['southwest', 'Southwestern Ontario', 'Including London, Windsor, Waterloo Region'], ['central', 'Toronto and central Ontario', 'Including the GTA, Hamilton, Niagara, Barrie']]; }, when: function () { return ans.prov === 'Ontario'; } },
    { k: 'ind', st: 0, q: 'Which industry best describes your business?', o: function () { return IND; }, cols: 2 },
    { k: 'legal', st: 0, q: 'How is your business set up?', hint: 'Many programs only fund incorporated businesses.', o: function () { return opt(LEGAL); } },
    { k: 'emp', st: 0, q: 'How many people work in the business?', hint: 'Count full-time equivalents in Canada, including you.', o: function () { return opt(EMP); }, cols: 3 },
    { k: 'rev', st: 0, q: 'What was your revenue in the last full year?', o: function () { return opt(REV); }, cols: 2, when: function () { return ans.legal !== 'none'; } },
    { k: 'yrs', st: 0, q: 'How long has the business been operating?', o: function () { return opt(YRS); }, cols: 3, when: function () { return ans.legal !== 'none'; } },
    { k: 'goal', st: 1, q: 'What do you want funding for?', hint: 'Pick up to three.', max: 3, o: function () { return GOALS.map(function (g) { return [g[0], g[1], g[2]]; }); } },
    { k: 'budget', st: 1, q: 'About how much will the project cost in total?', hint: 'Pick a range. If you know the figure, enter it below for more precise amounts.', o: function () { return BUDGET.map(function (b) { return [b[0], b[1], '']; }); }, extra: costHTML },
    { k: 'start', st: 1, q: 'When will the project start?', hint: 'Most grants only cover costs after approval.', o: function () { return opt(START); } },
    { k: 'who', st: 2, q: 'Do any of these describe your business?', hint: 'Optional. Some programs are reserved for these groups. Pick all that apply, or "None of these".', max: 9, o: function () { return opt(WHO); }, cols: 2, excl: 'none' },
    { k: 'sit', st: 2, q: 'Do any of these situations apply?', hint: 'Some programs are only for these situations. Pick all that apply, or "None of these".', max: 4, o: function () { return [['tariff', 'Affected by U.S. tariffs', 'Lost sales, higher costs or a need to find new markets'], ['defence', 'Supplying or planning to supply defence or security customers'], ['energy', 'Large energy user', 'Industrial or large commercial electricity or gas account'], ['none', 'None of these']]; }, excl: 'none' },
    { k: 'pref', st: 3, q: 'What kind of funding would you consider?', hint: 'Pick all that apply.', max: 4, o: function () { return opt(PREF); } },
    { k: 'cash', st: 3, q: 'How much of the project cost could you pay yourself?', hint: 'Most programs share costs. Your share usually has to be cash.', o: function () { return opt(CASH); } },
    { k: 'ready', st: 4, q: 'What do you already have in place?', hint: 'Pick all that apply.', max: 5, o: function () { return opt(READY); }, excl: 'nil' }];

  var ans = {}, idx = 0;
  var intro = $('#fm-intro'), quiz = $('#fm-quiz'), result = $('#fm-result'), qbox = $('#fm-qbox'), next = $('#fm-next'), back = $('#fm-back');
  function visible() { return SCREENS.filter(function (s) { return !s.when || s.when(); }); }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-fm]'); if (!t) return;
    var a = t.dataset.fm;
    if (a === 'start' || a === 'restart') { e.preventDefault(); ans = {}; idx = 0; RES = null; REP = null; var f = $('#fm-result form'); if (f) { f.reset(); var st = f.querySelector('.form-status'); if (st) st.textContent = ''; } intro.hidden = true; result.hidden = true; quiz.hidden = false; show.ready = true; show(); $('#match').scrollIntoView({ behavior: 'smooth' }); }
    if (a === 'more') { var box = t.previousElementSibling; box.hidden = false; var h = box.querySelector('h4'); t.remove(); if (h) { h.tabIndex = -1; h.focus(); } }
    if (a === 'print') {
      var lbl = t.textContent; t.disabled = true; t.textContent = 'Preparing PDF…';
      makePdf().then(function (o) { o.doc.save(o.file); }).catch(function () { window.print(); }).then(function () { t.disabled = false; t.textContent = lbl; });
    }
  });
  function show() {
    var list = visible(), s = list[idx];
    $('#fm-steps').innerHTML = STEPS.map(function (n, i) { return '<li' + (i === s.st ? ' aria-current="step"' : '') + ' class="' + (i === s.st ? 'on' : i < s.st ? 'done' : '') + '">' + (i + 1) + '. ' + n + '</li>'; }).join('');
    $('#fm-bar').style.width = (idx / list.length * 100) + '%';
    $('#fm-qcount').textContent = 'Question ' + (idx + 1) + ' of ' + list.length;
    var multi = !!s.max, sel = ans[s.k] || (multi ? [] : '');
    qbox.innerHTML = '<legend class="finder-qtext h-md" tabindex="-1" style="font-size:24px">' + esc(s.q) + '</legend>' + (s.hint ? '<p class="erp-qhint" id="fm-hint">' + esc(s.hint) + '</p>' : '') + (s.max && s.max < 9 ? '<p class="fm-limit" id="fm-limit" aria-live="polite"></p>' : '') +
      '<div class="finder-opts' + (s.cols ? ' fm-cols' + s.cols : '') + '">' + s.o().map(function (o) {
        var on = multi ? sel.indexOf(o[0]) >= 0 : sel === o[0];
        return '<label class="finder-opt"><input type="' + (multi ? 'checkbox' : 'radio') + '" name="fq_' + s.k + '" value="' + esc(o[0]) + '"' + (on ? ' checked' : '') + '><span>' + esc(o[1]) + (o[2] ? '<small>' + esc(o[2]) + '</small>' : '') + '</span></label>';
      }).join('') + '</div>' + (s.extra ? s.extra() : '');
    if (s.hint) qbox.setAttribute('aria-describedby', 'fm-hint'); else qbox.removeAttribute('aria-describedby');
    back.disabled = idx === 0;
    next.textContent = idx === list.length - 1 ? 'See my funding matches →' : 'Next →';
    update(); limit();
    if (show.ready) qbox.querySelector('legend').focus({ preventScroll: true });
  }
  function limit() {
    var s = visible()[idx], el = $('#fm-limit'); if (!s.max || !el) return;
    var n = $$('input:checked', qbox).length, full = n >= s.max;
    $$('input', qbox).forEach(function (b) { b.disabled = full && !b.checked; });
    el.textContent = full ? 'You have picked ' + s.max + '. Untick one to choose another.' : '';
  }
  function costHTML() {
    return '<div class="fm-cost"><label for="fm-cost">Exact project cost <span class="hint">(optional)</span></label>' +
      '<div class="fm-cost-in"><span aria-hidden="true">$</span><input id="fm-cost" type="text" inputmode="numeric" autocomplete="off" placeholder="e.g. 275,000" value="' + (ans.cost ? ans.cost.toLocaleString('en-CA') : '') + '" aria-describedby="fm-cost-msg"></div>' +
      '<p class="fm-cost-msg" id="fm-cost-msg" aria-live="polite"></p></div>';
  }
  function parseCost(v) { v = String(v || '').replace(/[\s,$]/g, ''); if (!v) return 0; if (!/^\d+(\.\d+)?$/.test(v)) return NaN; return Math.round(+v); }
  function rangeFor(n) { for (var i = 0; i < BUDGET.length; i++) if (n < BUDGET[i][3] || i === BUDGET.length - 1) return BUDGET[i][0]; }
  qbox.addEventListener('input', function (e) {
    if (e.target.id !== 'fm-cost') return;
    var n = parseCost(e.target.value), msg = $('#fm-cost-msg');
    costBad = false;
    if (isNaN(n) || (n && n < 1000)) { costBad = true; msg.textContent = 'Enter the total cost in dollars, for example 275,000.'; delete ans.cost; }
    else if (!n) { msg.textContent = ''; delete ans.cost; }
    else { ans.cost = n; ans.budget = rangeFor(n); msg.textContent = 'Using ' + full(n) + ' (' + row(BUDGET, ans.budget)[1] + ').'; var rb = qbox.querySelector('input[type=radio][value="' + ans.budget + '"]'); if (rb) rb.checked = true; }
    update();
  });
  var costBad = false;
  qbox.addEventListener('change', function (e) {
    if (e.target.id === 'fm-cost') return;
    var s = visible()[idx];
    if (s.max) {
      if (s.excl) {
        if (e.target.value === s.excl && e.target.checked) $$('input', qbox).forEach(function (b) { if (b.value !== s.excl) b.checked = false; });
        else if (e.target.checked) $$('input', qbox).forEach(function (b) { if (b.value === s.excl) b.checked = false; });
      }
      var boxes = $$('input:checked', qbox);
      if (boxes.length > s.max) { e.target.checked = false; boxes = $$('input:checked', qbox); }
      ans[s.k] = boxes.map(function (b) { return b.value; }); limit();
    } else { var prev = ans[s.k]; ans[s.k] = e.target.value;
      if (s.k === 'legal' && ans.legal === 'none') { ans.rev = '0'; ans.yrs = '0'; }
      else if (s.k === 'legal' && prev === 'none') { delete ans.rev; delete ans.yrs; }
      if (s.k === 'budget' && ans.cost && rangeFor(ans.cost) !== ans.budget) { delete ans.cost; costBad = false; var ci = $('#fm-cost'); if (ci) ci.value = ''; var cm = $('#fm-cost-msg'); if (cm) cm.textContent = 'The figure did not fit that range, so it was cleared.'; } }
    update();
  });
  function update() { var s = visible()[idx], v = ans[s.k]; next.disabled = !(v && v.length) || (s.k === 'budget' && costBad); }
  back.addEventListener('click', function () { if (idx > 0) { idx--; show(); } });
  next.addEventListener('click', function () { if (next.disabled) return; if (idx < visible().length - 1) { idx++; show(); window.scrollTo({ top: $('#match').offsetTop - 70, behavior: 'smooth' }); } else finish(); });

  /* ---------- matching ---------- */
  function row(list, k) { return list.filter(function (x) { return x[0] === k; })[0]; }
  function profile() {
    var e = row(EMP, ans.emp), r = row(REV, ans.rev || '0'), y = row(YRS, ans.yrs || '0');
    var forprofit = ans.legal !== 'npo';
    var types = [];
    if (ans.legal === 'npo') types.push('Non-profit');
    else { types.push(e[2] >= 500 ? 'Large business' : 'Small & medium business'); if (ans.legal === 'coop') types.push('Co-operative'); }
    if (y[3] < 2 || ans.legal === 'none') types.push('Startup');
    var who = (ans.who || []).filter(function (w) { return w !== 'none'; });
    var ind = row(IND, ans.ind), inds = ind && ind[3] ? ind[3] : [ans.ind];
    var purposes = {}, sector = SECTOR_PURPOSE[inds[0]];
    (ans.goal || []).forEach(function (g) { row(GOALS, g)[3].forEach(function (p) { purposes[p] = purposes[p] || g; }); });
    return { prov: ans.prov, region: ans.prov === 'Ontario' ? ans.region : null, ind: ans.ind, inds: inds, legal: ans.legal, forprofit: forprofit, emp: [e[2], e[3]], rev: [r[2], r[3]], yrs: [y[2], y[3]],
      types: types, who: who, sit: (ans.sit || []).filter(function (w) { return w !== 'none'; }), purposes: purposes, sector: sector, budget: ans.cost || row(BUDGET, ans.budget)[2], budgetHi: ans.cost || row(BUDGET, ans.budget)[3], exact: !!ans.cost,
      pref: ans.pref || [], started: ans.start === 'started', cash: +ans.cash };
  }
  function inProv(r, P) { if (r.jurisdiction === P.prov) return true; if (r.jurisdiction !== 'Federal') return false; return r.provinces.indexOf('All') >= 0 || r.provinces.indexOf(P.prov) >= 0; }
  function inRegion(ru, P) {
    if (!ru.region || !P.region) return true;
    if (ru.region === 'south') return P.region !== 'north';
    return ru.region === P.region;
  }
  // primary type: the first listed type decides the group (a loan-led program with a small grant part stays a loan)
  function groupOf(r) { return TYPEGROUP[r.funding_types[0]] || 'grant'; }
  function rep(x) { return x.r.funding_types.indexOf('Repayable contribution') >= 0 || x.g === 'loan'; }
  var SIZE_TAGS = ['Small & medium business', 'Large business', 'Non-profit', 'Co-operative', 'Startup'];
  var NICHE = { tariff: ['tariff', 'businesses affected by U.S. tariffs'], defence: ['defence', 'defence and security supply chains'], energy: ['energy', 'large energy users (industrial or large commercial accounts)'],
    ccus: [null, 'carbon capture, utilization and storage projects'], worksharing: [null, 'employers in an approved Work-Sharing agreement'], cea: [null, 'greenhouse and vertical farming projects'], building: [null, 'owners of large commercial or industrial buildings'] };
  function evaluate(r0, P) {
    if (!inProv(r0, P)) return null;
    var ru = RULES[r0.id] || {};
    var r = ru.data ? Object.assign({}, r0, ru.data) : r0;
    if (!inRegion(ru, P)) return null;
    var indHit = P.inds.some(function (i) { return r.industries.indexOf(i) >= 0; });
    if (!indHit && r.industries.indexOf('All industries') < 0) return null;
    // who can apply: size/form tags must match; identity tags (Exporter, Rural...) cannot stand in for size
    var sizeTags = r.applicant_types.filter(function (t) { return SIZE_TAGS.indexOf(t) >= 0; });
    var whoTags = r.applicant_types.filter(function (t) { return SIZE_TAGS.indexOf(t) < 0; });
    if (sizeTags.length) { if (!sizeTags.some(function (t) { return P.types.indexOf(t) >= 0; })) return null; }
    else if (!whoTags.some(function (t) { return P.who.indexOf(t) >= 0; })) return null;
    if ((ru.req_who || []).some(function (w) { return P.who.indexOf(w) < 0; })) return null;
    // purposes
    var hitGoals = {}, sectorHit = false, hitP = 0;
    r.purposes.forEach(function (p) { if (P.purposes[p]) { hitGoals[P.purposes[p]] = 1; hitP++; } if (p === P.sector) sectorHit = true; });
    var nGoals = Object.keys(hitGoals).length;
    if (!nGoals) return null;
    var SECT = ['Agriculture & agri-food', 'Fisheries & ocean', 'Tourism', 'Arts, culture & media'];
    var sectMiss = r.purposes.some(function (p) { return SECT.indexOf(p) >= 0; }) && !sectorHit;
    if (sectMiss && !indHit) return null;
    // eligibility rules: hard fails rule out, soft fails become near misses
    var hard = [], soft = [];
    if (ru.forprofit === false && P.forprofit) hard.push('for non-profits');
    if (ru.forprofit === true && !P.forprofit) hard.push('for for-profit businesses');
    if (ru.legal_excl && ru.legal_excl.indexOf(P.legal) >= 0 && !(ru.inc && P.legal !== 'coop')) hard.push('not for your business structure');
    var sized = !(ru.scope === 'forprofit' && !P.forprofit);   // some size limits apply to private employers only
    var incOk = P.legal === 'inc' || (P.legal === 'coop' && !(ru.legal_excl || []).length && /co-?op/i.test(r.eligibility) && !/co-?op[^.;]*(?:not|in)eligible|no co-?op/i.test(r.eligibility));
    if (ru.inc && !incOk && P.forprofit) soft.push({ k: 'inc', t: 'an incorporated business' });
    if (sized && ru.emp_max != null && P.emp[0] > ru.emp_max) hard.push('up to ' + ru.emp_max + ' employees');
    if (sized && ru.emp_min != null && P.emp[1] < ru.emp_min) soft.push({ k: 'emp', t: 'at least ' + ru.emp_min + ' employee' + (ru.emp_min > 1 ? 's' : '') });
    if (sized && ru.rev_max != null && P.rev[0] > ru.rev_max) hard.push('revenue up to ' + money(ru.rev_max));
    if (ru.proj_min != null && P.budgetHi < ru.proj_min) hard.push('projects of at least ' + money(ru.proj_min));
    if (ru.yrs_max != null && P.yrs[0] > ru.yrs_max) hard.push('new businesses only');
    if (sized && ru.rev_min != null && P.rev[1] < ru.rev_min) soft.push({ k: 'rev', t: 'annual revenue of at least ' + money(ru.rev_min) });
    if (ru.yrs_min != null && P.yrs[1] < ru.yrs_min) soft.push({ k: 'yrs', t: ru.yrs_min < 1 ? 'at least ' + Math.round(ru.yrs_min * 12) + ' months in operation' : 'at least ' + ru.yrs_min + ' year' + (ru.yrs_min > 1 ? 's' : '') + ' in operation' });
    if (hard.length) return null;
    // score (maximum 100): goals 36, industry 18, funding type 12, amount 14, intake 10, targeted group 6, anchor 4
    var g = groupOf(r), want = P.pref, goals = ans.goal || [];
    var goalN = Math.max(1, Math.min(3, goals.length));
    var share = Math.min(1, nGoals / Math.min(goalN, r.purposes.length));
    if (hitP === r.purposes.length) share = 1;                  // every purpose of the program is one of your goals
    var s = 26 + 10 * share;
    if (sectMiss) s -= 15;
    if (r.purposes.indexOf('Research & development') >= 0 && goals.indexOf('rd') < 0) s -= 10;
    if (r.purposes.indexOf('Clean technology & energy efficiency') >= 0 && r.purposes.length <= 2 && goals.indexOf('clean') < 0) s -= 10;
    s += indHit || sectorHit ? 18 : 11;
    var typeHit = r.funding_types.some(function (t) { return want.indexOf(TYPEGROUP[t]) >= 0; });
    s += typeHit ? 12 : 0;
    var need = P.budget * ((ru.pct || 50) / 100);
    s += r.max_amount_cad ? (r.max_amount_cad >= need * 0.25 ? 14 : 14 * r.max_amount_cad / (need * 0.25)) : 11;
    s += { 'Open': 10, 'Continuous intake': 10, 'Periodic intake': 6 }[r.status] || 0;
    var targeted = P.who.some(function (w) { return whoTags.indexOf(w) >= 0 && ['Exporter', 'Rural business'].indexOf(w) < 0; });
    if (targeted) s += 6;
    if (ru.anchor && goals.indexOf(ru.anchor) >= 0) s += 4;
    var niche = ru.niche && NICHE[ru.niche], nicheOk = niche && niche[0] && P.sit.indexOf(niche[0]) >= 0;
    if (ru.niche === 'cea' && P.ind === 'Agriculture & agri-food') nicheOk = true;
    if (P.ind === 'food' && /\b(?:farms?|farmers?|producers?|livestock|growers?)\b/i.test(r.eligibility) && !/process/i.test(r.eligibility + ' ' + r.summary)) s -= 15;   // farm-only programs for a food processor
    if (ru.niche === 'building' && goals.indexOf('clean') >= 0 && +ans.budget >= 4) nicheOk = true;
    if (niche && !nicheOk) s -= 20;
    if (ru.investor) s -= 15;
    if (r.confidence === 'Low') s -= 5;
    if (P.started && ru.pre) s -= 4;
    s = Math.max(5, Math.min(100, Math.round(s)));
    // explanations
    var why = [];
    why.push('Funds ' + Object.keys(hitGoals).map(function (k) { return SHORT[k]; }).join(' and '));
    if (indHit && r.industries.indexOf('All industries') < 0) why.push('Targets your industry'); else why.push('Open to all industries');
    if (targeted) why.push('Reserved for or prioritizes businesses like yours');
    if (nicheOk && niche[0]) why.push('Fits your situation: ' + niche[1]);
    if (r.status === 'Continuous intake' || r.status === 'Open') why.push('Accepting applications now'); else if (r.status === 'Periodic intake') why.push('Takes applications in intake windows');
    var check = [];
    if (niche && !nicheOk) check.push('Only for ' + niche[1]);
    if (ru.investor) check.push('The credit goes to your investors, not to the business');
    if (ru.note) check.push(ru.note);
    if (ru.inc) check.push(P.legal === 'coop' ? 'Must be an incorporated company: check whether co-operatives qualify' : 'Your business must be incorporated');
    if (ru.emp_min || ru.emp_max) check.push((ru.emp_max ? 'Size: ' + (ru.emp_min || 1) + ' to ' + ru.emp_max + ' employees' : 'At least ' + ru.emp_min + ' employee' + (ru.emp_min > 1 ? 's' : '')) + (ru.scope === 'forprofit' ? ' (businesses)' : ''));
    if (ru.rev_min) check.push('Revenue of at least ' + money(ru.rev_min));
    if (ru.yrs_min) check.push(ru.yrs_min < 1 ? 'At least ' + Math.round(ru.yrs_min * 12) + ' months in operation' : 'At least ' + ru.yrs_min + ' year' + (ru.yrs_min > 1 ? 's' : '') + ' in operation');
    if (ru.yrs_max) check.push('For businesses in their first ' + Math.round(ru.yrs_max * 12) + ' months');
    if (r.cost_share) check.push('Cost share: ' + r.cost_share);
    if (ru.pre) check.push(P.started ? 'Your project has started: costs before approval are usually not covered' : 'Apply before you spend: costs before approval are usually not covered');
    if (ru.proj_min) check.push('Minimum project size: ' + money(ru.proj_min));
    if (r.funding_types.indexOf('Repayable contribution') >= 0) check.push(r.funding_types.indexOf('Grant') >= 0 ? 'Partly repayable: some projects must pay the contribution back' : 'Repayable: the contribution is paid back, usually interest-free');
    if (ru.stack) check.push('Total government funding capped at ' + ru.stack + '% of eligible costs');
    if (r.confidence !== 'High' || ru.multi) check.push('Rules vary by stream: confirm the details on the official page');
    return { r: r, ru: ru, g: g, score: s, soft: soft, why: why, check: check, typeHit: typeHit };
  }

  var RES = null;
  function finish() {
    var P = profile(), open = [], near = [], watch = [];
    DATA.forEach(function (r) {
      var x = evaluate(r, P); if (!x) return;
      if (x.soft.length === 1 && r.status !== CLOSED && r.status !== 'Paused') { if (x.score >= 50) near.push(x); return; }
      if (x.soft.length) return;
      if (r.status === CLOSED || r.status === 'Paused') { if (x.score >= 50) watch.push(x); return; }
      open.push(x);
    });
    function byScore(a, b) { return b.score - a.score || (b.r.max_amount_cad || 0) - (a.r.max_amount_cad || 0); }
    open.sort(byScore); near.sort(byScore); watch.sort(byScore);
    var groups = {}; open.forEach(function (x) { (groups[x.g] = groups[x.g] || []).push(x); });
    var order = ['grant', 'tax', 'loan', 'adv'].sort(function (a, b) { return (P.pref.indexOf(b) >= 0) - (P.pref.indexOf(a) >= 0); });
    RES = { P: P, open: open, near: near.slice(0, 6), watch: watch.slice(0, 4), groups: groups, order: order, stack: buildStack(P, groups) };
    render();
    quiz.hidden = true; result.hidden = false; result.focus(); $('#match').scrollIntoView({ behavior: 'smooth' });
  }

  function buildStack(P, groups) {
    var pick = [], used = {}, cap = 75, gov = 0, govRep = 0;
    function estimate(x) {
      if (x.ru.per_unit || (!x.ru.pct && !x.r.max_amount_cad)) return null;   // per-person amounts or unknown amounts: say so, do not guess
      var e = P.budget * ((x.ru.pct || 50) / 100);
      if (x.r.max_amount_cad) e = Math.min(e, x.r.max_amount_cad);
      if (x.ru.per_unit) e = Math.min(e, x.ru.per_unit * P.emp[1]);
      return e;
    }
    function takeGrant(filt) {
      var list = (groups.grant || []).filter(filt);
      for (var i = 0; i < list.length; i++) {
        var x = list[i]; if (used[x.r.id]) continue;
        var c = x.ru.stack && x.ru.stack < cap ? x.ru.stack : cap, room = P.budget * c / 100 - gov - govRep;
        var e = estimate(x);
        if (e != null) { e = Math.min(e, room); if (e < 1000) continue; }      // no room left under the cap: try the next program
        used[x.r.id] = 1; cap = c; x.est = e == null ? null : Math.round(e / 1000) * 1000; x.rep = rep(x);
        if (x.est) { if (x.rep) govRep += x.est; else gov += x.est; }
        pick.push(x); return;
      }
    }
    function take(g) { var x = (groups[g] || []).filter(function (y) { return !used[y.r.id]; })[0]; if (x) { used[x.r.id] = 1; x.est = null; pick.push(x); } }
    if (P.pref.indexOf('grant') >= 0) { takeGrant(function (x) { return x.r.jurisdiction === 'Federal'; }); takeGrant(function (x) { return x.r.jurisdiction !== 'Federal'; }); }
    if (P.pref.indexOf('tax') >= 0) take('tax');
    if (P.pref.indexOf('loan') >= 0) take('loan');
    if (P.pref.indexOf('adv') >= 0) take('adv');
    return { pick: pick, cap: cap, gov: gov, govRep: govRep, budget: P.budget, share: P.budget - gov - govRep };
  }

  /* ---------- results ---------- */
  function chip(t, c) { return '<span class="fm-chip' + (c ? ' ' + c : '') + '">' + esc(t) + '</span>'; }
  function statusCls(s) { return s === 'Open' || s === 'Continuous intake' ? 'ok' : s === CLOSED ? 'no' : 'mid'; }
  function card(x) {
    var r = x.r;
    return '<article class="fm-card"><div class="fm-card-top"><div class="fm-card-h"><h4>' + esc(r.name) + '</h4><p class="fm-admin">' + esc(r.administrator) + '</p></div>' +
      '<div class="fm-fit" title="How closely the program matches your answers. Not a chance of approval."><b>' + x.score + '</b><span>fit score</span><i style="--w:' + x.score + '%"></i></div></div>' +
      '<p class="fm-chips">' + chip(r.jurisdiction) + r.funding_types.map(function (t) { return chip(t, 't'); }).join('') + chip(r.status, statusCls(r.status)) + '</p>' +
      '<p class="fm-amt">' + esc(r.amount_text) + '</p>' +
      '<div class="fm-cols"><div><h5>Why it fits</h5><ul class="fm-why">' + x.why.map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul></div>' +
      '<div><h5>Check before you apply</h5><ul class="fm-check">' + (x.check.length ? x.check : ['Confirm eligibility and eligible costs on the official page']).map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul></div></div>' +
      '<p class="fm-links"><a href="' + esc(r.url) + '" target="_blank" rel="noopener">Official program page ↗</a><a href="#p-' + esc(r.id) + '" data-fm-goto="' + esc(r.id) + '">See in directory</a><span class="muted">Deadline: ' + esc(r.deadline) + '</span></p></article>';
  }
  function render() {
    var R = RES, P = R.P;
    var n = R.open.length;
    var bl = P.exact ? full(P.budget) : row(BUDGET, ans.budget)[1].toLowerCase(), art = /^[uo]/.test(bl) ? 'an ' : 'a ';
    $('#fm-res-lead').textContent = n ? n + (n === 1 ? ' program fits' : ' programs fit') + ' your answers for ' + art + bl + ' project in ' + P.prov + '. Here are the strongest matches, grouped by type.' :
      'No open programs fit every answer. ' + (R.near.length + R.watch.length ? 'See the near misses and programs opening again below, or try ' : 'Try ') + 'more goals or funding types, or browse the directory below.';
    // summary tiles
    var tiles = R.order.map(function (g) { return '<div><strong>' + ((R.groups[g] || []).length) + '</strong><span>' + GROUPNAME[g].toLowerCase() + '</span></div>'; }).join('') +
      '<div><strong>' + R.near.length + '</strong><span>near misses</span></div>';
    $('#fm-tiles').innerHTML = tiles;
    // stack
    var S = R.stack, sh = '';
    if (S.pick.length) {
      var gp = Math.round(S.gov / S.budget * 100), rp = Math.round(S.govRep / S.budget * 100), yp = 100 - gp - rp, anyAmt = S.gov + S.govRep > 0;
      function amt(x) {
        if (x.g === 'grant') return x.est != null ? money(x.est) + (x.rep ? ' (repayable or partly repayable)' : '') : x.ru.per_unit ? 'Up to ' + money(x.ru.per_unit) + ' per participant' : 'Amount varies: check the program';
        return x.g === 'tax' ? 'Claimed after you spend' : x.g === 'loan' ? 'Financing, repayable' : 'Advice and support';
      }
      sh = '<div class="as-card fm-stack"><h3>A funding stack to explore</h3><p class="muted">Up to two grants (one federal, one provincial or territorial) and one program from each other type you chose, best fit first. Each program sets its own stacking limit, often 50% to 100% of eligible costs, and tax credits may count. As a guide we keep grants and contributions within ' + S.cap + '% of ' + (P.exact ? 'your ' + full(S.budget) + ' project (your figure).' : 'a project assumed at about ' + money(S.budget) + ' (you chose ' + esc(row(BUDGET, ans.budget)[1]) + '). Enter an exact cost for more precise amounts.') + '</p>' +
        '<table class="fm-stack-t"><thead><tr><th>Program</th><th>Type</th><th class="num">Indicative amount</th></tr></thead><tbody>' +
        S.pick.map(function (x) { return '<tr><td><a href="' + esc(x.r.url) + '" target="_blank" rel="noopener">' + esc(x.r.name) + '</a></td><td>' + esc(GROUPNAME[x.g]) + '</td><td class="num">' + esc(amt(x)) + '</td></tr>'; }).join('') + '</tbody></table>' +
        (anyAmt ? '<div class="fm-bar2" role="img" aria-label="Non-repayable funding about ' + gp + '%, repayable about ' + rp + '%, your share about ' + yp + '% of the project"><span style="width:' + gp + '%"></span><span class="r" style="width:' + rp + '%"></span></div>' +
        '<p class="fm-bar2-l">' + (S.gov ? '<span><i class="g"></i>Non-repayable: about ' + money(S.gov) + ' (' + gp + '%)</span>' : '') + (S.govRep ? '<span><i class="rr"></i>Repayable: about ' + money(S.govRep) + ' (' + rp + '%)</span>' : '') + '<span><i></i>Your share: about ' + money(S.share) + ' (' + yp + '%)</span></p>' +
        (P.cash && P.cash < yp ? '<p class="fm-warn">You said you could pay about ' + P.cash + '% yourself. This stack needs about ' + yp + '% from you up front. A loan, a tax credit claimed later or a smaller first phase can close the gap.</p>' : '') +
        (!P.cash ? '<p class="fm-small muted">You were not sure how much you could pay yourself. Most programs need your share in cash, so check this before you apply.</p>' : '') : '') +
        '<p class="muted fm-small">Indicative only, based on each program\'s usual share and maximum. Programs decide the real amount, and most pay after you spend. Some programs count tax credits toward their stacking limit too.</p></div>';
    }
    $('#fm-stack').innerHTML = sh;
    // groups
    $('#fm-groups').innerHTML = R.order.filter(function (g) { return (R.groups[g] || []).length; }).map(function (g) {
      var list = R.groups[g], top = list.slice(0, 3), rest = list.slice(3);
      return '<section class="fm-group"><div class="fm-group-h"><h3>' + esc(GROUPNAME[g]) + '</h3><span class="muted">' + list.length + ' match' + (list.length > 1 ? 'es' : '') + (P.pref.indexOf(g) < 0 ? ' · not a type you picked' : '') + '</span></div>' +
        top.map(card).join('') + (rest.length ? '<div hidden>' + rest.map(card).join('') + '</div><button type="button" class="btn btn-ghost fm-more" data-fm="more">Show ' + rest.length + ' more</button>' : '') + '</section>';
    }).join('');
    // near misses
    $('#fm-near').innerHTML = R.near.length ? '<div class="as-card"><h3>Near misses</h3><p class="muted">These fit your project, but each one has a requirement you do not meet yet. Plan for them as you grow.</p><ul class="fm-near">' +
      R.near.map(function (x) { var s = x.soft[0]; return '<li><a href="' + esc(x.r.url) + '" target="_blank" rel="noopener">' + esc(x.r.name) + '</a><span>Needs ' + esc(s.t) + '. This is the only rule we found that you do not meet yet. Check the other requirements on the official page.</span></li>'; }).join('') + '</ul></div>' : '';
    // watch list
    $('#fm-watch').innerHTML = R.watch.length ? '<div class="as-card"><h3>Watch for the next intake</h3><p class="muted">Strong fits that are closed to new applications right now.</p><ul class="fm-near">' +
      R.watch.map(function (x) { return '<li><a href="' + esc(x.r.url) + '" target="_blank" rel="noopener">' + esc(x.r.name) + '</a><span>' + esc(x.r.deadline) + '</span></li>'; }).join('') + '</ul></div>' : '';
    // readiness
    var have = ans.ready || [], todo = [];
    if (P.legal === 'none' || P.legal === 'sole' || P.legal === 'part' || (P.legal === 'coop' && R.near.some(function (x) { return x.soft[0].k === 'inc'; }))) todo.push(['Consider incorporating', 'Some programs, such as NRC IRAP, fund incorporated businesses only. Others accept partnerships or co-operatives. Ask your accountant whether incorporating makes sense for you.']);
    if (have.indexOf('bn') < 0) todo.push(['Get a CRA business number', 'Almost every federal and provincial program asks for it. Register online with the Canada Revenue Agency.']);
    if (have.indexOf('fs') < 0) todo.push(['Prepare financial statements', 'Funders check that you can carry your share of the project. Ask your bookkeeper for the last full year.']);
    if (have.indexOf('plan') < 0) todo.push(['Write a project plan and budget', 'Scope, milestones, quotes and the results you expect. This is the core of every application.']);
    if (have.indexOf('cash') < 0) todo.push(['Plan your cash flow', 'Most programs reimburse costs after you pay them, often months later. Line up cash or a credit facility first.']);
    todo.push([P.started ? 'Talk to the program before you spend more' : 'Do not spend before approval', 'Costs incurred before a funding agreement is signed are usually not covered.']);
    todo.push(['Disclose all government funding', 'Applications ask for every other public source on the project, so funders can apply stacking limits.']);
    $('#fm-ready').innerHTML = '<div class="as-card"><h3>Your readiness checklist</h3><ol class="fm-todo">' + todo.map(function (t) { return '<li><b>' + esc(t[0]) + '</b><span>' + esc(t[1]) + '</span></li>'; }).join('') + '</ol></div>';
    REP = report();
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-fm-goto]'); if (!a) return;
    var card = document.getElementById('p-' + a.dataset.fmGoto); if (!card) return;
    e.preventDefault();
    if (card.hidden) { var clr = document.querySelector('#gr-finder [data-clear]'); if (clr) clr.click(); }
    if (card.hidden) { var cl = document.getElementById('gr-closed'); if (cl) { cl.checked = true; cl.dispatchEvent(new Event('change', { bubbles: true })); } }
    var d = card.querySelector('details'); if (d) d.open = true;
    card.scrollIntoView({ behavior: 'smooth', block: 'center' }); card.tabIndex = -1; card.focus({ preventScroll: true }); card.classList.add('fm-flash'); setTimeout(function () { card.classList.remove('fm-flash'); }, 2200);
  });

  /* ---------- report text and PDF (same report service as the Digital Assessment) ---------- */
  var REP = null, SITE = 'https://www.chmltech.com/';
  function report() {
    var R = RES, P = R.P, secs = [];
    var lab = function (list, k) { var x = row(list, k); return x ? x[1] : k; };
    secs.push(['1. Your answers', [
      'Location: ' + P.prov + (P.region ? ' (' + lab([['north', 'Northern Ontario'], ['east', 'Eastern Ontario'], ['southwest', 'Southwestern Ontario'], ['central', 'Toronto and central Ontario']], P.region) + ')' : ''), 'Industry: ' + lab(IND, ans.ind), 'Business set-up: ' + lab(LEGAL, ans.legal), 'Employees: ' + lab(EMP, ans.emp),
      ans.legal !== 'none' ? 'Revenue: ' + lab(REV, ans.rev) : '', ans.legal !== 'none' ? 'Years operating: ' + lab(YRS, ans.yrs) : '',
      'Funding for: ' + (ans.goal || []).map(function (g) { return lab(GOALS, g); }).join('; '), 'Project cost: ' + (ans.cost ? '$' + ans.cost.toLocaleString('en-CA') + ' (your figure)' : lab(BUDGET, ans.budget)), 'Start: ' + lab(START, ans.start),
      P.sit.length ? 'Situation: ' + P.sit.map(function (k) { return { tariff: 'affected by U.S. tariffs', defence: 'defence or security supplier', energy: 'large energy user' }[k]; }).join('; ') : '',
      P.who.length ? 'About you: ' + P.who.map(function (w) { return lab(WHO, w); }).join('; ') : '',
      'Funding types: ' + (ans.pref || []).map(function (g) { return lab(PREF, g); }).join('; '), 'Your cash share: ' + lab(CASH, ans.cash), 'In place: ' + (ans.ready || []).map(function (g) { return lab(READY, g); }).join('; ')].filter(Boolean).join('\n')]);
    var S = R.stack;
    if (S.pick.length) secs.push(['2. A funding stack to explore', S.pick.map(function (x, i) { return (i + 1) + '. ' + x.r.name + ' (' + GROUPNAME[x.g] + '): ' + (x.est != null ? 'about ' + money(x.est) + (x.rep ? ' (repayable or partly repayable)' : '') : x.g === 'grant' ? 'amount varies' : x.g === 'tax' ? 'claimed after you spend' : x.g === 'loan' ? 'repayable financing' : 'advice and support') + '\n   ' + x.r.url; }).join('\n') +
      '\n\nNon-repayable: about ' + money(S.gov) + (S.govRep ? '; repayable: about ' + money(S.govRep) : '') + ' of ' + (P.exact ? 'your ' + full(S.budget) : 'a project assumed at ' + money(S.budget)) + (P.exact ? ' project' : '') + ' (kept within ' + S.cap + '% of the project cost). Your share: about ' + money(S.share) + '. Indicative only; each program decides the real amount.']);
    var n = 3;
    R.order.forEach(function (g) {
      var list = (R.groups[g] || []).slice(0, 5); if (!list.length) return;
      secs.push([(n++) + '. ' + GROUPNAME[g], list.map(function (x, i) {
        return (i + 1) + '. ' + x.r.name + ' (fit score ' + x.score + '/100)\n   ' + x.r.administrator + ' | ' + x.r.status + '\n   Amount: ' + x.r.amount_text + '\n   Why it fits: ' + x.why.join('; ') + '\n   Check: ' + (x.check.join('; ') || 'confirm on the official page') + '\n   ' + x.r.url;
      }).join('\n\n')]);
    });
    if (R.near.length) secs.push([(n++) + '. Near misses', R.near.map(function (x) { return '- ' + x.r.name + ': needs ' + x.soft[0].t + '. ' + x.r.url; }).join('\n')]);
    if (R.watch.length) secs.push([(n++) + '. Watch for the next intake', R.watch.map(function (x) { return '- ' + x.r.name + ': ' + x.r.deadline; }).join('\n')]);
    secs.push([(n++) + '. Readiness checklist', $$('#fm-ready li').map(function (li) { return '- ' + li.querySelector('b').textContent + ': ' + li.querySelector('span').textContent; }).join('\n')]);
    secs.push([(n++) + '. Important', 'This report is a starting point, not a decision on eligibility. Programs, amounts and deadlines change often. Confirm every rule on the official program page before you apply. Chmltech is not affiliated with any government program and does not decide funding applications. Program data checked November 2026.']);
    return { secs: secs };
  }
  function loadJsPDF() {
    if (window.jspdf) return Promise.resolve(window.jspdf);
    return new Promise(function (ok, no) { var sc = document.createElement('script'); sc.src = 'assets/js/vendor/jspdf.umd.min.js'; sc.onload = function () { window.jspdf ? ok(window.jspdf) : no(); }; sc.onerror = no; document.head.appendChild(sc); });
  }
  function logoData() {
    var im = document.querySelector('.brand img'); if (!im || !im.naturalWidth) return null;
    try { var c = document.createElement('canvas'); c.width = im.naturalWidth; c.height = im.naturalHeight; c.getContext('2d').drawImage(im, 0, 0); return { d: c.toDataURL('image/png'), r: im.naturalWidth / im.naturalHeight }; } catch (e) { return null; }
  }
  function pdfTxt(x) { return String(x).replace(/→/g, 'to').replace(/↗/g, '').replace(/≥/g, '>=').replace(/≤/g, '<=').replace(/œ/g, 'oe').replace(/Œ/g, 'OE').replace(/[^\x00-\xff–—‘’“”•…€™ŠšŽžŸƒ]/g, ''); }
  function makePdf() {
    if (!REP) return Promise.reject();
    return loadJsPDF().then(function (J) {
      var doc = new J.jsPDF({ unit: 'mm', format: 'a4' }), W = 210, M = 18, CW = W - 2 * M, y = 0, logo = logoData();
      var NAVY = [11, 42, 90], MUT = [90, 100, 117], LINE = [214, 220, 230], TINT = [232, 238, 247];
      var who = ($('#fm-name') || {}).value || '', co = ($('#fm-co') || {}).value || '';
      var date = new Date().toLocaleDateString('en-CA', { year: 'numeric', month: 'long', day: 'numeric' });
      function col(c) { doc.setTextColor(c[0], c[1], c[2]); }
      function head() {
        if (logo) doc.addImage(logo.d, 'PNG', M, 9, 12 * logo.r, 12, 'chmllogo', 'FAST');
        doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5); col(MUT);
        doc.text('Funding Match  |  Funding report', W - M, 15, { align: 'right' }); doc.text(date, W - M, 19, { align: 'right' });
        doc.setDrawColor(NAVY[0], NAVY[1], NAVY[2]); doc.setLineWidth(0.6); doc.line(M, 24, W - M, 24); y = 32;
      }
      function room(h) { if (y + h > 274) { doc.addPage(); head(); } }
      function para(txt, o) {
        o = o || {}; var size = o.size || 9.6, lh = size * 0.47, x = M + (o.ind || 0), w = CW - (o.ind || 0);
        doc.setFontSize(size); doc.setFont('helvetica', o.bold ? 'bold' : 'normal');
        var lines = doc.splitTextToSize(txt, w);
        if (o.hang && lines.length > 1) lines = [lines[0]].concat(doc.splitTextToSize(lines.slice(1).join(' '), w - o.hang));
        room(lh * lines.length + 1);
        lines.forEach(function (ln, i) {
          col(o.color || [40, 48, 62]); doc.text(ln, x + (i && o.hang ? o.hang : 0), y);
          y += lh;
        });
      }
      head();
      doc.setFillColor(NAVY[0], NAVY[1], NAVY[2]); doc.rect(M, y - 4, CW, 30, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(21); doc.setTextColor(255, 255, 255); doc.text('Your Funding Match', M + 7, y + 7);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.text(pdfTxt('Prepared for ' + ([who, co].filter(Boolean).join(', ') || 'your business') + '  |  ' + RES.P.prov), M + 7, y + 15);
      doc.text(pdfTxt('Chmltech Funding Match  |  ' + date), M + 7, y + 21);
      y += 30;
      doc.setFont('helvetica', 'italic'); doc.setFontSize(8.5); col(MUT); doc.text('A starting point, not a decision on eligibility. Confirm every rule on the official program page before you apply.', M, y); y += 6;
      REP.secs.forEach(function (sec) {
        room(28); y += 3; doc.setFont('helvetica', 'bold'); doc.setFontSize(13); col(NAVY); doc.text(pdfTxt(sec[0]), M, y);
        doc.setDrawColor(LINE[0], LINE[1], LINE[2]); doc.setLineWidth(0.3); doc.line(M, y + 2, W - M, y + 2); y += 8;
        String(sec[1]).split('\n').forEach(function (ln) {
          if (!ln.trim()) { y += 2.5; return; }
          var t = pdfTxt(ln);
          var u = /^\s*(https?:\/\/\S+)\s*$/.exec(ln);
          if (u) { room(6); doc.setFontSize(9.6); doc.setFont('helvetica', 'bold'); doc.setTextColor(11, 111, 164); doc.textWithLink('Official program page', M + 5, y, { url: u[1] }); y += 4.5; return; }
          if (/^\d+\. /.test(t) && !/^\s/.test(ln)) { room(/\n {3}/.test(sec[1]) ? 40 : 14); y += 1; para(t, { bold: true, color: NAVY, size: 10, hang: 4 }); return; }
          if (/^- /.test(t)) { var uu = /(https?:\/\/\S+)$/.exec(t); para('•  ' + (uu ? t.slice(2, uu.index).replace(/[\s.]+$/, '') : t.slice(2)), { ind: 2, hang: 4 }); if (uu) { room(6); doc.setFontSize(9.6); doc.setFont('helvetica', 'bold'); doc.setTextColor(11, 111, 164); doc.textWithLink('Official program page', M + 6, y, { url: uu[1] }); y += 4.5; } return; }
          para(t.trim(), { ind: /^\s{3}/.test(ln) ? 5 : 0 });
        });
        y += 2;
      });
      room(30); y += 4;
      doc.setFillColor(TINT[0], TINT[1], TINT[2]); doc.rect(M, y, CW, 20, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(11); col(NAVY); doc.text('Get your project ready for funding', M + 6, y + 8);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(9.5); doc.text('Free 30-minute funding review:  www.chmltech.com/book   |   info@chmltech.com', M + 6, y + 14.5);
      doc.link(M, y, CW, 20, { url: SITE + 'book' });
      var np = doc.getNumberOfPages();
      for (var i = 1; i <= np; i++) {
        doc.setPage(i); doc.setDrawColor(LINE[0], LINE[1], LINE[2]); doc.setLineWidth(0.3); doc.line(M, 283, W - M, 283);
        doc.setFont('helvetica', 'normal'); doc.setFontSize(8); col(MUT);
        doc.text('Chmltech Ltd.  |  Vancouver, BC  |  www.chmltech.com', M, 288); doc.text('Page ' + i + ' of ' + np, W - M, 288, { align: 'right' });
      }
      doc.setProperties({ title: 'Your Funding Match — Chmltech', author: 'Chmltech Ltd.', subject: 'Funding Match report' });
      var slug = (co || 'Report').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '').slice(0, 40) || 'Report';
      return { doc: doc, file: 'Chmltech_Funding_Match_' + slug + '.pdf' };
    });
  }
  window.ChmlReportText = function () { return REP ? REP.secs.map(function (x) { return x[0] + '\n' + x[1]; }).join('\n\n') : ''; };
  window.ChmlReportIndustry = function () { var x = row(IND, ans.ind); return x ? x[1] : ''; };
  window.ChmlReportPdf = function () { return makePdf().then(function (o) { return { blob: o.doc.output('blob'), file: o.file }; }); };
  // Only one report tool (Digital Assessment or Funding Match) may load per page: they share the ChmlReport* globals.
  if (/[?&]fmtest=1/.test(location.search)) window.ChmlFundingMatchTest = { evaluate: evaluate, profile: profile, setAnswers: function (a) { ans = a; }, finish: finish, res: function () { return RES; } };
})();
