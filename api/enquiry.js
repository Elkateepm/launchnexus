/**
 * POST /api/enquiry
 *
 * Emails a website enquiry to info@launchnexus.co.uk via Resend, and — if
 * Supabase credentials are present — also files it in the enquiries table so
 * there's a pipeline to work from later.
 *
 * Required environment variables (Vercel → Settings → Environment Variables):
 *   RESEND_API_KEY      Resend API key
 *   ENQUIRY_TO          Optional. Defaults to info@launchnexus.co.uk
 *   ENQUIRY_FROM        Optional. Defaults to onboarding@resend.dev, which
 *                       only delivers to the Resend account owner. Once
 *                       launchnexus.co.uk is verified in Resend, set this to
 *                       something like "LaunchNexus <website@launchnexus.co.uk>"
 *                       so enquiries reach the real inbox.
 *
 * Optional (to also store enquiries):
 *   SUPABASE_URL
 *   SUPABASE_SERVICE_ROLE_KEY   Server-side only. Never expose to the browser.
 */

const SERVICES = ['Personalised CRM', 'Website', 'App', 'Not sure yet'];

const MAX_BODY_BYTES = 20 * 1024;   // nothing legitimate comes close
const RATE_LIMIT = 5;               // submissions per IP...
const RATE_WINDOW_MS = 10 * 60 * 1000; // ...per 10 minutes

/**
 * Best-effort in-memory rate limit. Serverless instances are ephemeral and
 * there may be several running at once, so this throttles casual abuse but is
 * NOT a hard guarantee — a determined attacker spraying across cold starts can
 * still get through. For a real ceiling, put Vercel's firewall / rate limiting
 * in front of this route.
 */
const hits = new Map();

function rateLimited(ip) {
  const now = Date.now();
  for (const [key, times] of hits) {
    const live = times.filter((t) => now - t < RATE_WINDOW_MS);
    if (live.length) hits.set(key, live);
    else hits.delete(key);
  }
  const mine = (hits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  if (mine.length >= RATE_LIMIT) return true;
  mine.push(now);
  hits.set(ip, mine);
  return false;
}

const esc = (s) =>
  String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

const clean = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Requests from our own fetch() set this; a plain <form> POST does not, which
  // is how we tell whether to answer with JSON or a redirect.
  const wantsJson = req.headers['x-requested-with'] === 'fetch';
  const done = (code, payload) => {
    if (wantsJson) return res.status(code).json(payload);
    if (code === 200) {
      res.setHeader('Location', '/thanks.html');
      return res.status(303).end();
    }
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res
      .status(code)
      .end(
        `<!doctype html><meta charset="utf-8"><title>Enquiry not sent</title>` +
          `<body style="font-family:system-ui;max-width:36rem;margin:12vh auto;padding:0 1.5rem;line-height:1.6">` +
          `<h1 style="font-size:1.5rem">That didn&rsquo;t send</h1><p>${esc(
            payload.error || 'Something went wrong.'
          )}</p><p>Please email <a href="mailto:info@launchnexus.co.uk">info@launchnexus.co.uk</a> ` +
          `and we&rsquo;ll pick it up from there.</p><p><a href="/contact.html">Back to the form</a></p></body>`
      );
  };

  const length = Number(req.headers['content-length'] || 0);
  if (length > MAX_BODY_BYTES) {
    return done(413, { error: 'That message is too long to send.' });
  }

  const ip =
    (req.headers['x-forwarded-for'] || '').split(',')[0].trim() ||
    req.socket?.remoteAddress ||
    'unknown';
  if (rateLimited(ip)) {
    return done(429, { error: 'Too many enquiries from this connection. Please try again shortly.' });
  }

  const body = typeof req.body === 'string' ? safeParse(req.body) : req.body || {};

  // Honeypot — bots complete hidden fields, people don't. Accept and discard.
  if (clean(body.website, 200)) return done(200, { ok: true });

  const data = {
    name: clean(body.name, 200),
    organisation: clean(body.organisation, 200),
    email: clean(body.email, 320),
    service: SERVICES.includes(body.service) ? body.service : 'Not sure yet',
    message: clean(body.message, 5000),
    budget: clean(body.budget, 100),
    target_date: clean(body.target_date, 20)
  };

  if (!data.name || !data.message) {
    return done(400, { error: 'Please include your name and a message.' });
  }
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email)) {
    return done(400, { error: 'Please check the email address.' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error('RESEND_API_KEY is not set — enquiry could not be emailed.');
    return done(500, { error: 'Email is not configured.' });
  }

  const to = process.env.ENQUIRY_TO || 'info@launchnexus.co.uk';
  const from = process.env.ENQUIRY_FROM || 'LaunchNexus <onboarding@resend.dev>';

  const rows = [
    ['Name', data.name],
    ['Organisation', data.organisation || '—'],
    ['Email', data.email],
    ['Looking for', data.service],
    ['Budget', data.budget || 'Not given'],
    ['Ideal launch date', data.target_date || 'Not given']
  ];

  const html = `
    <div style="font-family:-apple-system,Segoe UI,sans-serif;color:#0A0F1C;max-width:620px">
      <h2 style="margin:0 0 6px">New project enquiry</h2>
      <p style="color:#5C6880;margin:0 0 22px">From the LaunchNexus website</p>
      <table style="border-collapse:collapse;width:100%;font-size:15px">
        ${rows
          .map(
            ([k, v]) =>
              `<tr><td style="padding:9px 14px 9px 0;color:#5C6880;white-space:nowrap;vertical-align:top">${esc(
                k
              )}</td><td style="padding:9px 0"><strong>${esc(v)}</strong></td></tr>`
          )
          .join('')}
      </table>
      <h3 style="margin:26px 0 8px;font-size:15px">What they need</h3>
      <p style="white-space:pre-wrap;line-height:1.6;margin:0">${esc(data.message)}</p>
    </div>`;

  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n') + `\n\nWhat they need:\n${data.message}`;

  try {
    const send = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: data.email, // replying goes straight back to the enquirer
        subject: `Project enquiry — ${data.organisation || data.name}`,
        html,
        text
      })
    });

    if (!send.ok) {
      const detail = await send.text();
      console.error('Resend rejected the message:', send.status, detail);
      return done(502, { error: 'The message could not be sent.' });
    }
  } catch (err) {
    console.error('Resend request failed:', err);
    return done(502, { error: 'The message could not be sent.' });
  }

  // Optional: keep a copy in the enquiries table. A storage failure must not
  // lose an enquiry that has already been emailed, so it's logged, not thrown.
  const dbUrl = process.env.SUPABASE_URL;
  const dbKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (dbUrl && dbKey) {
    try {
      const stored = await fetch(`${dbUrl}/rest/v1/enquiries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          apikey: dbKey,
          Authorization: `Bearer ${dbKey}`,
          Prefer: 'return=minimal'
        },
        body: JSON.stringify({
          ...data,
          organisation: data.organisation || null,
          budget: data.budget || null,
          target_date: data.target_date || null,
          status: 'New'
        })
      });
      if (!stored.ok) console.error('Supabase insert failed:', stored.status, await stored.text());
    } catch (err) {
      console.error('Supabase insert threw:', err);
    }
  }

  return done(200, { ok: true });
}

function safeParse(s) {
  try {
    return JSON.parse(s);
  } catch {
    return {};
  }
}
