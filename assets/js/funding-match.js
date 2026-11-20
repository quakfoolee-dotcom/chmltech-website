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
  function money(n) { if (n == null) return ''; if (n >= 1e6) return '$' + (+(n / 1e6).toFixed(n % 1e6 ? 1 : 0)) + 'M'; if (n >= 1e3) return '$' + Math.round(n / 1e3) + 'K'; return '$' + n; }
  var CLOSED = 'Closed to new applications';

  /* ---------- questions ---------- */
  var PROV = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'New Brunswick', 'Nova Scotia', 'Prince Edward Island', 'Newfoundland and Labrador', 'Yukon', 'Northwest Territories', 'Nunavut'];
  var IND = [['Manufacturing', 'Manufacturing'], ['Construction', 'Construction and trades'], ['Retail & wholesale', 'Retail, wholesale and distribution'], ['Transportation & logistics', 'Transportation, warehousing and logistics'],
    ['Technology & digital', 'Software, IT and digital'], ['Professional services', 'Professional and business services'], ['Life sciences & health', 'Health care and life sciences'], ['Tourism & hospitality', 'Tourism, food service and hospitality'],
    ['Agriculture & agri-food', 'Agriculture and food processing'], ['Clean technology', 'Clean technology'], ['Mining & energy', 'Mining, oil, gas and energy'], ['Forestry', 'Forestry and wood products'],
    ['Fisheries & aquaculture', 'Fisheries and aquaculture'], ['Aerospace & defence', 'Aerospace and defence'], ['Automotive', 'Automotive'], ['Arts, culture & media', 'Arts, culture and media'], ['other', 'Something else']];
  var LEGAL = [['inc', 'Incorporated company', 'Federal or provincial corporation'], ['sole', 'Sole proprietor', 'Registered business name, not incorporated'], ['part', 'Partnership'], ['coop', 'Co-operative'], ['npo', 'Non-profit or charity'], ['none', 'Not registered yet', 'Planning to start a business']];
  var EMP = [['0', 'Just me', 0, 0], ['1', '1 to 2', 1, 2], ['3', '3 to 4', 3, 4], ['5', '5 to 9', 5, 9], ['10', '10 to 49', 10, 49], ['50', '50 to 99', 50, 99], ['100', '100 to 249', 100, 249], ['250', '250 to 499', 250, 499], ['500', '500 or more', 500, 1e6]];
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
  var PREF = [['grant', 'Grants and contributions', 'Money you do not repay'], ['tax', 'Tax credits', 'Claimed with your tax return after you spend'], ['loan', 'Loans and financing', 'Repayable, often on better terms than a bank'], ['adv', 'Advice and expert help', 'Advisors, coaching, subsidised consultants']];
  var CASH = [['25', 'About 25% or more'], ['50', 'About 50% or more'], ['75', '75% or more'], ['0', 'Not sure yet']];
  var READY = [['bn', 'A CRA business number'], ['fs', 'Financial statements for the last year'], ['plan', 'A written project plan and budget'], ['cash', 'Cash to pay costs first and claim them back later'], ['nil', 'None of these yet']];
  var TYPEGROUP = { 'Grant': 'grant', 'Repayable contribution': 'grant', 'Voucher': 'grant', 'Wage subsidy': 'grant', 'Rebate/Incentive': 'grant', 'Tax credit': 'tax', 'Loan': 'loan', 'Loan guarantee': 'loan', 'Equity investment': 'loan', 'Advisory service': 'adv' };
  var GROUPNAME = { grant: 'Grants and contributions', tax: 'Tax credits', loan: 'Loans and financing', adv: 'Advice and expert help' };

  var STEPS = ['Your business', 'Your project', 'About you', 'Funding type', 'Readiness'];
  function opt(a) { return a.map(function (x) { return [x[0], x[1], typeof x[2] === 'string' ? x[2] : '']; }); }
  var SCREENS = [
    { k: 'prov', st: 0, q: 'Where does your business operate?', hint: 'Pick the province or territory where the project will happen.', o: function () { return PROV.map(function (p) { return [p, p]; }); }, cols: 2 },
    { k: 'ind', st: 0, q: 'Which industry best describes your business?', o: function () { return IND; }, cols: 2 },
    { k: 'legal', st: 0, q: 'How is your business set up?', hint: 'Many programs only fund incorporated businesses.', o: function () { return opt(LEGAL); } },
    { k: 'emp', st: 0, q: 'How many people work in the business?', hint: 'Count full-time equivalents in Canada, including you.', o: function () { return opt(EMP); }, cols: 3 },
    { k: 'rev', st: 0, q: 'What was your revenue in the last full year?', o: function () { return opt(REV); }, cols: 2, when: function () { return ans.legal !== 'none'; } },
    { k: 'yrs', st: 0, q: 'How long has the business been operating?', o: function () { return opt(YRS); }, cols: 3, when: function () { return ans.legal !== 'none'; } },
    { k: 'goal', st: 1, q: 'What do you want funding for?', hint: 'Pick up to three.', max: 3, o: function () { return GOALS.map(function (g) { return [g[0], g[1], g[2]]; }); } },
    { k: 'budget', st: 1, q: 'About how much will the project cost in total?', o: function () { return BUDGET.map(function (b) { return [b[0], b[1], '']; }); } },
    { k: 'start', st: 1, q: 'When will the project start?', hint: 'Most grants only cover costs after approval.', o: function () { return opt(START); } },
    { k: 'who', st: 2, q: 'Do any of these describe your business?', hint: 'Optional. Some programs are reserved for these groups. Pick all that apply, or "None of these".', max: 9, o: function () { return opt(WHO); }, cols: 2, excl: 'none' },
    { k: 'pref', st: 3, q: 'What kind of funding would you consider?', hint: 'Pick all that apply.', max: 4, o: function () { return opt(PREF); } },
    { k: 'cash', st: 3, q: 'How much of the project cost could you pay yourself?', hint: 'Most programs share costs. Your share usually has to be cash.', o: function () { return opt(CASH); } },
    { k: 'ready', st: 4, q: 'What do you already have in place?', hint: 'Pick all that apply.', max: 5, o: function () { return opt(READY); }, excl: 'nil' }];

  var ans = {}, idx = 0;
  var intro = $('#fm-intro'), quiz = $('#fm-quiz'), result = $('#fm-result'), qbox = $('#fm-qbox'), next = $('#fm-next'), back = $('#fm-back');
  function visible() { return SCREENS.filter(function (s) { return !s.when || s.when(); }); }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-fm]'); if (!t) return;
    var a = t.dataset.fm;
    if (a === 'start' || a === 'restart') { e.preventDefault(); ans = {}; idx = 0; intro.hidden = true; result.hidden = true; quiz.hidden = false; show(); $('#match').scrollIntoView({ behavior: 'smooth' }); }
    if (a === 'more') { var box = t.previousElementSibling; box.hidden = false; t.remove(); }
    if (a === 'print') {
      var lbl = t.textContent; t.disabled = true; t.textContent = 'Preparing PDF…';
      makePdf().then(function (o) { o.doc.save(o.file); }).catch(function () { window.print(); }).then(function () { t.disabled = false; t.textContent = lbl; });
    }
  });
  function show() {
    var list = visible(), s = list[idx];
    $('#fm-steps').innerHTML = STEPS.map(function (n, i) { return '<li class="' + (i === s.st ? 'on' : i < s.st ? 'done' : '') + '">' + (i + 1) + '. ' + n + '</li>'; }).join('');
    $('#fm-bar').style.width = (idx / list.length * 100) + '%';
    $('#fm-qcount').textContent = 'Question ' + (idx + 1) + ' of ' + list.length;
    var multi = !!s.max, sel = ans[s.k] || (multi ? [] : '');
    qbox.innerHTML = '<legend class="finder-qtext h-md" style="font-size:24px">' + esc(s.q) + '</legend>' + (s.hint ? '<p class="erp-qhint">' + esc(s.hint) + '</p>' : '') +
      '<div class="finder-opts' + (s.cols ? ' fm-cols' + s.cols : '') + '">' + s.o().map(function (o) {
        var on = multi ? sel.indexOf(o[0]) >= 0 : sel === o[0];
        return '<label class="finder-opt"><input type="' + (multi ? 'checkbox' : 'radio') + '" name="fq_' + s.k + '" value="' + esc(o[0]) + '"' + (on ? ' checked' : '') + '><span>' + esc(o[1]) + (o[2] ? '<small>' + esc(o[2]) + '</small>' : '') + '</span></label>';
      }).join('') + '</div>';
    back.disabled = idx === 0;
    next.textContent = idx === list.length - 1 ? 'See my funding matches →' : 'Next →';
    update();
  }
  qbox.addEventListener('change', function (e) {
    var s = visible()[idx];
    if (s.max) {
      if (s.excl) {
        if (e.target.value === s.excl && e.target.checked) $$('input', qbox).forEach(function (b) { if (b.value !== s.excl) b.checked = false; });
        else if (e.target.checked) $$('input', qbox).forEach(function (b) { if (b.value === s.excl) b.checked = false; });
      }
      var boxes = $$('input:checked', qbox);
      if (boxes.length > s.max) { e.target.checked = false; boxes = $$('input:checked', qbox); }
      ans[s.k] = boxes.map(function (b) { return b.value; });
    } else { ans[s.k] = e.target.value; if (s.k === 'legal' && ans.legal === 'none') { ans.rev = '0'; ans.yrs = '0'; } }
    update();
  });
  function update() { var v = ans[visible()[idx].k]; next.disabled = !(v && v.length); }
  back.addEventListener('click', function () { if (idx > 0) { idx--; show(); } });
  next.addEventListener('click', function () { if (idx < visible().length - 1) { idx++; show(); window.scrollTo({ top: $('#match').offsetTop - 70, behavior: 'smooth' }); } else finish(); });
  qbox.addEventListener('dblclick', function (e) { if (e.target.closest('.finder-opt') && !visible()[idx].max && !next.disabled) next.click(); });

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
    var purposes = {}, sector = SECTOR_PURPOSE[ans.ind];
    (ans.goal || []).forEach(function (g) { row(GOALS, g)[3].forEach(function (p) { purposes[p] = purposes[p] || g; }); });
    return { prov: ans.prov, ind: ans.ind, legal: ans.legal, forprofit: forprofit, inc: ans.legal === 'inc' || ans.legal === 'coop', emp: [e[2], e[3]], rev: [r[2], r[3]], yrs: [y[2], y[3]],
      types: types.concat(who), who: who, purposes: purposes, sector: sector, budget: row(BUDGET, ans.budget)[2], budgetHi: row(BUDGET, ans.budget)[3], pref: ans.pref || [], started: ans.start === 'started', cash: +ans.cash };
  }
  function inProv(r, P) { if (r.jurisdiction === P.prov) return true; if (r.jurisdiction !== 'Federal') return false; return r.provinces.indexOf('All') >= 0 || r.provinces.indexOf(P.prov) >= 0; }
  function groupOf(r) { var g = r.funding_types.map(function (t) { return TYPEGROUP[t]; }); return ['grant', 'tax', 'loan', 'adv'].filter(function (x) { return g.indexOf(x) >= 0; })[0] || 'grant'; }
  function evaluate(r, P) {
    if (!inProv(r, P)) return null;
    var ru = RULES[r.id] || {};
    var indOk = r.industries.indexOf('All industries') >= 0 || r.industries.indexOf(P.ind) >= 0;
    if (!indOk) return null;
    var typeOk = r.applicant_types.some(function (t) { return P.types.indexOf(t) >= 0; });
    if (!typeOk) return null;
    // purposes
    var hitGoals = {}, sectorHit = false;
    r.purposes.forEach(function (p) { if (P.purposes[p]) hitGoals[P.purposes[p]] = 1; if (p === P.sector) sectorHit = true; });
    var nGoals = Object.keys(hitGoals).length;
    if (!nGoals) return null;
    // sector programs (farming, fisheries, tourism, arts) only for that sector
    var SECT = ['Agriculture & agri-food', 'Fisheries & ocean', 'Tourism', 'Arts, culture & media'];
    var sectMiss = r.purposes.some(function (p) { return SECT.indexOf(p) >= 0; }) && !r.purposes.some(function (p) { return p === P.sector; });
    if (sectMiss && r.industries.indexOf(P.ind) < 0) return null;
    // eligibility rules: hard fails rule out, soft fails become near misses
    var hard = [], soft = [];
    if (ru.forprofit === false && P.forprofit) hard.push('for non-profits');
    if (ru.forprofit === true && !P.forprofit) hard.push('for for-profit businesses');
    if (ru.inc && !P.inc && P.forprofit) soft.push({ k: 'inc', t: 'an incorporated business' });
    if (ru.emp_max != null && P.emp[0] > ru.emp_max) hard.push('up to ' + ru.emp_max + ' employees');
    if (ru.emp_min != null && P.emp[1] < ru.emp_min) soft.push({ k: 'emp', t: 'at least ' + ru.emp_min + ' employee' + (ru.emp_min > 1 ? 's' : '') });
    if (ru.rev_max != null && P.rev[0] > ru.rev_max) hard.push('revenue up to ' + money(ru.rev_max));
    if (ru.proj_min != null && P.budgetHi < ru.proj_min) hard.push('projects of at least ' + money(ru.proj_min));
    if (ru.rev_min != null && P.rev[1] < ru.rev_min) soft.push({ k: 'rev', t: 'annual revenue of at least ' + money(ru.rev_min) });
    if (ru.yrs_min != null && P.yrs[1] < ru.yrs_min) soft.push({ k: 'yrs', t: ru.yrs_min < 1 ? 'at least ' + Math.round(ru.yrs_min * 12) + ' months in operation' : 'at least ' + ru.yrs_min + ' year' + (ru.yrs_min > 1 ? 's' : '') + ' in operation' });
    if (hard.length) return null;
    // score
    var g = groupOf(r), want = P.pref;
    var goalN = Math.max(1, Math.min(3, (ans.goal || []).length));
    var s = nGoals >= 2 || goalN === 1 ? 40 : 32;
    // programs built around R&D or clean technology fit best when that is the goal
    if (sectMiss) s -= 15;
    if (r.purposes.indexOf('Research & development') >= 0 && (ans.goal || []).indexOf('rd') < 0) s -= 10;
    if (r.purposes.indexOf('Clean technology & energy efficiency') >= 0 && r.purposes.length <= 2 && (ans.goal || []).indexOf('clean') < 0) s -= 10;
    s += r.industries.indexOf(P.ind) >= 0 || sectorHit ? 20 : 12;
    var typeHit = r.funding_types.some(function (t) { return want.indexOf(TYPEGROUP[t]) >= 0; });
    s += typeHit ? 15 : 0;
    var need = P.budget * ((ru.pct || 50) / 100);
    s += r.max_amount_cad ? (r.max_amount_cad >= need * 0.25 ? 15 : 15 * r.max_amount_cad / (need * 0.25)) : 8;
    s += { 'Open': 10, 'Continuous intake': 10, 'Periodic intake': 6, 'Paused': 2 }[r.status] || 0;
    if (P.who.some(function (w) { return r.applicant_types.indexOf(w) >= 0; })) s += 6;
    if (r.confidence === 'Low') s -= 5;
    if (P.started && ru.pre) s -= 4;
    s = Math.max(5, Math.min(99, Math.round(s)));
    // explanations
    var why = [];
    var goalNames = Object.keys(hitGoals).map(function (k) { return SHORT[k]; });
    why.push('Funds ' + goalNames.join(' and '));
    if (r.industries.indexOf(P.ind) >= 0) why.push('Targets your industry'); else why.push('Open to all industries');
    if (P.who.some(function (w) { return r.applicant_types.indexOf(w) >= 0; })) why.push('Reserved for or prioritises businesses like yours');
    if (r.status === 'Continuous intake' || r.status === 'Open') why.push('Accepting applications now'); else if (r.status === 'Periodic intake') why.push('Takes applications in intake windows');
    var check = [];
    if (ru.inc) check.push('Your business must be incorporated');
    if (ru.emp_min || ru.emp_max) check.push('Size: ' + (ru.emp_min ? ru.emp_min : 1) + ' to ' + (ru.emp_max || 'any number of') + ' employees');
    if (ru.rev_min) check.push('Revenue of at least ' + money(ru.rev_min));
    if (ru.yrs_min) check.push(ru.yrs_min < 1 ? 'At least ' + Math.round(ru.yrs_min * 12) + ' months in operation' : 'At least ' + ru.yrs_min + ' years in operation');
    if (r.cost_share) check.push('Cost share: ' + r.cost_share);
    if (ru.pre) check.push(P.started ? 'Your project has started: costs before approval are usually not covered' : 'Apply before you spend: costs before approval are usually not covered');
    if (ru.proj_min) check.push('Minimum project size: ' + money(ru.proj_min));
    if (r.funding_types.indexOf('Repayable contribution') >= 0 && r.funding_types.indexOf('Grant') < 0) check.push('Repayable: the contribution is paid back, usually interest-free');
    if (ru.stack) check.push('Total government funding capped at ' + ru.stack + '% of project costs');
    if (r.confidence !== 'High' || ru.multi) check.push('Rules vary by stream: confirm the details on the official page');
    return { r: r, ru: ru, g: g, score: s, soft: soft, why: why, check: check, typeHit: typeHit };
  }

  var RES = null;
  function finish() {
    var P = profile(), open = [], near = [], watch = [];
    DATA.forEach(function (r) {
      var x = evaluate(r, P); if (!x) return;
      if (x.soft.length === 1 && r.status !== CLOSED) { if (x.score >= 50) near.push(x); return; }
      if (x.soft.length) return;
      if (r.status === CLOSED) { if (x.score >= 50) watch.push(x); return; }
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
    var pick = [], used = {};
    function take(g, n, filt) { (groups[g] || []).filter(filt || function () { return true; }).slice(0, n).forEach(function (x) { if (!used[x.r.id]) { used[x.r.id] = 1; pick.push(x); } }); }
    if (P.pref.indexOf('grant') >= 0) { take('grant', 1, function (x) { return x.r.jurisdiction === 'Federal'; }); take('grant', 1, function (x) { return x.r.jurisdiction !== 'Federal'; }); }
    if (P.pref.indexOf('tax') >= 0) take('tax', 1);
    if (P.pref.indexOf('loan') >= 0) take('loan', 1);
    if (P.pref.indexOf('adv') >= 0) take('adv', 1);
    var cap = 75; pick.forEach(function (x) { if (x.ru.stack && x.ru.stack < cap) cap = x.ru.stack; });
    var gov = 0;
    pick.forEach(function (x) {
      if (x.g !== 'grant') { x.est = null; return; }
      var pct = (x.ru.pct || 50) / 100, e = P.budget * pct; if (x.r.max_amount_cad) e = Math.min(e, x.r.max_amount_cad);
      e = Math.min(e, Math.max(0, P.budget * cap / 100 - gov)); x.est = Math.round(e / 1000) * 1000; gov += x.est;
    });
    return { pick: pick, cap: cap, gov: gov, budget: P.budget, share: P.budget - gov };
  }

  /* ---------- results ---------- */
  function rep(x) { return x.r.funding_types.indexOf('Repayable contribution') >= 0 && x.r.funding_types.indexOf('Grant') < 0; }
  function chip(t, c) { return '<span class="fm-chip' + (c ? ' ' + c : '') + '">' + esc(t) + '</span>'; }
  function statusCls(s) { return s === 'Open' || s === 'Continuous intake' ? 'ok' : s === CLOSED ? 'no' : 'mid'; }
  function card(x) {
    var r = x.r;
    return '<article class="fm-card"><div class="fm-card-top"><div class="fm-card-h"><h4>' + esc(r.name) + '</h4><p class="fm-admin">' + esc(r.administrator) + '</p></div>' +
      '<div class="fm-fit" title="How well this program fits your answers"><b>' + x.score + '%</b><span>fit</span><i style="--w:' + x.score + '%"></i></div></div>' +
      '<p class="fm-chips">' + chip(r.jurisdiction) + r.funding_types.map(function (t) { return chip(t, 't'); }).join('') + chip(r.status, statusCls(r.status)) + '</p>' +
      '<p class="fm-amt">' + esc(r.amount_text) + '</p>' +
      '<div class="fm-cols"><div><h5>Why it fits</h5><ul class="fm-why">' + x.why.map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul></div>' +
      '<div><h5>Check before you apply</h5><ul class="fm-check">' + (x.check.length ? x.check : ['Confirm eligibility and eligible costs on the official page']).map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul></div></div>' +
      '<p class="fm-links"><a href="' + esc(r.url) + '" target="_blank" rel="noopener">Official program page ↗</a><a href="#p-' + esc(r.id) + '" data-fm-goto="' + esc(r.id) + '">See in directory</a><span class="muted">Deadline: ' + esc(r.deadline) + '</span></p></article>';
  }
  function render() {
    var R = RES, P = R.P;
    var n = R.open.length;
    $('#fm-res-lead').textContent = n ? n + ' programs fit your answers for a ' + row(BUDGET, ans.budget)[1].toLowerCase() + ' project in ' + P.prov + '. Here are the strongest matches, grouped by type.' :
      'No open programs fit every answer. See the near misses and programs opening again below, or widen your funding types.';
    // summary tiles
    var tiles = R.order.map(function (g) { return '<div><strong>' + ((R.groups[g] || []).length) + '</strong><span>' + GROUPNAME[g].toLowerCase() + '</span></div>'; }).join('') +
      '<div><strong>' + R.near.length + '</strong><span>near misses</span></div>';
    $('#fm-tiles').innerHTML = tiles;
    // stack
    var S = R.stack, sh = '';
    if (S.pick.length) {
      var govPct = Math.round(S.gov / S.budget * 100);
      sh = '<div class="as-card fm-stack"><h3>A funding stack to explore</h3><p class="muted">One program from each type you chose, best fit first. Programs can often be combined on one project, but total government funding is usually capped. We use ' + S.cap + '% of eligible costs here.</p>' +
        '<table class="fm-stack-t"><thead><tr><th>Program</th><th>Type</th><th class="num">Indicative amount</th></tr></thead><tbody>' +
        S.pick.map(function (x) { return '<tr><td><a href="' + esc(x.r.url) + '" target="_blank" rel="noopener">' + esc(x.r.name) + '</a></td><td>' + esc(GROUPNAME[x.g]) + '</td><td class="num">' + (x.est != null ? money(x.est) + (rep(x) ? ' (repayable)' : '') : x.g === 'tax' ? 'Claimed after you spend' : x.g === 'loan' ? 'Financing, repayable' : 'Advice and support') + '</td></tr>'; }).join('') +
        '</tbody></table><div class="fm-bar2" role="img" aria-label="Grants about ' + govPct + '% of the project, your share ' + (100 - govPct) + '%"><span style="width:' + govPct + '%"></span></div>' +
        '<p class="fm-bar2-l"><span><i class="g"></i>Grants and contributions: about ' + money(S.gov) + ' (' + govPct + '%)</span><span><i></i>Your share: about ' + money(S.share) + ' (' + (100 - govPct) + '%)</span></p>' +
        (P.cash && P.cash < 100 - govPct ? '<p class="fm-warn">You said you could pay about ' + P.cash + '% yourself. This stack needs about ' + (100 - govPct) + '% from you before tax credits and loans. A loan or a smaller first phase can close the gap.</p>' : '') +
        '<p class="muted fm-small">Indicative only, based on each program\'s maximum share and amount. Programs decide the real amount, and most pay after you spend.</p></div>';
    }
    $('#fm-stack').innerHTML = sh;
    // groups
    $('#fm-groups').innerHTML = R.order.filter(function (g) { return (R.groups[g] || []).length; }).map(function (g) {
      var list = R.groups[g], top = list.slice(0, 3), rest = list.slice(3, 12);
      return '<section class="fm-group"><div class="fm-group-h"><h3>' + esc(GROUPNAME[g]) + '</h3><span class="muted">' + list.length + ' match' + (list.length > 1 ? 'es' : '') + (P.pref.indexOf(g) < 0 ? ' · not a type you picked' : '') + '</span></div>' +
        top.map(card).join('') + (rest.length ? '<div hidden>' + rest.map(card).join('') + '</div><button type="button" class="btn btn-ghost fm-more" data-fm="more">Show ' + rest.length + ' more</button>' : '') + '</section>';
    }).join('');
    // near misses
    $('#fm-near').innerHTML = R.near.length ? '<div class="as-card"><h3>Near misses</h3><p class="muted">These fit your project, but each one has a requirement you do not meet yet. Plan for them as you grow.</p><ul class="fm-near">' +
      R.near.map(function (x) { var s = x.soft[0]; return '<li><a href="' + esc(x.r.url) + '" target="_blank" rel="noopener">' + esc(x.r.name) + '</a><span>Needs ' + esc(s.t) + '. ' + (s.k === 'inc' ? 'You would qualify once the business is incorporated.' : 'You would qualify once you reach it.') + '</span></li>'; }).join('') + '</ul></div>' : '';
    // watch list
    $('#fm-watch').innerHTML = R.watch.length ? '<div class="as-card"><h3>Watch for the next intake</h3><p class="muted">Strong fits that are closed to new applications right now.</p><ul class="fm-near">' +
      R.watch.map(function (x) { return '<li><a href="' + esc(x.r.url) + '" target="_blank" rel="noopener">' + esc(x.r.name) + '</a><span>' + esc(x.r.deadline) + '</span></li>'; }).join('') + '</ul></div>' : '';
    // readiness
    var have = ans.ready || [], todo = [];
    if (P.legal === 'none' || P.legal === 'sole' || P.legal === 'part') todo.push(['Consider incorporating', 'Many grants, including NRC IRAP and CanExport SMEs, fund incorporated businesses only. Ask your accountant whether it makes sense for you.']);
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
    e.preventDefault(); card.hidden = false; var d = card.querySelector('details'); if (d) d.open = true;
    card.scrollIntoView({ behavior: 'smooth', block: 'center' }); card.classList.add('fm-flash'); setTimeout(function () { card.classList.remove('fm-flash'); }, 2200);
  });

  /* ---------- report text and PDF (same report service as the Digital Assessment) ---------- */
  var REP = null, SITE = 'https://www.chmltech.com/';
  function report() {
    var R = RES, P = R.P, secs = [];
    var lab = function (list, k) { var x = row(list, k); return x ? x[1] : k; };
    secs.push(['1. Your answers', [
      'Location: ' + P.prov, 'Industry: ' + lab(IND, ans.ind), 'Business set-up: ' + lab(LEGAL, ans.legal), 'Employees: ' + lab(EMP, ans.emp),
      ans.legal !== 'none' ? 'Revenue: ' + lab(REV, ans.rev) : '', ans.legal !== 'none' ? 'Years operating: ' + lab(YRS, ans.yrs) : '',
      'Funding for: ' + (ans.goal || []).map(function (g) { return lab(GOALS, g); }).join('; '), 'Project cost: ' + lab(BUDGET, ans.budget), 'Start: ' + lab(START, ans.start),
      'Funding types: ' + (ans.pref || []).map(function (g) { return lab(PREF, g); }).join('; ')].filter(Boolean).join('\n')]);
    var S = R.stack;
    if (S.pick.length) secs.push(['2. A funding stack to explore', S.pick.map(function (x, i) { return (i + 1) + '. ' + x.r.name + ' (' + GROUPNAME[x.g] + '): ' + (x.est != null ? 'about ' + money(x.est) + (rep(x) ? ' (repayable)' : '') : x.g === 'tax' ? 'claimed after you spend' : x.g === 'loan' ? 'repayable financing' : 'advice and support') + '\n   ' + x.r.url; }).join('\n') +
      '\n\nGrants and contributions: about ' + money(S.gov) + ' of a ' + money(S.budget) + ' project (cap used: ' + S.cap + '% of eligible costs). Your share: about ' + money(S.share) + '. Indicative only; each program decides the real amount.']);
    var n = 3;
    R.order.forEach(function (g) {
      var list = (R.groups[g] || []).slice(0, 5); if (!list.length) return;
      secs.push([(n++) + '. ' + GROUPNAME[g], list.map(function (x, i) {
        return (i + 1) + '. ' + x.r.name + ' (fit ' + x.score + '%)\n   ' + x.r.administrator + ' | ' + x.r.status + '\n   Amount: ' + x.r.amount_text + '\n   Why it fits: ' + x.why.join('; ') + '\n   Check: ' + (x.check.join('; ') || 'confirm on the official page') + '\n   ' + x.r.url;
      }).join('\n\n')]);
    });
    if (R.near.length) secs.push([(n++) + '. Near misses', R.near.map(function (x) { return '- ' + x.r.name + ': needs ' + x.soft[0].t + '. ' + x.r.url; }).join('\n')]);
    if (R.watch.length) secs.push([(n++) + '. Watch for the next intake', R.watch.map(function (x) { return '- ' + x.r.name + ': ' + x.r.deadline; }).join('\n')]);
    secs.push([(n++) + '. Readiness checklist', $$('#fm-ready li').map(function (li, i) { return (i + 1) + '. ' + li.querySelector('b').textContent + ': ' + li.querySelector('span').textContent; }).join('\n')]);
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
  function pdfTxt(x) { return String(x).replace(/→/g, 'to').replace(/↗/g, '').replace(/[^\x00-\xff–—‘’“”•…€™]/g, ''); }
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
        room(lh * lines.length + 1);
        lines.forEach(function (ln) {
          col(o.color || [40, 48, 62]); doc.text(ln, x, y);
          var u = /(https?:\/\/\S+)/.exec(ln);
          if (u) { var ux = x + doc.getTextWidth(ln.slice(0, u.index)); doc.link(ux, y - 3.2, doc.getTextWidth(u[1]), 4.2, { url: u[1] }); }
          y += lh;
        });
      }
      head();
      doc.setFillColor(NAVY[0], NAVY[1], NAVY[2]); doc.rect(M, y - 4, CW, 30, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(21); doc.setTextColor(255, 255, 255); doc.text('Your Funding Match', M + 7, y + 7);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.text(pdfTxt('Prepared for ' + ([who, co].filter(Boolean).join(', ') || 'your business') + '  |  ' + RES.P.prov), M + 7, y + 15);
      doc.text(pdfTxt('Chmltech Funding Match  |  ' + date), M + 7, y + 21);
      y += 34;
      REP.secs.forEach(function (sec) {
        room(28); y += 3; doc.setFont('helvetica', 'bold'); doc.setFontSize(13); col(NAVY); doc.text(pdfTxt(sec[0]), M, y);
        doc.setDrawColor(LINE[0], LINE[1], LINE[2]); doc.setLineWidth(0.3); doc.line(M, y + 2, W - M, y + 2); y += 8;
        String(sec[1]).split('\n').forEach(function (ln) {
          if (!ln.trim()) { y += 2.5; return; }
          var t = pdfTxt(ln);
          if (/^\d+\. /.test(t) && !/^\s/.test(ln)) { room(14); y += 1; para(t, { bold: true, color: NAVY, size: 10 }); return; }
          if (/^- /.test(t)) { para('•  ' + t.slice(2), { ind: 2 }); return; }
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
      var slug = (co || 'Report').replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '').slice(0, 40) || 'Report';
      return { doc: doc, file: 'Chmltech_Funding_Match_' + slug + '.pdf' };
    });
  }
  window.ChmlReportText = function () { return REP ? REP.secs.map(function (x) { return x[0] + '\n' + x[1]; }).join('\n\n') : ''; };
  window.ChmlReportIndustry = function () { var x = row(IND, ans.ind); return x ? x[1] : ''; };
  window.ChmlReportPdf = function () { return makePdf().then(function (o) { return { blob: o.doc.output('blob'), file: o.file }; }); };
  window.ChmlFundingMatchTest = { evaluate: evaluate, profile: profile, setAnswers: function (a) { ans = a; }, finish: finish, res: function () { return RES; } };
})();
