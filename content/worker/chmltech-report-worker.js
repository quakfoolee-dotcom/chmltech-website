/**
 * chmltech-report — Cloudflare Worker (V26.1)
 * Receives the Digital Assessment report (PDF + text) from www.chmltech.com and emails it via Resend:
 *   1) to the visitor (PDF attached), reply-to info@chmltech.com
 *   2) a copy to Chmltech (full text report + PDF), reply-to the visitor
 *
 * Secrets (Cloudflare → Worker → Settings → Variables and Secrets):
 *   RESEND_API_KEY    Resend API key with "Sending access" for mail.chmltech.com
 *   TURNSTILE_SECRET  Turnstile widget secret key
 * Optional plain variables: FROM, OWNER, ALLOWED_ORIGINS (comma-separated)
 */
const DEFAULTS = {
  FROM: 'Chmltech <reports@mail.chmltech.com>',
  OWNER: 'info@chmltech.com',
  ALLOWED_ORIGINS: 'https://www.chmltech.com,https://chmltech.com',
};
const MAX_PDF = 2 * 1024 * 1024;     // 2 MB
const MAX_TEXT = 40000;              // characters of report text
const EMAIL_RE = /^[^\s@<>"]{1,64}@[^\s@<>"]{1,190}\.[A-Za-z]{2,24}$/;

function cfg(env, k) { return (env && env[k]) || DEFAULTS[k]; }
function esc(s) { return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
function clean(s, n) { return String(s || '').replace(/[\r\n\t]+/g, ' ').trim().slice(0, n); }

function cors(origin, env) {
  const ok = cfg(env, 'ALLOWED_ORIGINS').split(',').map(s => s.trim()).includes(origin);
  return ok ? { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Vary': 'Origin' } : null;
}
function json(body, status, headers) {
  return new Response(JSON.stringify(body), { status, headers: Object.assign({ 'Content-Type': 'application/json' }, headers || {}) });
}
function toBase64(buf) {
  const bytes = new Uint8Array(buf); let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}
async function sendEmail(env, payload) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + env.RESEND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error('resend ' + r.status + ' ' + (await r.text()).slice(0, 300));
  return r.json();
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const ch = cors(origin, env);
    if (request.method === 'OPTIONS') return ch ? new Response(null, { status: 204, headers: ch }) : new Response(null, { status: 403 });
    if (request.method !== 'POST') return json({ ok: false, error: 'method' }, 405, ch);
    if (!ch) return json({ ok: false, error: 'origin' }, 403);

    let fd;
    try { fd = await request.formData(); } catch (e) { return json({ ok: false, error: 'bad form' }, 400, ch); }

    // honeypot
    if (fd.get('botcheck')) return json({ ok: true }, 200, ch);

    // Turnstile
    const token = fd.get('cf-turnstile-response');
    if (!token) return json({ ok: false, error: 'verification missing' }, 400, ch);
    const tv = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: String(token), remoteip: request.headers.get('CF-Connecting-IP') || '' }),
    }).then(r => r.json()).catch(() => ({ success: false }));
    if (!tv.success) return json({ ok: false, error: 'verification failed' }, 403, ch);

    // fields
    const name = clean(fd.get('name'), 120), email = clean(fd.get('email'), 254), company = clean(fd.get('company'), 160);
    if (!name || !EMAIL_RE.test(email) || fd.get('consent') !== 'yes') return json({ ok: false, error: 'invalid fields' }, 400, ch);
    const text = String(fd.get('report_text') || '').slice(0, MAX_TEXT);
    const industry = clean(fd.get('industry'), 120);
    const kind = clean(fd.get('report_kind'), 20) === 'funding' ? 'funding' : 'digital';
    const K = kind === 'funding'
      ? { tool: 'Funding Match', doc: 'Funding Match', covers: 'best-fit grants, tax credits and loans for your project, a funding stack to explore, near misses to plan for and a readiness checklist', review: 'funding review', subj: 'Your Funding Match from Chmltech', owner: 'Funding match report', def: 'Chmltech_Funding_Match.pdf', note: 'Results are a starting point, not a decision on eligibility; confirm each program on its official page.' }
      : { tool: 'Digital Needs Assessment', doc: 'Digital Roadmap', covers: 'your technology priorities, a first project, software options with demo questions, a 90-day action plan, AI tools to try and funding', review: 'roadmap review', subj: 'Your Digital Roadmap from Chmltech', owner: 'Digital assessment report', def: 'Chmltech_Digital_Roadmap.pdf', note: 'Scores are our analyst rating from vendor information; confirm them in a demo.' };

    // PDF
    const pdf = fd.get('report_pdf');
    if (!pdf || typeof pdf === 'string' || pdf.size > MAX_PDF || pdf.size < 1000) return json({ ok: false, error: 'pdf' }, 400, ch);
    const buf = await pdf.arrayBuffer();
    const head = new TextDecoder().decode(buf.slice(0, 5));
    if (head !== '%PDF-') return json({ ok: false, error: 'pdf' }, 400, ch);
    const fileName = clean(pdf.name, 80).replace(/[^A-Za-z0-9_.-]/g, '_') || K.def;
    const attachment = [{ filename: fileName.endsWith('.pdf') ? fileName : fileName + '.pdf', content: toBase64(buf) }];

    const first = name.split(' ')[0];
    const visitorHtml =
      '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#1d2433;max-width:560px">' +
      '<p>Hi ' + esc(first) + ',</p>' +
      '<p>Thank you for completing the Chmltech ' + K.tool + '. Your ' + K.doc + ' is attached as a PDF.</p>' +
      '<p>It covers ' + K.covers + '.</p>' +
      '<p>Want to talk it through? <a href="https://www.chmltech.com/book" style="color:#0B2A5A;font-weight:bold">Book a free 30-minute ' + K.review + '</a>, or simply reply to this email.</p>' +
      '<p>Regards,<br>Quak Foo Lee<br>Chmltech Ltd. | Vancouver, BC<br><a href="https://www.chmltech.com" style="color:#0B2A5A">www.chmltech.com</a></p>' +
      '<p style="font-size:12px;color:#5a6475">' + K.note + ' You received this email because you requested your report on chmltech.com.</p></div>';

    const ownerHtml =
      '<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#1d2433">' +
      '<p><b>New ' + K.owner + '</b> (PDF attached, also sent to the visitor)</p>' +
      '<p>Name: ' + esc(name) + '<br>Email: ' + esc(email) + '<br>Company: ' + esc(company || '-') + '<br>Industry: ' + esc(industry || '-') + '</p>' +
      '<div style="white-space:pre-wrap;font-family:Arial,Helvetica,sans-serif;font-size:13.5px;line-height:1.5;background:#f5f7fa;padding:14px;border-radius:6px">' + esc(text) + '</div></div>';

    try {
      await sendEmail(env, {
        from: cfg(env, 'FROM'), to: [email], reply_to: cfg(env, 'OWNER'),
        subject: K.subj, html: visitorHtml, attachments: attachment,
      });
    } catch (e) {
      console.log('visitor send failed', String(e));
      return json({ ok: false, error: 'send' }, 502, ch);
    }
    try {
      await sendEmail(env, {
        from: cfg(env, 'FROM'), to: [cfg(env, 'OWNER')], reply_to: email,
        subject: K.owner + ' — ' + name + (company ? ' (' + company + ')' : ''), html: ownerHtml, attachments: attachment,
      });
    } catch (e) { console.log('owner copy failed', String(e)); }

    return json({ ok: true }, 200, ch);
  },
};
