#!/usr/bin/env python3
"""Generate the LaunchNexus static site.

Every page shares one header/footer here so the shell can't drift between
pages. Run `python3 build.py` from the repo root after editing.
"""
import os, re, hashlib

SITE = "https://launchnexus.co.uk/"


def asset_version(*paths):
    """Short hash of the shared assets. Appended to their URLs so a deploy
    always busts the cache — the filenames themselves never change, and
    without this a returning visitor keeps last week's CSS."""
    h = hashlib.md5()
    root = os.path.dirname(os.path.abspath(__file__))
    for p in paths:
        full = os.path.join(root, p)
        if os.path.exists(full):
            h.update(open(full, "rb").read())
    return h.hexdigest()[:10]


VER = asset_version("assets/site.css", "assets/site.js")

NAV = [
    ("services.html", "Services"),
    ("work.html", "Work"),
    ("how-it-works.html", "How It Works"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

MARK = '<img src="assets/logo-lockup.png" alt="LaunchNexus" width="376" height="112">'
MARK_LIGHT = '<img src="assets/logo-lockup-light.png" alt="LaunchNexus" width="376" height="112">'

TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
        'stroke-linejoin="round"><path d="m5 13 4 4L19 7"/></svg>')

ARROW = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>')

EXT = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M9 7h8v8"/></svg>')
EXT_SMALL = ('<svg class="ext" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M9 7h8v8"/></svg>')

CHEV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>')


def shell(page, body):
    active = page["file"]
    links = "".join(
        '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href == active else "", label)
        for href, label in NAV
    )
    drawer = "".join('<a href="%s">%s</a>' % (h, l) for h, l in NAV)
    extra_js = page.get("extra_js", "")
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<link rel="canonical" href="{SITE}{'' if active == 'index.html' else active}">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{'' if active == 'index.html' else active}">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" href="assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:image" content="{SITE}assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{'<meta name="robots" content="noindex">' if page.get('noindex') else ''}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css?v={VER}">
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html">{MARK}</a>
    <nav class="nav-links" aria-label="Primary">{links}</nav>
    <div class="nav-cta">
      <a class="btn btn--primary" href="contact.html">Start a Project</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Menu"><span></span></button>
    </div>
  </div>
</header>

<nav class="drawer" id="drawer" aria-label="Mobile">{drawer}<a class="btn btn--primary" href="contact.html">Start a Project</a></nav>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html">{MARK_LIGHT}</a>
        <p class="foot-tagline">Building technology. Connecting impact.</p>
        <p style="max-width:34ch;font-size:15px">Digital tools built around your organisation.</p>
        <p style="font-size:15px;margin-top:14px"><a href="mailto:info@launchnexus.co.uk">info@launchnexus.co.uk</a></p>
      </div>
      <div><h2 class="foot-h">Services</h2><ul>
        <li><a href="services-crm.html">Custom CRM</a></li>
        <li><a href="services-websites.html">Websites</a></li>
        <li><a href="services-apps.html">Apps</a></li>
      </ul></div>
      <div><h2 class="foot-h">Company</h2><ul>
        <li><a href="about.html">About</a></li>
        <li><a href="work.html">Work</a></li>
        <li><a href="how-it-works.html">How It Works</a></li>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="https://launchsession.co.uk" target="_blank" rel="noopener">LaunchSession<svg class="ext" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M9 7h8v8"/></svg><span class="sr-only"> (opens in a new tab)</span></a></li>
      </ul></div>
      <div><h2 class="foot-h">Legal</h2><ul>
        <li><a href="privacy.html">Privacy</a></li>
        <li><a href="terms.html">Terms</a></li>
        <li><a href="cookies.html">Cookies</a></li>
      </ul></div>
    </div>
    <div class="foot-note">
      <p>© <span data-year>2026</span> LaunchNexus Ltd. Registered in England &amp; Wales, company no. 17333693.</p>
      <p>Watford, United Kingdom · <a href="mailto:info@launchnexus.co.uk">info@launchnexus.co.uk</a></p>
    </div>
  </div>
</footer>
{extra_js}
<script src="assets/site.js?v={VER}" defer></script>
</body>
</html>
"""


def page_hero(crumb, h1, lede):
    return f"""<section class="page-hero">
  <div class="wrap">
    <span class="crumb rise">{crumb}</span>
    <h1 class="rise">{h1}</h1>
    <p class="lede rise">{lede}</p>
  </div>
</section>"""


def cta_band(heading, text, primary=("contact.html", "Start a Project"), secondary=("mailto:info@launchnexus.co.uk", "Talk to Us")):
    return f"""<section class="section cta-band">
  <div class="wrap">
    <div class="rise">
      <h2 class="center" style="max-width:19ch">{heading}</h2>
      <p class="lede center" style="margin-top:22px">{text}</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="{primary[0]}">{primary[1]}</a>
        <a class="btn btn--ghost" href="{secondary[0]}">{secondary[1]}</a>
      </div>
    </div>
  </div>
</section>"""


def module(title, text):
    return f'<div class="module"><h3>{title}</h3><p>{text}</p></div>'


def step(title, text):
    return f'<li class="step"><div><h3>{title}</h3><p>{text}</p></div></li>'


def built_item(text):
    return f'<li>{TICK} {text}</li>'


# ===========================================================================
# SERVICES OVERVIEW
# ===========================================================================
SERVICES = page_hero(
    '<a href="index.html">Home</a> · Services',
    "Three ways we help.",
    "Personalised CRM systems, websites and apps — all designed around the way your organisation already works, rather than the other way round.",
) + """
<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Our services</span>
      <h2>Pick the one that sounds like your problem.</h2>
      <p class="lede">Plenty of projects turn out to be two of these at once — a website with a system behind it, or an app that grows out of a CRM.</p>
    </div>
    <div class="grid grid-3">
      <article class="card card--hover rise">
        <span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M3 9h18M9 9v12"/></svg></span>
        <h3>Personalised CRM Systems</h3>
        <p><strong>Your organisation. Your workflow. Your CRM.</strong></p>
        <p>Custom management systems built around how you actually operate — the records you keep, the steps you follow and the people who need to see what.</p>
        <p style="margin-top:22px"><a class="link-arrow" href="services-crm.html">Explore Custom CRMs """ + ARROW + """</a></p>
      </article>
      <article class="card card--hover rise">
        <span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.9 2.6 15.1 0 18M12 3c-2.6 2.9-2.6 15.1 0 18"/></svg></span>
        <h3>Websites</h3>
        <p><strong>Websites built to do more.</strong></p>
        <p>Fast, responsive sites designed around your brand and audience — with the enquiry, booking and payment plumbing behind them.</p>
        <p style="margin-top:22px"><a class="link-arrow" href="services-websites.html">Explore Websites """ + ARROW + """</a></p>
      </article>
      <article class="card card--hover rise">
        <span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2.5" width="12" height="19" rx="2.6"/><path d="M11 18.5h2"/></svg></span>
        <h3>Web &amp; Mobile Apps</h3>
        <p><strong>Turn your idea into a product.</strong></p>
        <p>Web and mobile applications for businesses, organisations and new ideas — from internal tools to a first version you can put in front of users.</p>
        <p style="margin-top:22px"><a class="link-arrow" href="services-apps.html">Explore Apps """ + ARROW + """</a></p>
      </article>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Technology</span>
      <h2>Modern technology. Built properly.</h2>
      <p class="lede">You don't need to care what any of this is called. It matters because it's what keeps your system fast, secure and still working in five years.</p>
    </div>
    <div class="grid grid-2">
      <article class="card rise"><h3>Secure cloud infrastructure</h3><p>Your data lives on managed cloud infrastructure with encryption in transit and at rest, and automatic backups.</p></article>
      <article class="card rise"><h3>Role-based access</h3><p>People see what their role allows and nothing more — enforced at the database, not just hidden in the interface.</p></article>
      <article class="card rise"><h3>Responsive interfaces</h3><p>The same system works properly on a laptop in the office and a phone at the side of a pitch.</p></article>
      <article class="card rise"><h3>Scalable architecture</h3><p>Built so that adding users, records or a second site is a configuration change rather than a rebuild.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Integrations</span>
      <h2>Your new system doesn't have to live in isolation.</h2>
      <p class="lede">Where it makes sense, we connect your system to the tools you already use, so information doesn't have to be copied between them by hand.</p>
    </div>
    <div class="chips rise">
      <span>Payments</span><span>Email</span><span>SMS</span><span>Calendars</span>
      <span>Cloud storage</span><span>Accounting systems</span><span>APIs</span><span>Analytics</span>
    </div>
    <p class="form-note rise" style="margin-top:22px">We'll confirm exactly which integrations are possible for your setup during discovery, rather than promising them up front.</p>
  </div>
</section>
""" + cta_band(
    "Not sure which of these you need?",
    "That's a normal place to start. Tell us what's getting in the way and we'll tell you what would actually help.",
    ("contact.html", "Start a Project"), ("how-it-works.html", "See How It Works"))


# ===========================================================================
# CRM SERVICE PAGE
# ===========================================================================
CRM = page_hero(
    '<a href="index.html">Home</a> · <a href="services.html">Services</a> · Custom CRM',
    "CRM software designed around you.",
    "Instead of forcing your organisation into an off-the-shelf system, we learn how you work and build a CRM around it.",
) + """
<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Possible modules</span>
      <h2>Only the parts you need.</h2>
      <p class="lede">A CRM doesn't have to mean a sales pipeline. These are the pieces we build most often — yours might use four of them, or all of them under different names.</p>
    </div>
    <div class="modules rise">
""" + "".join([
    module("Customer / client management", "Keep contacts, history and information together in one record instead of five places."),
    module("Staff", "Manage your team, their permissions and what they've done."),
    module("Projects", "Track work from beginning to completion, with everyone seeing the same status."),
    module("Forms", "Collect information digitally — registrations, consent, feedback, applications."),
    module("Documents", "Keep important files organised and attached to the record they belong to."),
    module("Payments", "Track transactions, outstanding balances and who has paid what."),
    module("Communications", "Keep messages connected to the record they relate to."),
    module("Reporting", "Understand what's actually happening across the organisation, without exporting to a spreadsheet first."),
    module("Automation", "Reduce repetitive admin — reminders, recurring tasks and the jobs someone currently does by hand."),
]) + """
    </div>
    <p class="lede rise" style="margin-top:34px;font-size:19px;color:var(--text)"><strong>Every CRM is different because every organisation is different.</strong></p>
    <p class="lede rise" style="margin-top:18px">We build our own too. <a href="https://launchsession.co.uk" target="_blank" rel="noopener" style="color:var(--accent);font-weight:600;text-decoration:none">LaunchSession <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M9 7h8v8"/></svg><span class="sr-only"> (opens in a new tab)</span></a> is our platform for youth organisations, charities and sports clubs \u2014 the same approach, running in production.</p>
    <div class="btn-row rise"><a class="btn btn--primary" href="contact.html">Tell Us What You Need</a></div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">How a CRM gets built</span>
      <h2>It starts with your workflow, not our template.</h2>
      <p class="lede">This is the part most software skips. It's also the reason a bespoke system fits when a generic one doesn't.</p>
    </div>
    <div class="flow rise">
      <div class="flow-item">Your organisation<span>How you work today, including the spreadsheets</span></div>
      <div class="flow-item">We learn how you work<span>Sitting with the people who do the job</span></div>
      <div class="flow-item">We map your workflows<span>Every step, decision and handover written down</span></div>
      <div class="flow-item">We design your system<span>Screens built around those steps</span></div>
      <div class="flow-item">We build &amp; test<span>With your feedback while changes are still cheap</span></div>
      <div class="flow-item is-end">Your personalised CRM<span>Yours to keep growing</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Signs you need one</span>
      <h2>Sound familiar?</h2>
    </div>
    <div class="grid grid-2">
      <article class="card rise"><h3>The spreadsheet has outgrown itself</h3><p>It works, but only one person really understands it, and everyone's afraid of breaking the formulas.</p></article>
      <article class="card rise"><h3>The same information gets typed twice</h3><p>Once into a form, once into a spreadsheet, and once more into an email to someone who needs to know.</p></article>
      <article class="card rise"><h3>Your CRM doesn't fit how you work</h3><p>You're paying monthly for something you've had to bend your process around, and still using half of it.</p></article>
      <article class="card rise"><h3>Nobody can answer simple questions</h3><p>How many people came last month? Who hasn't paid? Which forms are outstanding? It takes an afternoon to find out.</p></article>
    </div>
  </div>
</section>
""" + cta_band(
    "Tell us how your organisation works today.",
    "We'll tell you honestly whether a custom CRM is worth it for you — or whether something simpler would do the job.",
    ("contact.html", "Tell Us What You Need"), ("work.html", "See Our Work"))


# ===========================================================================
# WEBSITES SERVICE PAGE
# ===========================================================================
WEBSITES = page_hero(
    '<a href="index.html">Home</a> · <a href="services.html">Services</a> · Websites',
    "A website that represents your organisation properly.",
    "Fast, responsive and designed around what you need your visitors to actually do.",
) + """
<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">What we build</span>
      <h2>Built for the job it has to do.</h2>
      <p class="lede">A charity raising funds and a service business taking bookings need very different websites. We start with what a visitor should do, then design backwards from that.</p>
    </div>
    <div class="grid grid-3">
      <article class="card card--hover rise"><h3>Business websites</h3><p>A professional online presence that explains what you do clearly and makes it easy to get in touch.</p></article>
      <article class="card card--hover rise"><h3>Charity websites</h3><p>Tell your story, demonstrate your impact and support fundraising — with donations handled properly.</p></article>
      <article class="card card--hover rise"><h3>Lead generation</h3><p>Turn visitors into enquiries, with forms that go somewhere useful rather than an inbox nobody checks.</p></article>
      <article class="card card--hover rise"><h3>Booking &amp; services</h3><p>Let customers book, request or pay for services without a phone call and a diary.</p></article>
      <article class="card card--hover rise"><h3>Landing pages</h3><p>Focused pages for a campaign, product or funding appeal, built to be measured.</p></article>
      <article class="card card--hover rise"><h3>Custom functionality</h3><p>When a template can't do it, we build the tool directly into the site — calculators, portals, member areas, directories.</p></article>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Included as standard</span>
      <h2>The parts people forget to ask about.</h2>
    </div>
    <div class="grid grid-2">
      <article class="card rise"><h3>Genuinely responsive</h3><p>Designed for mobile properly, not shrunk down from the desktop version at the end.</p></article>
      <article class="card rise"><h3>Accessible</h3><p>Proper headings, keyboard navigation, visible focus and sufficient contrast — which matters legally as well as ethically for charities and public-facing organisations.</p></article>
      <article class="card rise"><h3>Fast</h3><p>Optimised images, minimal scripts and good Core Web Vitals, because a slow site loses enquiries before anyone reads a word.</p></article>
      <article class="card rise"><h3>Editable</h3><p>Where you need to make your own changes, we set up a content system so you don't have to call us to fix a typo.</p></article>
    </div>
  </div>
</section>
""" + cta_band(
    "Need a website that does more than sit there?",
    "Tell us who it's for and what you need them to do, and we'll come back with a clear proposal.",
    ("contact.html", "Start a Project"), ("services-crm.html", "Explore Custom CRMs"))


# ===========================================================================
# APPS SERVICE PAGE
# ===========================================================================
APPS = page_hero(
    '<a href="index.html">Home</a> · <a href="services.html">Services</a> · Apps',
    "From idea to working application.",
    "We design and develop web and mobile applications for businesses, organisations and brand-new ideas — including first versions built to be tested with real users.",
) + """
<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">The route</span>
      <h2>Six stages, and you'll see it working long before the end.</h2>
    </div>
    <div class="rail rise">
      <b>Idea</b>""" + CHEV + """<b>Product design</b>""" + CHEV + """<b>Prototype</b>""" + CHEV + """<b>Development</b>""" + CHEV + """<b>Testing</b>""" + CHEV + """<b>Launch</b>
    </div>
    <p class="lede rise" style="margin-top:30px">Most people come to us somewhere in the first two stages, with a clear problem and no idea what building it involves. That's the right time to talk.</p>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">What we build</span>
      <h2>Applications people actually open.</h2>
    </div>
    <div class="grid grid-3">
      <article class="card card--hover rise"><h3>Mobile apps</h3><p>iOS and Android apps built around a real daily workflow, not a demo video.</p></article>
      <article class="card card--hover rise"><h3>Internal systems</h3><p>The tool your team uses to do the job, replacing the shared spreadsheet and the group chat.</p></article>
      <article class="card card--hover rise"><h3>Customer portals</h3><p>Let your customers see their own information, book, pay and get answers without emailing you.</p></article>
      <article class="card card--hover rise"><h3>Staff platforms</h3><p>Rotas, records, tasks and permissions for the people delivering your service.</p></article>
      <article class="card card--hover rise"><h3>Booking &amp; membership</h3><p>Sessions, places, renewals and payments — handled once, properly.</p></article>
      <article class="card card--hover rise"><h3>MVP development</h3><p>The smallest version of your idea that's genuinely useful, so you learn from real users before spending more.</p></article>
    </div>
    <div class="btn-row rise"><a class="btn btn--primary" href="contact.html">Discuss Your App</a></div>
  </div>
</section>
""" + cta_band(
    "Got an idea you keep coming back to?",
    "Tell us what problem it solves and who it's for. We'll be straight with you about what it would take to build.",
    ("contact.html", "Discuss Your App"), ("how-it-works.html", "See How It Works"))


# ===========================================================================
# WORK
# ===========================================================================
WORK = page_hero(
    '<a href="index.html">Home</a> · Work',
    "Selected work.",
    "A small, honest portfolio. Everything here is software that exists and is in use — no invented clients and no borrowed case studies.",
) + """
<section class="section">
  <div class="wrap">

    <article class="case rise">
      <div class="case-grid">
        <div>
          <span class="kind">CRM · Multi-tenant platform</span>
          <h2 style="font-size:clamp(26px,3.2vw,38px)">LaunchSession</h2>
          <h3 class="case-label">The challenge</h3>
          <p>Youth organisations, charities and sports clubs run on paper registers, consent forms in a filing cabinet and a spreadsheet that only one person understands. Off-the-shelf charity software either costs more than their budget or assumes a way of working they don't have.</p>
          <h3 class="case-label">The solution</h3>
          <p>A management platform where each organisation gets its own branded system with only the modules relevant to them, rather than a single generic tool everyone has to adapt to.</p>
          <h3 class="case-label">What we built</h3>
          <ul class="built">
""" + "".join([
    built_item("Live registers and attendance tracking"),
    built_item("Consent, medical and safeguarding records"),
    built_item("Volunteer rotas and role-based permissions"),
    built_item("Digital forms and parent registration"),
    built_item("Fundraising and payment tracking"),
    built_item("Risk assessments and reporting"),
]) + """
          </ul>
        </div>
        <div>
          <div class="mock" style="width:100%">
            <div class="mock-bar"><i class="dot"></i><i class="dot"></i><i class="dot"></i><span class="url">app.launchsession.co.uk</span></div>
            <div class="dash">
              <div class="dash-side"><i class="on"></i><i></i><i></i><i></i><i></i></div>
              <div class="dash-main">
                <div class="kpis">
                  <div class="kpi"><b>18</b><span>Present</span></div>
                  <div class="kpi"><b>3</b><span>Absent</span></div>
                  <div class="kpi"><b>6</b><span>Staff</span></div>
                </div>
                <div class="chart">
                  <i style="height:44%"></i><i style="height:66%"></i><i style="height:52%"></i>
                  <i style="height:81%"></i><i style="height:60%"></i><i style="height:90%"></i><i style="height:72%"></i>
                </div>
                <div class="rows">
                  <div class="row"><span class="av"></span><span class="l1"></span><span class="st">In</span></div>
                  <div class="row"><span class="av"></span><span class="l1"></span><span class="st">In</span></div>
                  <div class="row"><span class="av"></span><span class="l1"></span><span class="l2"></span></div>
                </div>
              </div>
            </div>
          </div>
          <p class="form-note" style="text-align:center">Interface shown with sample data.</p>
        </div>
      </div>
    </article>

    <article class="case rise">
      <div class="case-grid">
        <div>
          <span class="kind">Internal platform · Charity</span>
          <h2 style="font-size:clamp(26px,3.2vw,38px)">Charity operations platform</h2>
          <h3 class="case-label">The challenge</h3>
          <p>A London children's charity was taking attendance on paper, tracking payments in a spreadsheet and building the staff rota by hand each week — with the same names re-entered in three places.</p>
          <h3 class="case-label">The solution</h3>
          <p>A single system for the people who run sessions, designed around the order they actually do things on the day rather than a generic database structure.</p>
          <h3 class="case-label">What we built</h3>
          <ul class="built">
""" + "".join([
    built_item("Live attendance register, usable on a phone"),
    built_item("Payment tracking with outstanding balances"),
    built_item("Staff rota and session planning"),
    built_item("Historical registers and reporting"),
    built_item("Archive with restore, so nothing is lost by accident"),
]) + """
          </ul>
        </div>
        <div>
          <div class="mock" style="width:100%">
            <div class="mock-bar"><i class="dot"></i><i class="dot"></i><i class="dot"></i><span class="url">Session register</span></div>
            <div class="dash">
              <div class="dash-side"><i></i><i class="on"></i><i></i><i></i></div>
              <div class="dash-main">
                <div class="kpis">
                  <div class="kpi"><b>24</b><span>Children</span></div>
                  <div class="kpi"><b>19</b><span>Paid</span></div>
                  <div class="kpi"><b>5</b><span>Due</span></div>
                </div>
                <div class="rows">
                  <div class="row"><span class="av"></span><span class="l1"></span><span class="st">Paid</span></div>
                  <div class="row"><span class="av"></span><span class="l1"></span><span class="st">Paid</span></div>
                  <div class="row"><span class="av"></span><span class="l1"></span><span class="l2"></span></div>
                  <div class="row"><span class="av"></span><span class="l1"></span><span class="l2"></span></div>
                </div>
              </div>
            </div>
          </div>
          <p class="form-note" style="text-align:center">Client named on request.</p>
        </div>
      </div>
    </article>

    <div class="grid grid-2" style="margin-top:clamp(34px,4.5vw,54px)">
      <article class="card card--hover rise">
        <span class="kind">Website · Bookings</span>
        <h3>JMS VIP Services</h3>
        <p>A luxury property site with viewing requests, member accounts and checkout, installable as an app on any device.</p>
        <ul class="built">
""" + built_item("Property listings and viewing requests") + built_item("Member accounts and booking history") + built_item("Payments and enquiry handling") + """
        </ul>
      </article>
      <article class="card card--hover rise">
        <span class="kind">Web app · Education</span>
        <h3>Revision Box</h3>
        <p>A GCSE revision app built for one student and then opened up to others.</p>
        <ul class="built">
""" + built_item("Flashcards and timed practice") + built_item("Progress tracking by topic") + built_item("Works offline on a phone") + """
        </ul>
      </article>
    </div>

  </div>
</section>
""" + cta_band(
    "Want something like this for your organisation?",
    "Tell us what you're running on today and we'll tell you what would actually help.",
    ("contact.html", "Start a Project"), ("services.html", "Explore Our Services"))


# ===========================================================================
# HOW IT WORKS
# ===========================================================================
HOW = page_hero(
    '<a href="index.html">Home</a> · How It Works',
    "From idea to launch.",
    "Five stages. You'll know what happens at each one, what you get at the end of it, and what it costs before we start building.",
) + """
<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">The process</span>
      <h2>Five stages, start to finish.</h2>
    </div>
    <ol class="steps rise">
""" + "".join([
    step("Discovery", "We talk through what your organisation does, what you're running on today, where the problems are, what you're aiming for, and who has to use the thing every day. Usually this is a conversation and a look at your current spreadsheets — no preparation needed."),
    step("Blueprint", "We map your workflows, user journeys, required functionality and the information behind them. You get a written scope with a price and a timeline before any code exists, so there are no surprises later."),
    step("Design", "We design the interfaces, dashboards and mobile screens to your brand. You see exactly what you're getting and we change it while changing it is easy."),
    step("Build", "We develop the working product, sharing progress on a private link as we go. You're never waiting months for a big reveal that turns out to be wrong."),
    step("Launch &amp; support", "Testing, data migration from your old systems, staff training and go-live — then ongoing support as your requirements change. We don't hand over a zip file and disappear."),
]) + """
    </ol>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Pricing</span>
      <h2>Every project is different.</h2>
      <p class="lede">We'll understand what you need first, then provide a clear proposal and project cost. No hourly billing you can't predict, and no price quoted before we know what we're building.</p>
    </div>
    <div class="grid grid-3">
      <article class="card rise"><h3>Fixed scope, fixed price</h3><p>You approve a written scope and a cost before the build starts.</p></article>
      <article class="card rise"><h3>Staged payments</h3><p>Payment is spread across the project rather than demanded up front.</p></article>
      <article class="card rise"><h3>Honest answers</h3><p>If an off-the-shelf tool would genuinely serve you better, we'll say so.</p></article>
    </div>
    <div class="btn-row rise"><a class="btn btn--primary" href="contact.html">Request a Project Estimate</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Common questions</span>
      <h2>Before you get in touch.</h2>
    </div>
    <div class="grid grid-2">
      <article class="card rise"><h3>We don't have anyone technical. Is that a problem?</h3><p>No — most of the organisations we work with don't. We handle the technical side and explain decisions in plain English.</p></article>
      <article class="card rise"><h3>How long does it take?</h3><p>It depends entirely on scope, which is why we won't guess before discovery. You'll get a date in the written proposal.</p></article>
      <article class="card rise"><h3>What happens to our existing data?</h3><p>We migrate it. Spreadsheets, exports from an old system, even paper records — bringing your history across is part of the launch stage.</p></article>
      <article class="card rise"><h3>Do we own what you build?</h3><p>Yes. Ownership terms are set out in the proposal before you commit to anything.</p></article>
    </div>
  </div>
</section>
""" + cta_band(
    "Ready to talk it through?",
    "The first conversation is free and there's no commitment attached to it.",
    ("contact.html", "Start a Project"), ("work.html", "See Our Work"))


# ===========================================================================
# ABOUT
# ===========================================================================
ABOUT = page_hero(
    '<a href="index.html">Home</a> · About',
    "Technology should make organisations easier to run.",
    "LaunchNexus was created around a simple idea: organisations shouldn't have to fight with their technology.",
) + """
<section class="section">
  <div class="wrap">
    <div class="measure rise" style="font-size:18px">
      <p>Most software is built for an average organisation that doesn't exist. It arrives with a fixed idea of how you should work, and the gap between that idea and reality gets filled by people — re-typing information, keeping a private spreadsheet, remembering the thing the system can't record.</p>
      <p>We think that's backwards. The way your organisation works is usually the result of years of good reasons. Software should be shaped around it, not the other way round.</p>
      <p>So we start with the work, not the technology. We sit with the people doing the job, learn where the friction actually is, and design around that. Sometimes the answer is a full custom system. Sometimes it's a much smaller change than anyone expected — and we'll say so.</p>
      <p>LaunchNexus is deliberately small. You talk to the person building your system, not an account manager relaying messages to a team you never meet.</p>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">How we think</span>
      <h2>Six things we believe.</h2>
    </div>
    <div class="grid grid-3">
      <article class="card rise"><h3>Built around you</h3><p>Every project starts with your workflow, not a template we've used before.</p></article>
      <article class="card rise"><h3>Simple by design</h3><p>Powerful systems should still be usable by a new volunteer on their first day.</p></article>
      <article class="card rise"><h3>One partner</h3><p>Design, development and launch handled together — no coordinating three suppliers.</p></article>
      <article class="card rise"><h3>Designed to grow</h3><p>Your system changes as your requirements do, without starting again.</p></article>
      <article class="card rise"><h3>Real understanding</h3><p>We begin with how you work, then choose the technology.</p></article>
      <article class="card rise"><h3>Long-term thinking</h3><p>Build something useful today without limiting what's possible tomorrow.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head rise">
      <span class="eyebrow">Who we work with</span>
      <h2>Built for organisations doing real work.</h2>
    </div>
    <div class="grid grid-2">
      <article class="card rise"><h3>Charities &amp; community organisations</h3><p>Simplify operations and spend less of the week on administration, with safeguarding and consent handled properly.</p></article>
      <article class="card rise"><h3>Service businesses</h3><p>Manage customers, bookings, projects and staff in one place.</p></article>
      <article class="card rise"><h3>Growing businesses</h3><p>Replace spreadsheets with systems designed to scale.</p></article>
      <article class="card rise"><h3>Startups &amp; founders</h3><p>Turn an idea into a working digital product.</p></article>
    </div>
  </div>
</section>
""" + cta_band(
    "Let's build something useful.",
    "Tell us how your organisation works today and what you'd like to make better.",
    ("contact.html", "Start a Project"), ("work.html", "See Our Work"))


# ===========================================================================
# CONTACT
# ===========================================================================
CONTACT = page_hero(
    '<a href="index.html">Home</a> · Contact',
    "Let's build something useful.",
    "Tell us a little about your organisation and what you'd like to improve, replace or build. You'll get a straight answer on whether we're the right fit.",
) + """
<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="gap:clamp(30px,4vw,52px);align-items:start">
      <form class="form rise" id="enquiry-form" action="/api/enquiry" method="post">
        <div class="field">
          <label for="name_field">Your name</label>
          <input id="name_field" name="name_field" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="organisation">Organisation / business</label>
          <input id="organisation" name="organisation" type="text" autocomplete="organization">
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" autocomplete="email" required>
        </div>

        <fieldset>
          <legend class="legend">What would you like to build?</legend>
          <div class="choices">
            <label class="choice"><input type="radio" name="service" value="Personalised CRM"><span>Personalised CRM</span></label>
            <label class="choice"><input type="radio" name="service" value="Website"><span>Website</span></label>
            <label class="choice"><input type="radio" name="service" value="App"><span>App</span></label>
            <label class="choice"><input type="radio" name="service" value="Not sure yet" checked><span>Not sure yet</span></label>
          </div>
        </fieldset>

        <div class="field">
          <label for="message">Tell us a little about what you need <span class="hint">— and what problem you're trying to solve.</span></label>
          <textarea id="message" name="message" required></textarea>
        </div>

        <div class="two-up">
          <div class="field">
            <label for="budget">Approximate budget <span class="hint">Optional</span></label>
            <input id="budget" name="budget" type="text" placeholder="e.g. £3,000–£5,000">
          </div>
          <div class="field">
            <label for="target_date">Ideal launch date <span class="hint">Optional</span></label>
            <input id="target_date" name="target_date" type="date">
          </div>
        </div>

        <p class="hp"><label for="website">Leave this empty</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></p>

        <button class="btn btn--primary" type="submit">Start the Conversation</button>
        <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
        <p class="form-note">We'll only use these details to reply to your enquiry. See our <a href="privacy.html">privacy notice</a>.</p>
      </form>

      <div class="rise">
        <h2 style="font-size:clamp(24px,2.8vw,32px)">Prefer email?</h2>
        <p class="lede" style="margin-top:16px"><a href="mailto:info@launchnexus.co.uk" style="color:var(--accent);font-weight:600;text-decoration:none">info@launchnexus.co.uk</a></p>

        <h3 style="margin-top:38px">What happens next</h3>
        <ol class="steps" style="margin-top:14px">
          <li class="step"><div><h3>We read it properly</h3><p>Not an autoresponder — someone who could actually build the thing.</p></div></li>
          <li class="step"><div><h3>We reply within two working days</h3><p>Either with questions, or with a suggested time to talk.</p></div></li>
          <li class="step"><div><h3>A free discovery call</h3><p>No commitment. If we're not the right fit, we'll tell you that too.</p></div></li>
        </ol>

        <div class="card" style="margin-top:32px">
          <h3>LaunchNexus Ltd</h3>
          <p>Watford, United Kingdom.<br>Working with organisations UK-wide.</p>
          <p style="margin-top:12px">Registered in England &amp; Wales, company no. 17333693.</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""

CONTACT_JS = ''


# ===========================================================================
# THANKS
# ===========================================================================
THANKS = """
<section class="section" style="padding-top:clamp(80px,10vw,140px)">
  <div class="wrap">
    <div class="confirm rise">
      <div class="tickmark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m5 13 4 4L19 7"/></svg></div>
      <h1 style="font-size:clamp(32px,4.6vw,52px)">Thanks — we've got it.</h1>
      <p class="lede" style="margin:22px auto 0">We'll review what you've told us and get back to you within two working days. In the meantime, feel free to explore more of our work.</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn btn--primary" href="work.html">See Our Work</a>
        <a class="btn btn--ghost" href="index.html">Back to Home</a>
      </div>
    </div>
  </div>
</section>
"""


# ===========================================================================
# LEGAL
# ===========================================================================
DRAFT = ('<div class="draft-note rise"><strong>Draft.</strong> This page describes how the LaunchNexus website '
         'behaves and should be checked against the live site before publication — an inaccurate notice is itself '
         'a compliance problem.</div>')

PRIVACY = page_hero('<a href="index.html">Home</a> · Privacy', "Privacy notice.",
                    "How LaunchNexus Ltd handles personal information collected through this website.") + f"""
<section class="section">
  <div class="wrap prose rise">
    {DRAFT}
    <p><strong>Last updated:</strong> <span data-year>2026</span></p>
    <p>This notice covers the LaunchNexus marketing website only. If you use a system we have built for another organisation, that organisation controls your data and you should contact them directly.</p>

    <h2>Who we are</h2>
    <p>LaunchNexus Ltd, company number 17333693, registered in England &amp; Wales, is the controller for personal data described here. Contact: <a href="mailto:info@launchnexus.co.uk">info@launchnexus.co.uk</a>.</p>

    <h2>What we collect</h2>
    <table>
      <tr><th>Data</th><th>Why</th><th>Lawful basis</th></tr>
      <tr><td>Name, organisation, email</td><td>To reply to your enquiry</td><td>Legitimate interests — responding to a request you made</td></tr>
      <tr><td>What you'd like built, budget, target date, your message</td><td>To understand your enquiry and prepare a proposal</td><td>Legitimate interests</td></tr>
      <tr><td>Correspondence after your enquiry</td><td>To manage the conversation and any resulting project</td><td>Legitimate interests / contract</td></tr>
    </table>
    <p>We do not run advertising or profiling on this site, and we do not sell personal data.</p>

    <h2>How long we keep it</h2>
    <p>Enquiries that don't lead to work are deleted within 24 months. Where an enquiry becomes a project, records are kept for the life of the relationship and for six years afterwards for accounting and legal purposes.</p>

    <h2>Who else sees it</h2>
    <p>Our hosting and database providers process this data on our behalf under contract. We share data with professional advisers or authorities only where we are legally required to.</p>

    <h2>Your rights</h2>
    <p>You can ask for a copy of your data, ask us to correct or delete it, or object to our use of it. Email <a href="mailto:info@launchnexus.co.uk">info@launchnexus.co.uk</a>. If you're unhappy with our response you can complain to the Information Commissioner's Office at ico.org.uk.</p>

    <h2>Changes</h2>
    <p>We may update this notice. Material changes will be reflected in the date above.</p>
  </div>
</section>
"""

COOKIES = page_hero('<a href="index.html">Home</a> · Cookies', "Cookie notice.",
                    "What this website stores on your device — which is very little.") + f"""
<section class="section">
  <div class="wrap prose rise">
    {DRAFT}
    <p><strong>Last updated:</strong> <span data-year>2026</span></p>
    <h2>What we use</h2>
    <p>This website does not set advertising or tracking cookies, and does not currently use an analytics tool. Nothing on the site requires a cookie banner as built.</p>
    <p>Fonts are loaded from Google Fonts, which means your browser makes a request to Google's servers and Google receives your IP address. If you would rather avoid this, the fonts can be self-hosted instead.</p>
    <h2>If analytics is added later</h2>
    <p>If we add an analytics tool in future, this page will be updated to name it and a consent banner will be added before it runs.</p>
    <h2>Managing cookies</h2>
    <p>Most browsers let you refuse or delete cookies through their settings.</p>
    <h2>Contact</h2>
    <p><a href="mailto:info@launchnexus.co.uk">info@launchnexus.co.uk</a></p>
  </div>
</section>
"""

TERMS = page_hero('<a href="index.html">Home</a> · Terms', "Website terms.",
                  "The terms on which you may use the LaunchNexus website.") + f"""
<section class="section">
  <div class="wrap prose rise">
    <div class="draft-note rise"><strong>Draft.</strong> These are website terms of use only, not terms for a project. Project terms are set out in the written proposal for each piece of work. Have these reviewed before publication.</div>
    <p><strong>Last updated:</strong> <span data-year>2026</span></p>
    <h2>Who we are</h2>
    <p>This site is operated by LaunchNexus Ltd, company number 17333693, registered in England &amp; Wales.</p>
    <h2>Using this site</h2>
    <p>You may use this site for lawful purposes. You must not misuse it by knowingly introducing malicious code or attempting to gain unauthorised access to it or any server or database connected to it.</p>
    <h2>Our content</h2>
    <p>We own or are licensed to use the content on this site. You may view and print pages for your own reference, but you may not reproduce them commercially without our permission.</p>
    <h2>Accuracy</h2>
    <p>Content on this site is provided for general information. It describes services we offer but does not constitute an offer or a quotation. Any project is governed by a separate written proposal and agreement.</p>
    <h2>Liability</h2>
    <p>We do not exclude liability for death or personal injury caused by negligence, or for fraud. Otherwise, we are not liable for loss arising from use of this site. Nothing here affects your statutory rights as a consumer.</p>
    <h2>Governing law</h2>
    <p>These terms are governed by the law of England and Wales, and disputes are subject to the exclusive jurisdiction of the courts of England and Wales.</p>
    <h2>Contact</h2>
    <p><a href="mailto:info@launchnexus.co.uk">info@launchnexus.co.uk</a></p>
  </div>
</section>
"""


PAGES = [
    dict(file="services.html", title="Services | LaunchNexus",
         desc="Personalised CRM systems, websites and apps designed around the way your organisation works.", body=SERVICES),
    dict(file="services-crm.html", title="Custom CRM Development | LaunchNexus",
         desc="Bespoke CRM systems built around your workflow — clients, staff, bookings, payments, forms and reporting.", body=CRM),
    dict(file="services-websites.html", title="Website Design &amp; Development | LaunchNexus",
         desc="Fast, responsive, accessible websites for charities, service businesses and growing organisations.", body=WEBSITES),
    dict(file="services-apps.html", title="Web &amp; Mobile App Development | LaunchNexus",
         desc="Web and mobile applications, internal systems, client portals and MVPs built from your idea.", body=APPS),
    dict(file="work.html", title="Selected Work | LaunchNexus",
         desc="Case studies of custom CRM systems, websites and apps built by LaunchNexus.", body=WORK),
    dict(file="how-it-works.html", title="How It Works | LaunchNexus",
         desc="Our five-stage process from discovery to launch, and how projects are scoped and priced.", body=HOW),
    dict(file="about.html", title="About | LaunchNexus",
         desc="LaunchNexus builds digital tools around the way organisations actually work.", body=ABOUT),
    dict(file="contact.html", title="Start a Project | LaunchNexus",
         desc="Tell us what you'd like to improve, replace or build. Free discovery call, no commitment.",
         body=CONTACT, extra_js=CONTACT_JS),
    dict(file="thanks.html", title="Thanks — we've got it | LaunchNexus",
         desc="Your enquiry has been received.", body=THANKS, noindex=True),
    dict(file="privacy.html", title="Privacy Notice | LaunchNexus",
         desc="How LaunchNexus Ltd handles personal information collected through this website.", body=PRIVACY),
    dict(file="cookies.html", title="Cookie Notice | LaunchNexus",
         desc="What the LaunchNexus website stores on your device.", body=COOKIES),
    dict(file="terms.html", title="Website Terms | LaunchNexus",
         desc="Terms on which you may use the LaunchNexus website.", body=TERMS),
]


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    for page in PAGES:
        html = shell(page, page["body"])
        with open(os.path.join(root, page["file"]), "w", encoding="utf-8") as fh:
            fh.write(html)
        print("wrote", page["file"], len(html), "bytes")

    # keep index.html (hand-written) on the same asset version
    idx = os.path.join(root, "index.html")
    if os.path.exists(idx):
        html = open(idx, encoding="utf-8").read()
        html = re.sub(r'assets/site\.css(\?v=[a-f0-9]+)?', 'assets/site.css?v=%s' % VER, html)
        html = re.sub(r'assets/site\.js(\?v=[a-f0-9]+)?', 'assets/site.js?v=%s' % VER, html)
        open(idx, "w", encoding="utf-8").write(html)
        print("stamped index.html with asset version", VER)

    # sitemap
    urls = ["index.html"] + [p["file"] for p in PAGES if not p.get("noindex")]
    entries = "".join(
        "\n  <url><loc>%s%s</loc></url>" % (SITE, "" if u == "index.html" else u) for u in urls
    )
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % entries
    open(os.path.join(root, "sitemap.xml"), "w").write(sitemap)
    open(os.path.join(root, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % SITE)
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
