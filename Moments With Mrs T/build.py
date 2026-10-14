"""Builds the Moments With Mrs. T static site into ./site from the Webflow export in ./_source.

Run:  python build.py
Content that came from the Webflow CMS (services + blog posts) lives in _source/cms.json.
Page copy lives in this file. Images live in site/assets/img (WebP, named by Webflow asset id).
"""
import html, json, math, re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
OUT = ROOT / "site"
SITE_URL = "https://mrstschair.com"
PHONE, PHONE_TEL = "(330) 249-1042", "+13302491042"
EMAIL = "momentwithmrst@gmail.com"
FACEBOOK = "https://www.facebook.com/tieshia.henry"
# Microsoft Clarity project ID (clarity.microsoft.com → Settings → Setup). Leave "" until the project exists.
CLARITY_ID = "yxqjh4jbps"
LEGAL_UPDATED = "October 14, 2026"

IMGS = json.loads((ROOT / "_source/imgs.json").read_text(encoding="utf-8"))
CMS = json.loads((ROOT / "_source/cms.json").read_text(encoding="utf-8"))
esc = html.escape

# ---------------------------------------------------------------- helpers
def img(aid, alt="", cls="", eager=False, sizes=None, style=""):
    m = IMGS[aid]
    if isinstance(m, str):  # svg
        return f'<img src="/assets/img/{m}" alt="{esc(alt)}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} loading="lazy">'
    attrs = [f'src="/assets/img/{m["f"]}"', f'width="{m["w"]}"', f'height="{m["h"]}"', f'alt="{esc(alt)}"']
    if cls: attrs.append(f'class="{cls}"')
    if style: attrs.append(f'style="{style}"')
    attrs.append('fetchpriority="high"' if eager else 'loading="lazy" decoding="async"')
    return f"<img {' '.join(attrs)}>"

ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.47 8.53a.75.75 0 0 1 1.06-1.06l4 4a.75.75 0 0 1 0 1.06l-4 4a.75.75 0 1 1-1.06-1.06l2.72-2.72H6.5a.75.75 0 0 1 0-1.5h9.69l-2.72-2.72Z"/></svg>'
def btn(label, href="/contact", cls=""):
    return f'<a class="btn {cls}" href="{href}"><span>{label}</span>{ARROW}</a>'

def checks(items, cls="checks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def clean_rich(h):
    h = re.sub(r'\s(id|class)=""', "", h)
    h = h.replace("‍", "")
    h = re.sub(r"<p>\s*(<br>)?\s*</p>", "", h)
    h = re.sub(r"</?(sub|sup)>", "", h)  # Webflow used sub/sup only to shrink headings
    h = re.sub(r"<h2>\s*<strong>(.*?)</strong>\s*</h2>", r"<h2>\1</h2>", h, flags=re.S)
    h = re.sub(r"<h3>\s*<strong>(.*?)</strong>\s*</h3>", r"<h3>\1</h3>", h, flags=re.S)
    h = re.sub(r"<h4>\s*<strong>(.*?)</strong>\s*</h4>", r"<h4>\1</h4>", h, flags=re.S)
    h = h.replace('href="/blog-posts/', 'href="/blog/')
    return h

def read_time(h):
    return max(2, math.ceil(len(re.sub("<[^>]+>", " ", h).split()) / 220))

# ---------------------------------------------------------------- data
SERVICE_ORDER = ["wellness-programs", "life-coach-services-cuyahoga", "resources-for-growth",
                 "wellness-coaching", "online-support-groups", "mental-health-resources"]
SHORT = {"wellness-programs": "Case Management", "life-coach-services-cuyahoga": "Life Coaching",
         "resources-for-growth": "Coping Skills & Workshops", "wellness-coaching": "Family Coaching",
         "online-support-groups": "Communication Skills", "mental-health-resources": "Mental Health & Wellness"}
# The Webflow "short description" for Communication was copy pasted from a trauma service; corrected here.
SHORT_DESC_FIX = {"online-support-groups": "Speak with confidence, listen deeper, and connect better at home, at work, and in your relationships."}
services = {it["fieldData"]["slug"]: it["fieldData"] for it in CMS["svc"]["items"]}
services = [dict(services[s], slug=s) for s in SERVICE_ORDER]
for s in services:
    s["short"] = SHORT_DESC_FIX.get(s["slug"], s["short-description"])
    s["label"] = SHORT[s["slug"]]

POST_ORDER = ["sleep-and-mental-wellness", "non-verbal-communication-skills", "family-communication-mistakes",
              "family-coaching-benefits", "case-management-eligibility-signs", "conflict-resolution-communication"]
posts = {it["fieldData"]["slug"]: dict(it["fieldData"], _published=it.get("lastPublished") or it["createdOn"]) for it in CMS["blog"]["items"]}
posts = [dict(posts[s], slug=s) for s in POST_ORDER]
for p in posts:
    p["body"] = clean_rich(p["post-body"])
    p["mins"] = read_time(p["body"])

# ---------------------------------------------------------------- chrome
NAV = [("About", "/about"), ("Services", "/services"), ("FAQs", "/faq"), ("Blog", "/blog")]

def header(active):
    links = "".join(f'<a class="link" href="{h}"{" aria-current=page" if active == h else ""}>{t}</a>' for t, h in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><a href="tel:{PHONE_TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Serving Lorain &amp; Cuyahoga County + virtual</span></div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/" aria-label="Moments With Mrs. T home">{img("68267156818e6f818f09be5c", "Moments With Mrs. T", eager=True)}</a>
  <button class="menu-toggle" data-menu aria-controls="nav" aria-expanded="false" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  <nav class="nav" id="nav" aria-label="Main">
    <button class="menu-toggle nav-close" data-menu aria-label="Close menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    {links}{btn("Book a free consultation", "/contact", "small")}
  </nav>
</div></header><div class="scrim"></div>"""

FB_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.3v3.2h2.8V22h3.4Z"/></svg>'

def footer():
    svc_links = "".join(f'<li><a href="/services/{s["slug"]}">{s["label"]}</a></li>' for s in services)
    return f"""<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div>
      {img("68267156818e6f818f09be5c", "Moments With Mrs. T", cls="logo")}
      <h2>Start your path to mental wellness</h2>
      <p>Even thinking about looking for guidance means you're in the right place. I'm ready when you are.</p>
      {btn("Book your session", "/contact", "light")}
      <div class="social"><a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Tieshia Henry on Facebook">{FB_ICON}</a></div>
    </div>
    <div><h3>Explore</h3><ul><li><a href="/">Home</a></li><li><a href="/about">About</a></li><li><a href="/services">Services</a></li><li><a href="/blog">Blog</a></li><li><a href="/faq">FAQs</a></li><li><a href="/contact">Contact</a></li></ul></div>
    <div><h3>Services</h3><ul>{svc_links}</ul>
      <h3 style="margin-top:28px">Contact</h3><ul><li><a href="tel:{PHONE_TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
  </div>
  <div class="footer-bottom">
    <span>© <span data-year>{date.today().year}</span> Moments With Mrs. T. All rights reserved.</span>
    <nav aria-label="Legal"><a href="/privacy-policy-terms-and-agreements">Privacy Policy</a><a href="/privacy-policy-terms-and-agreements#terms">Terms of Service</a><a href="/privacy-policy-terms-and-agreements#cookies" data-privacy-choices>Privacy choices</a></nav>
    <span>Website designed with ❤️ by <a href="https://blackmine.dev/" target="_blank" rel="noopener">BlackMine</a></span>
  </div>
</div></footer>"""

LD_BUSINESS = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Moments With Mrs. T",
    "description": "Life coaching, case management, family coaching and coping skills workshops in Lorain & Cuyahoga County, Ohio, plus virtual sessions.",
    "url": SITE_URL, "telephone": "+1-330-249-1042", "email": EMAIL, "image": SITE_URL + "/assets/og-image.jpg",
    "founder": {"@type": "Person", "name": "Tieshia Henry", "jobTitle": "Founder & Certified Life Coach"},
    "areaServed": [{"@type": "AdministrativeArea", "name": "Lorain County, OH"}, {"@type": "AdministrativeArea", "name": "Cuyahoga County, OH"}],
    "foundingDate": "2023", "sameAs": [FACEBOOK],
}

def page(path, title, desc, body, active=None, ld=None, og_image="/assets/og-image.jpg"):
    body = auto_seams(body)
    canon = SITE_URL + ("/" if path == "/" else path)
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    doc = f"""<!doctype html>
<html lang="en" class="no-js" data-clarity="{CLARITY_ID}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Moments With Mrs. T">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d3c5e">
<link rel="icon" href="/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/EncodeSans-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Karla-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/styles.css">
<link rel="stylesheet" href="/assets/css/depth.css">
<script>document.documentElement.className="js"</script>
{lds}
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/main.js" defer></script>
<script src="/assets/js/motion.js" type="module"></script>
<script src="/assets/js/consent.js" type="module"></script>
</body>
</html>
"""
    f = OUT / ("index.html" if path == "/" else path.strip("/") + ".html")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc, encoding="utf-8")
    SITEMAP.append(canon)

SITEMAP = []

# ---------------------------------------------------------------- shared sections (v2: layered depth)
def leaf_divider():
    return f'<div class="leaf-divider reveal" aria-hidden="true">{img("6826c1079272fef62799461b")}{img("6826c1079272fef62799461b", cls="flip")}</div>'

def layer_img(src, cls, depth=None, pointer=None, alt=""):
    d = f' data-depth="{depth}"' if depth is not None else ""
    p = f' data-pointer="{pointer}"' if pointer is not None else ""
    return f'<img src="{src}" class="{cls}" alt="{alt}" aria-hidden="true" loading="lazy"{d}{p}>'

def navy_layers(ghost="r"):
    return (f'<div class="navy-layers" aria-hidden="true"><img class="palm" src="/assets/layers/palm-shadow.webp" alt="" loading="lazy">'
            f'<div class="glow"></div><div class="border"></div></div>'
            f'<img class="ghostmark {ghost}" src="/assets/layers/logo-mark-white.webp" alt="" aria-hidden="true" loading="lazy">')



def booking_form(fid):
    svc_opts = "".join(f"<option>{s['label']}</option>" for s in services)
    return f"""<form class="form" novalidate aria-label="Book a consultation" data-clarity-mask="True">
    <div class="row">
      <label>Name<input name="Name" autocomplete="name" required></label>
      <label>Phone<input name="Phone" type="tel" autocomplete="tel" required></label>
    </div>
    <label>Email<input name="Email" type="email" autocomplete="email" required></label>
    <div class="row">
      <label>Best time to reach you<select name="Best time" required><option value="">Choose a time</option><option>Morning (9am–12pm)</option><option>Afternoon (12pm–4pm)</option><option>Evening (4pm–7pm)</option></select></label>
      <label>I'm interested in<select name="Interested in"><option>Not sure yet</option>{svc_opts}</select></label>
    </div>
    <label>Anything you'd like Mrs. T to know?<textarea name="Message"></textarea></label>
    <label class="hp" aria-hidden="true">Leave blank<input name="_honey" tabindex="-1" autocomplete="off"></label>
    <label class="check"><input type="checkbox" name="SMS consent" value="Yes — appointment texts OK"><span>Optional: text me appointment confirmations and reminders from Moments With Mrs. T. Message frequency varies. Msg &amp; data rates may apply. Reply STOP to opt out, HELP for help. Consent is not required to book.</span></label>
    <span class="consent">We use your details only to respond and schedule — never for marketing, and never sold. See the <a href="/privacy-policy-terms-and-agreements">Privacy Policy</a> and <a href="/privacy-policy-terms-and-agreements#terms">Terms</a>.</span>
    <button class="btn" type="submit">Request my consultation</button>
    <div class="form-status" role="status" aria-live="polite"></div>
  </form>"""

WHY = [
    ("5-star client experience", "Personalized, quality care you can trust.", '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z"/>'),
    ("Compassion-first approach", "I care because I've been there.", '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z"/>'),
    ("Real results", "Move from feeling stuck to thriving with proven strategies.", '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>'),
    ("Local & caring", "Rooted in the Lorain, Cuyahoga, and Strongsville community.", '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12Z"/><circle cx="12" cy="9" r="2.5"/>'),
    ("Affordable packages", "Tailored support without breaking the bank.", '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2Z"/><path d="M9 8h6M9 12h6"/>'),
]


def service_cards(limit=None, photos=True):
    out = []
    for s in services[:limit]:
        thumb = f'<div class="thumb-wrap">{img(s["photo-service"]["fileId"], "", cls="thumb")}</div>' if photos else ""
        icon = img(s["main-image"]["fileId"], "", cls="icon")
        out.append(f'<a class="card reveal" data-tilt href="/services/{s["slug"]}">{thumb}<div class="body">{icon}<h3>{esc(s["label"])}</h3><p>{esc(s["short"])}</p><span class="more">Learn more <span aria-hidden="true">→</span></span></div></a>')
    return f'<div class="cards">{"".join(out)}</div>'

def post_cards(items):
    out = []
    for p in items:
        summ = p["post-summary"][:150].rsplit(" ", 1)[0] + ("…" if len(p["post-summary"]) > 150 else "")
        out.append(f'<a class="card reveal" data-tilt href="/blog/{p["slug"]}"><div class="thumb-wrap">{img(p["thumbnail-image"]["fileId"], p.get("alt-text") or "", cls="thumb")}</div><div class="body"><span class="meta">{p["mins"]} min read</span><h3>{esc(p["name"])}</h3><p>{esc(summ)}</p><span class="more">Read more <span aria-hidden="true">→</span></span></div></a>')
    return f'<div class="cards">{"".join(out)}</div>'


FAQ_SHORT = [
    ("What makes Moments With Mrs. T different from other life coaching services?", "My compassionate, lived-experience approach combined with certified expertise creates a genuinely nurturing environment for transformation."),
    ("How long are your programs?", "Programs range from 3 to 12 months, tailored to your personal growth needs."),
    ("Do you offer group sessions?", "Yes! I provide both one-on-one and group workshop sessions for coping skills and life strategy building."),
    ("Can life coaching sessions be virtual?", "Yes, I offer both in-person and virtual coaching sessions for your convenience."),
    ("What ages do you serve?", "I work with children starting in the 4th grade up to adults seeking guidance, healing, and empowerment."),
]
FAQ_LONG = [
    ("What makes Moments With Mrs. T different from other life coaching services?", "<p>A blend of genuine empathy and professional certification. I bring lived experience to every session, which creates a supportive environment for real personal growth and transformation.</p>"),
    ("How long are your programs?", "<p>Programs range from 3 to 12 months, designed around your goals, challenges, and strengths.</p>"),
    ("Can coaching help with seasonal stress or winter depression?", "<p>Absolutely. Seasonal Affective Disorder (SAD) is very real in Ohio. The long, dark winters and gray skies in Cuyahoga and Lorain can deeply affect your mood. I help you build coping strategies that keep you grounded, energized, and emotionally balanced — no matter the season.</p><p><a href=\"/services/wellness-coaching\">Family Coaching</a> also helps reduce seasonal stress at home.</p>"),
    ("What if I don't know where to start?", "<p>That's perfectly OK. These services are built for people who feel overwhelmed, unsure, or just need a starting point. Begin by <a href=\"/contact\">scheduling a free consultation</a> and I'll help guide your path forward — without pressure or judgment.</p>"),
    ("Do you take insurance?", "<p>I don't currently accept insurance, but rates are affordable and flexible, with discounts for long-term commitments and bundled sessions.</p>"),
    ("Is this service available in person or online?", "<p>Both! I serve clients across Cuyahoga, Lorain, and Strongsville in person, and I also offer secure virtual sessions — especially helpful during tough Ohio winters when travel is hard.</p>"),
    ("Do you offer group sessions or family-based coaching?", "<p>Yes! Many clients find group coaching comforting and relatable. Family sessions are also available for improving communication, rebuilding trust, or healing after difficult times.</p><p>See <a href=\"/services/wellness-coaching\">Family Coaching</a> and <a href=\"/services/resources-for-growth\">Coping Skills &amp; Workshops</a> to learn more.</p>"),
    ("What ages do you serve? Do you help teens?", "<p>I work with children starting in the 4th grade, teens, and adults — especially those navigating big changes, family conflict, or emotional overwhelm. Sessions are always adapted to fit the age and needs of the individual.</p>"),
    ("Is this therapy?", "<p>No. Life coaching and case management are forward-focused and action-based. They're a great fit alongside clinical care, but they aren't a replacement for it. If you're in crisis, call or text <a href=\"tel:988\">988</a> (Suicide &amp; Crisis Lifeline) or dial 911.</p>"),
    ("Are results guaranteed?", "<p>Every journey is unique. What I can guarantee is my commitment to your progress, honest feedback, and professional support every step of the way. Transformation takes time, and I'm with you for the long haul.</p>"),
]

CRISIS = f"""<div class="crisis reveal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10Z"/></svg><p style="margin:0"><strong>In crisis or thinking about harming yourself?</strong> Coaching isn't emergency care. Call or text <a href="tel:988">988</a> (Suicide &amp; Crisis Lifeline) any time, or dial 911.</p></div>"""

def faq_block(items, open_first=True):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"{" open" if (i == 0 and open_first) else ""}><summary>{esc(q)}</summary><div>{a if a.startswith("<") else f"<p>{a}</p>"}</div></details>' for i, (q, a) in enumerate(items)) + "</div>"
def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}



def photo_stack(main, alt, inset=None, inset_alt="", ratio="4/5", badge=""):
    ins = img(inset, inset_alt, cls="inset") if inset else ""
    return f"""<div class="stack reveal">
    <div class="back" data-depth="0.25" aria-hidden="true"></div>
    {img(main, alt, cls="main", style=f"aspect-ratio:{ratio}")}
    {ins}
    {layer_img("/assets/img/6826713a4d81fd6d0725b0f7.webp", "leafy tl", depth=-0.25)}
    {layer_img("/assets/img/6826713ad95c622675c96b76.webp", "leafy br", depth=-0.3)}
    {badge}
  </div>"""



ICON = {
    "free": '<path d="M20 12v9H4v-9M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7Zm0 0h4.5a2.5 2.5 0 1 0 0-5C13 2 12 7 12 7Z"/>',
    "where": '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12Z"/><circle cx="12" cy="9" r="2.5"/>',
    "video": '<rect x="2" y="6" width="14" height="12" rx="3"/><path d="m16 10 6-3v10l-6-3"/>',
}
def chip(cls, icon, text, pointer):
    return f'<div class="chip {cls}" data-pointer="{pointer}"><span class="dot"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[icon]}</svg></span>{text}</div>'

def hero_stage(cutout="tieshia-cutout.webp"):
    return f"""<div class="stage load" style="--d:3" data-pointer-scene>
    <div class="breath" aria-hidden="true"></div>
    <div class="layer" data-pointer="-6"><div class="arch" aria-hidden="true"></div></div>
    <div class="layer" data-pointer="4"><div class="person"><img src="/assets/layers/{cutout}" width="510" height="587" alt="Tieshia Henry, founder of Moments With Mrs. T and certified life coach" fetchpriority="high"></div></div>
    <div class="layer" data-pointer="14">{img("6826713b4b223a3a25c3cfa7", cls="leaf l2")}{img("6826713a9d2f9f610554745f", cls="leaf l1")}{img("6826713a05a08f242905e3cc", cls="leaf l3")}</div>
    {chip("c1", "free", "Free consultation", "10")}
    {chip("c2", "video", "In person or virtual", "8")}
    <div class="sig-card"><span class="sig">Tieshia Henry</span><small>Founder &amp; CEO</small></div>
  </div>"""

# ---------------------------------------------------------------- v3: tones + intentional edges
EDGE_PATHS = {
    "wave": ("M0 70C160 30 300 20 470 46s300 62 480 40 330-70 490-48V120H0Z", "M0 92c180-34 360-40 540-14s340 40 520 14 300-46 380-40V120H0Z"),
    "arch": ("M0 120V66Q720 -14 1440 66V120Z", "M0 120V90Q720 22 1440 90V120Z"),
    "dip":  ("M0 30Q720 150 1440 30V120H0Z", "M0 64Q720 160 1440 64V120H0Z"),
    "hill": ("M0 50C300 110 700 0 1000 40S1300 90 1440 60V120H0Z", "M0 84C360 40 620 120 980 80S1300 50 1440 92V120H0Z"),
}
TONE = {"cream": "var(--c-cream)", "sage": "var(--c-sage)", "sand": "var(--c-sand)", "mist": "var(--c-mist)",
        "mintl": "var(--c-mintl)", "green": "var(--c-green-1)", "navy": "var(--c-navy)", "deep": "var(--navy-deep)"}
SPRIGS = ["6826713a9d2f9f610554745f", "6826713b4b223a3a25c3cfa7", "6826713a4d81fd6d0725b0f7", "6826713ad95c622675c96b76", "6826713abd083aa53006a2ea"]
_sprig_i = [0]
def edge(to, kind="wave", sprig=None, top=False, vine=False):
    b, f = EDGE_PATHS[kind]
    extra = ""
    if sprig:
        sid = SPRIGS[_sprig_i[0] % len(SPRIGS)]; _sprig_i[0] += 1
        extra += f'<img class="sprig {sprig}" src="/assets/img/{sid}.webp" alt="" loading="lazy">'
    if vine:
        extra += '<img class="vine" src="/assets/img/6826c1079272fef62799461b.webp" alt="" loading="lazy">'
    return (f'<div class="edge{" top" if top else ""}" style="--to:{TONE[to]}" aria-hidden="true">'
            f'<svg class="b" viewBox="0 0 1440 120" preserveAspectRatio="none"><path d="{b}"/></svg>'
            f'<svg viewBox="0 0 1440 120" preserveAspectRatio="none"><path d="{f}"/></svg>{extra}</div>')

def horizon(to="cream", kind="wave"):
    # inner-page banner seam: banner -> first section
    return f'<div style="position:relative;height:0">{edge(to, kind, sprig="r")}</div>'

def consult_section(title="Take the first step toward improving your mental well-being today.",
                    text="Whether you're looking for a personalized game plan, group support, or a wellness program, Tieshia is here to guide you.",
                    eyebrow="Book a free consultation", tone=None, to=None, kind="wave", form_id="book"):
    e = edge(to, kind, sprig="l") if to else ""
    return f"""<section class="section{(" tone-" + tone) if tone else ""}{" edged" if to else ""}" id="{form_id}"><div class="wrap"><div class="consult reveal">
  {navy_layers("l")}
  <div>
    <span class="eyebrow light">{eyebrow}</span>
    <h2 data-split>{title}</h2>
    <p>{text}</p>
    <ul><li>Get tailored advice based on where you are right now.</li><li>Talk through your specific needs and build a personalized plan.</li><li>Confidential, compassionate support — no judgment.</li></ul>
    <div class="direct"><span>Prefer to talk now?</span><a href="tel:{PHONE_TEL}">Call {PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
  {booking_form(form_id)}
</div></div>{e}</section>"""

def why_section(tone=None, to=None, kind="hill"):
    items = "".join(f'<div class="why-item reveal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg><h3>{t}</h3><p>{d}</p></div>' for t, d, p in WHY)
    words = ["Wholeness", "Mindfulness", "Freedom", "Balance", "Compassion", "Empowerment", "Integrity", "Collaboration"]
    row = "".join(f"<li><b>{w}</b></li>" for w in words)
    e = edge(to, kind, sprig="r") if to else ""
    return f"""<section class="section{(" tone-" + tone) if tone else ""}{" edged" if to else ""}" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div>
  <div class="blob sage" style="width:480px;height:480px;left:-160px;top:10%" data-depth="0.2" aria-hidden="true"></div>
  <div class="wrap">
  <div class="center reveal"><span class="eyebrow">The moments matter</span><h2 data-split>Why choose Moments With Mrs. T?</h2></div>
  <div class="why" style="margin-top:36px">{items}</div>
  </div>
  <div class="marquee" style="margin-top:44px" aria-hidden="true"><ul>{row}</ul><ul>{row}</ul></div>
{e}</section>"""

def blog_section(title="Discover valuable resources", exclude=None, tone=None, to=None, kind="wave"):
    items = [p for p in posts if p["slug"] != exclude][:3]
    e = edge(to, kind, sprig="l") if to else ""
    return f"""<section class="section{(" tone-" + tone) if tone else ""}{" edged" if to else ""}" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap">
  <div class="reveal" style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:36px">
    <div><span class="eyebrow" style="background:#fff">Mrs. T's Chair — the blog</span><h2 style="margin:0" data-split>{title}</h2></div>
    {btn("All articles", "/blog", "ghost small")}
  </div>
  {post_cards(items)}
</div>{e}</section>"""

def faq_section(tone=None, to=None, kind="arch"):
    e = edge(to, kind) if to else ""
    return f"""<section class="section{(" tone-" + tone) if tone else ""}{" edged" if to else ""}" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div>
  <img class="ghostmark r" src="/assets/layers/logo-mark.webp" alt="" aria-hidden="true" loading="lazy">
  <div class="wrap">
  <div class="center reveal" style="margin-bottom:36px"><span class="eyebrow" style="background:#fff">FAQs</span><h2 data-split>Questions I hear often</h2><p class="lead">Here to answer your worries and put your mind at ease.</p></div>
  {faq_block(FAQ_SHORT)}
  {CRISIS}
  <p class="center" style="margin-top:28px"><a href="/faq">See all FAQs →</a></p>
</div>{e}</section>"""

def meet_tieshia(tone=None, to=None, kind="hill", photo="69bf2ac5b74b01ad68f9dafa", photo_alt="Tieshia Henry, founder of Moments With Mrs. T and certified life coach"):
    badge = '<div class="chip badge"><span class="dot"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z"/></svg></span>Certified Life Coach</div>'
    e = edge(to, kind, sprig="r") if to else ""
    return f"""<section class="section{(" tone-" + tone) if tone else ""}{" edged" if to else ""}" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div><div class="wrap split">
  {photo_stack(photo, photo_alt, badge=badge)}
  <div class="reveal">
    <span class="eyebrow">Meet your coach</span>
    <h2 data-split>Meet Tieshia Henry</h2>
    <p style="font-weight:600;color:var(--navy)">Founder &amp; Certified Life Coach · Passionate | Empathetic | Purpose-driven</p>
    <p>Tieshia brings a rare blend of professional expertise and real-world understanding to every coaching session. With a natural gift for encouraging others and a heart fueled by service, she's committed to helping clients feel empowered, validated, and hopeful — every step of the way.</p>
    {btn("Book a consultation", "/contact")}
  </div>
</div>{e}</section>"""

def roots_section(tone=None, to=None, kind="wave"):
    e = edge(to, kind, sprig="l") if to else ""
    return f"""<section class="section{(" tone-" + tone) if tone else ""}{" edged" if to else ""}" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap split reverse">
  {photo_stack("68269cecaa5f55bde312e14a", "Tieshia Henry with family and friends", inset="690947824620ec722b9268f7", inset_alt="Tieshia with clients", ratio="4/3")}
  <div class="reveal">
    <span class="eyebrow" style="background:#fff">Our story</span>
    <h2 data-split>The roots of Moments With Mrs. T</h2>
    <p class="lead">The seeds were planted in 2019, when Tieshia recognized a deeper calling — a desire to help others move beyond pain, uncertainty, and past trauma.</p>
    <p>Officially launched in 2023 after extensive coursework and Life Coach certification, Moments With Mrs. T is the culmination of personal experience, professional training, and an unwavering passion for people.</p>
    {btn("Book a consultation", "/contact")}
  </div>
</div>{e}</section>"""

def chair_section(tone="sand", to="cream", kind="arch"):
    return f"""<section class="section chair2 tone-{tone} edged" style="overflow:hidden">
  <div class="blob sand" style="width:560px;height:560px;right:-180px;top:40px;opacity:.9" data-depth="0.2" aria-hidden="true"></div>
  <div class="blob mint" style="width:420px;height:420px;left:-140px;bottom:0" data-depth="0.2" aria-hidden="true"></div>
  <div class="motif tr" aria-hidden="true"></div>
  <div class="wrap split">
  <div class="chair-frame reveal">
    <div class="ring" data-depth="0.25"></div>
    <div class="arch-img"><img src="/assets/layers/chair-scene.webp" alt="An illustrated armchair in a calm, sunlit room — Mrs. T's Chair" loading="lazy"></div>
    {img("6826713a4d81fd6d0725b0f7", cls="leaf-a")}{img("6826713b4b223a3a25c3cfa7", cls="leaf-b")}
    {chip("", "free", "Pull up a chair", "0").replace(' data-pointer="0"', '')}
  </div>
  <div class="reveal">
    <span class="eyebrow" style="background:#fff">Where healing begins</span>
    <h2 class="script">Mrs. T's Chair</h2>
    <p><em>Mrs. T's Chair</em> isn't just a name — it's a symbol of <strong>stillness</strong>, <strong>safety</strong>, and <strong>support</strong>. It's where the overwhelmed parent finally exhales. It's where the teen who's been misunderstood finds their voice. It's where organizations send those they care about most — because they know they'll be met with <strong>warmth</strong>, <strong>wisdom</strong>, and <strong>real help</strong>.</p>
    <p><strong>This chair represents a moment to pause and breathe</strong> — without judgment, without pressure. Just guidance, healing, and the kind of care that transforms lives.</p>
    {btn("Come sit with Mrs. T", "/contact")}
  </div>
</div>{edge(to, kind, vine=True)}</section>"""

def banner(h1, lead, crumbs=None, cta=True, cta_href="/contact", cta_label="Let's talk", to="cream"):
    cr = f'<div class="crumbs">{crumbs}</div>' if crumbs else ""
    return f"""<section class="banner">{navy_layers()}<div class="motif tr light" aria-hidden="true"></div><div class="wrap">{cr}
  <h1 data-split>{h1}</h1><p class="lead reveal">{lead}</p>
  <div class="reveal">{checks(["From pain to purpose", "Tailored to your journey", "Real healing, real talk"])}</div>
  {f'<div class="reveal">{btn(cta_label, cta_href, "light")}</div>' if cta else ""}
</div></section>"""


# ---------------------------------------------------------------- auto seams
# Every top-level section gets a tone that differs from its neighbours, and every seam
# gets a drawn edge painted in the next section's color (unless one was placed by hand).
CYCLE = ["cream", "sage", "sand", "mist"]
KINDS = ["wave", "hill", "dip", "arch"]
def _sections(body):
    out, i = [], 0
    for m in re.finditer(r"<section\b[^>]*>|</section>", body):
        if m.group().startswith("<section"):
            if i == 0: start, open_tag = m.start(), m.group()
            i += 1
        else:
            i -= 1
            if i == 0: out.append([start, m.end(), open_tag])
    return out

def _tone(tag):
    m = re.search(r"tone-(\w+)", tag)
    if m: return m.group(1)
    if "bg-navy" in tag or "banner" in tag: return "navy"
    if "journey" in tag: return "photo"
    if "hero" in tag: return "cream"
    if "trust" in tag: return "skip"
    return None

def auto_seams(body):
    secs = _sections(body)
    tones = [_tone(s[2]) for s in secs]
    rot = 0
    for i, t in enumerate(tones):
        if "data-same" in secs[i][2] and i: tones[i] = tones[i - 1]; continue
        if t is None:
            prev = tones[i - 1] if i else None
            nxt = next((x for x in tones[i + 1:] if x not in (None, "skip")), None)
            for j in range(4):
                c = CYCLE[(rot + j) % 4]
                if c not in (prev, nxt): tones[i] = c; rot = rot + j + 1; break
    pieces, last, k = [], 0, 0
    for i, (s, e, tag) in enumerate(secs):
        chunk = body[s:e]
        t = tones[i]
        if _tone(tag) is None and "data-same" not in tag:
            chunk = re.sub(r'class="', f'class="tone-{t} ', chunk, count=1) if 'class="' in tag else chunk.replace("<section", f'<section class="tone-{t}"', 1)
        if "data-same" in tag:
            chunk = re.sub(r'class="', f'class="tone-{t} ', chunk, count=1)
        nxt = tones[i + 1] if i + 1 < len(secs) else "deep"
        nxt_same = i + 1 < len(secs) and "data-same" in secs[i + 1][2]
        has_edge = re.search(r'class="edge[" ]', chunk[-2500:]) is not None
        if not has_edge and not nxt_same and t not in ("skip",) and nxt not in ("skip", "photo") and nxt != t and not (t == "cream" and "hero" in tag and nxt == "skip"):
            ed = edge(nxt, KINDS[k % 4], sprig=("l" if k % 2 else "r") if k % 3 != 2 else None); k += 1
            chunk = re.sub(r'class="', 'class="edged ', chunk, count=1)
            chunk = chunk[: chunk.rfind("</section>")] + ed + "</section>"
        pieces.append(body[last:s]); pieces.append(chunk); last = e
    pieces.append(body[last:])
    return "".join(pieces)

# ---------------------------------------------------------------- HOME
FEELINGS_A = [("Overwhelmed", "steady"), ("Stuck", "moving"), ("Alone", "supported"), ("Anxious", "grounded"), ("Burned out", "restored"), ("Unheard", "understood")]
FEELINGS_B = [("Grieving", "healing"), ("Disconnected", "close again"), ("Uncertain", "clear"), ("Exhausted", "rested"), ("Broken", "whole"), ("Doubting", "confident")]
def marquee_rows():
    def row(items): return "".join(f"<li>{a}<i>→</i><b>{b}</b></li>" for a, b in items)
    a, b = row(FEELINGS_A), row(FEELINGS_B)
    return (f'<div class="marquee"><ul>{a}</ul><ul aria-hidden="true">{a}</ul></div>'
            f'<div class="marquee rev"><ul>{b}</ul><ul aria-hidden="true">{b}</ul></div>')

PICKS = [("I'm overwhelmed and need structure", "Organize life, appointments, and resources.", "Case Management", "wellness-programs"),
         ("I want to grow and set goals", "Clarity, confidence, and a plan you'll keep.", "Life Coaching", "life-coach-services-cuyahoga"),
         ("My family needs help connecting", "Rebuild trust and talk to each other again.", "Family Coaching", "wellness-coaching"),
         ("I need tools to cope day to day", "Practical skills for stress and big emotions.", "Coping Skills", "resources-for-growth")]

def build_home():
    steps = [("6826713a9d2f9f610554745f", "Reach out", "Call or email to start the conversation — no pressure, just connection."),
             ("6826713abd083aa53006a2ea", "Free consultation", "We talk about where you are and where you want to go."),
             ("6826713a05a08f242905e3cc", "Your plan", "Choose a 3–12 month journey designed around your goals, challenges, and strengths."),
             ("68269dcfd1127426fc34b592", "Grow together", "Experience real change — with space for feedback and continued support whenever you need it.")]
    steps_html = "".join(f'<div class="step reveal"><span class="num" aria-hidden="true">0{n}</span>{img(i)}<h3>{t}</h3><p>{d}</p></div>' for n, (i, t, d) in enumerate(steps, 1))
    pillars = [("Comprehensive support", "Case management, coaching, and resources under one roof."),
               ("Personalized care", "A plan built around your life, not a template."),
               ("Compassionate community", "Group workshops where you're understood."),
               ("Accessibility & support", "In person in Lorain & Cuyahoga, or virtual from anywhere."),
               ("Planning proactively", "Tools to handle what's next before it overwhelms you."),
               ("Empowering growth", "Confidence and independence that last beyond our sessions.")]
    pillars_html = "".join(f'<div class="pillar reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in pillars)
    picks_html = "".join(f'<a class="pick reveal" href="/services/{slug}"><strong>{t}</strong><span>{d}</span><em>{lbl} →</em></a>' for t, d, lbl, slug in PICKS)
    locs = "".join(f'<div class="loc reveal"><h3>{n}</h3><a href="tel:{PHONE_TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>' for n in ["Lorain County", "Cuyahoga County", "Virtual sessions"])
    body = f"""
<section class="hero">
  <div class="blob sage b1" data-depth="0.2" aria-hidden="true"></div><div class="blob sky b2" data-depth="0.2" aria-hidden="true"></div><div class="blob sand b3" data-depth="0.2" aria-hidden="true"></div>
  <img class="palm" src="/assets/layers/palm-shadow.webp" alt="" aria-hidden="true">
  <div class="motif bl" aria-hidden="true"></div>
  <div class="wrap hero-grid">
  <div>
    <span class="eyebrow load" style="--d:0">Empowering your mental well-being</span>
    <h1 data-split>Moments With Mrs.&nbsp;T <span class="accent">Life Coaching &amp; Case Management in Lorain &amp; Cuyahoga County</span></h1>
    <p class="lead load" style="--d:2">Helping overwhelmed parents, teens, and women rebuild confidence and emotional strength. Coaching for women, families, and caregivers who are ready to heal, rebuild, and grow — without judgment.</p>
    <div class="load" style="--d:3">{checks(["Real healing, real talk", "Tailored to your journey", "From pain to purpose"])}</div>
    <div class="load" style="--d:4">{btn("Come sit with Mrs. T", "/contact")}</div>
    <div class="verse load" style="--d:5">“I am the vine; you are the branches.” — <a href="https://www.biblegateway.com/passage/?search=John%2015&amp;version=NIV" target="_blank" rel="noopener">John 15:5</a></div>
  </div>
  {hero_stage()}
</div></section>

<section class="trust" aria-label="At a glance"><div class="wrap"><div class="reveal">
  <div class="t"><div class="n"><span data-count="6">6</span></div><div class="l">Services under one roof</div></div>
  <div class="t"><div class="n">3–12<small>mo</small></div><div class="l">Journeys built around you</div></div>
  <div class="t"><div class="n"><span data-count="2">2</span><small>+ virtual</small></div><div class="l">Counties served in person</div></div>
  <div class="t"><div class="n">4th<small>grade → adult</small></div><div class="l">Ages welcomed</div></div>
</div></div></section>

<section class="feelings tone-cream edged" style="position:relative" aria-label="From how you feel to where you're headed">
  <h2 class="reveal">Wherever you are right now, there's a way forward.</h2>
  {marquee_rows()}
  {edge("sage", "wave", sprig="r")}
</section>

<section class="section who tone-sage edged" style="overflow:hidden;padding-top:clamp(40px,5vw,70px)">
  <div class="blob mint" style="width:620px;height:620px;left:-220px;top:40px" data-depth="0.2" aria-hidden="true"></div>
  <div class="blob sky" style="width:460px;height:460px;right:-160px;bottom:10%" data-depth="0.2" aria-hidden="true"></div>
  <div class="motif tr" aria-hidden="true"></div>
  <div class="wrap">
  <div class="center reveal" style="margin-bottom:36px"><span class="eyebrow" style="background:#fff">Is this right for you?</span><h2 data-split>Who this is for</h2></div>
  <div class="fit">
    <div class="fit-card glass reveal"><h3>This is for you if you're…</h3><ul><li>An overwhelmed parent needing support</li><li>A teen struggling with communication or identity</li><li>A woman navigating trauma, stress, or life transitions</li><li>A family needing guidance and emotional tools</li></ul></div>
    <div class="fit-card not glass reveal"><h3>This isn't the right fit if you're…</h3><ul><li>Unwilling to engage in the healing process</li><li>Seeking crisis clinical therapy (call or text <a href="tel:988">988</a> any time)</li><li>Looking for quick fixes without personal work</li></ul></div>
  </div>
  <div class="leaf-divider reveal" aria-hidden="true" style="margin:64px auto 8px">{img("6826c1079272fef62799461b")}</div>
  <div class="center reveal"><span class="eyebrow" style="background:#fff">Not sure where to start?</span><h2 data-split>Where are you right now?</h2></div>
  <div class="picker">{picks_html}</div>
</div>
  {edge("sand", "hill", sprig="l")}
</section>

{chair_section(tone="sand", to="cream", kind="arch")}

<section class="section tone-cream edged" style="overflow:hidden;padding-top:clamp(40px,5vw,70px)"><div class="motif tr" aria-hidden="true"></div><div class="wrap split">
  {photo_stack("68269cecaa5f55bde312e14a", "Tieshia Henry with family and friends", inset="690947824620ec722b9268f7", inset_alt="Tieshia with clients", ratio="4/3")}
  <div class="reveal">
    <span class="eyebrow">About</span>
    <h2 data-split>About Moments With Mrs. T</h2>
    <p class="lead">Healing and moving forward should be a supported, empowering journey.</p>
    <p>I'm Tieshia Henry, a certified life coach with a heart for service. I founded Moments With Mrs. T in 2023 to offer wraparound services that help you acknowledge, process, and triumph over life's challenges.</p>
    <p>My approach blends case management, coping strategies, and personalized care, so you never have to walk the path alone. I'm proudly based in Lorain County and serve the surrounding Cuyahoga areas with dedication and compassion.</p>
    {btn("More about Mrs. T", "/about", "ghost")}
  </div>
</div>
  {edge("green", "dip", sprig="r")}
</section>

<section class="section tone-green edged" style="overflow:hidden">
  <div class="motif tr" aria-hidden="true"></div>
  <div class="blob" style="width:640px;height:640px;right:-220px;top:40px;background:#3f8a7b;opacity:.45" data-depth="0.2" aria-hidden="true"></div>
  <img class="ghostmark l" src="/assets/layers/logo-mark-white.webp" alt="" aria-hidden="true" loading="lazy" style="opacity:.07">
  <div class="wrap">
  <div class="center reveal" style="margin-bottom:44px"><span class="eyebrow">How I can help</span><h2 data-split>Explore the core services</h2><p class="lead">Coaching and wellness services tailored to help you heal, grow, and thrive — at your own pace and in your own way.</p></div>
  {service_cards()}
  <p class="center reveal" style="margin-top:40px">{btn("See all services", "/services", "light")}</p>
</div>
  {edge("cream", "wave", sprig="l")}
</section>

<section class="section tone-cream edged" style="overflow:hidden"><div class="wrap split">
  <div class="video-stack reveal">
    <div class="frame" data-depth="0.3" aria-hidden="true"></div>
    <div class="video-panel"><video autoplay muted loop playsinline preload="none" poster="/assets/video/pottery-poster.jpg" aria-hidden="true"><source src="/assets/video/pottery.mp4" type="video/mp4"></video><div class="caption">Molding broken pieces into purposeful wholeness</div></div>
    <div class="quote glass" data-depth="-0.3">Reshape what's been cracked. Mold new strength where there once was pain.</div>
  </div>
  <div class="reveal">
    <span class="eyebrow">My approach</span>
    <h2 data-split>Mental health conversations should be open</h2>
    <p class="lead">My approach is gentle, intentional, and rooted in restoration.</p>
    <p>I help you reshape what's been cracked, smooth what's been rough, and mold new strength where there once was pain.</p>
    {btn("Come sit with Mrs. T", "/contact")}
  </div>
</div>
  {edge("mist", "hill", sprig="r")}
</section>

<section class="section tone-mist edged" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div>
  <div class="blob sky" style="width:520px;height:520px;right:-180px;top:40px" data-depth="0.2" aria-hidden="true"></div>
  <div class="wrap">
  <div class="center reveal"><span class="eyebrow" style="background:#fff">The healing process</span><h2 data-split>Start your healing journey in 4 simple steps</h2><p class="lead">From reaching out to rising up — your journey starts here.</p></div>
  <div class="steps" data-steps>{steps_html}</div>
  <div class="expect">
    <div class="reveal"><b>Free first conversation</b><span>No cost, no obligation — just see if it's a fit.</span></div>
    <div class="reveal"><b>In person or virtual</b><span>Lorain &amp; Cuyahoga County, or from home.</span></div>
    <div class="reveal"><b>3–12 month programs</b><span>One-on-one, family, or group workshops.</span></div>
    <div class="reveal"><b>Affordable &amp; flexible</b><span>No insurance needed; bundles and long-term discounts.</span></div>
  </div>
  <p class="center reveal" style="margin-top:36px">{btn("Start your session", "/contact")}</p>
</div>
  {edge("navy", "arch")}
</section>

<section class="section bg-navy edged">{navy_layers()}<div class="wrap">
  <div class="center reveal"><span class="eyebrow light">Holistic support</span><h2 data-split>Holistic, personalized mental wellness support</h2></div>
  <div class="pillars">{pillars_html}</div>
</div>
  {edge("cream", "wave", sprig="l")}
</section>

{consult_section(tone="cream", to="sand", kind="dip")}

{why_section(tone="sand", to=None)}

<section class="journey">
  <div class="scene" data-depth="0.5" aria-hidden="true"></div><div class="veil" aria-hidden="true"></div>
  {edge("sand", "hill", top=True)}
  <div class="wrap"><div class="glass reveal">
    <span class="eyebrow">Your journey starts here</span>
    <h2 data-split>Your path is unique, and I'll walk alongside you every step of the way.</h2>
    {checks(["A safe, supportive space", "Expert guidance, tailored to you", "A community of support"], "checks")}
    {btn("Start your session", "/contact")}
  </div></div>
  {edge("cream", "wave", sprig="r")}
</section>

<section class="section tone-cream edged" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap locations">
  <div class="reveal map-embed" data-map="https://www.google.com/maps?q=Elyria,+OH&amp;z=9&amp;output=embed"><div class="map-gate"><div><svg class="pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg><strong>Lorain &amp; Cuyahoga County, Ohio</strong><p>The interactive map is provided by Google, which may set cookies.</p><button type="button" class="btn small" data-load-map>Show map</button></div></div></div>
  <div><div class="reveal"><span class="eyebrow">Locations</span><h2 data-split>Where I serve</h2></div><div class="loc-list">{locs}</div></div>
</div>
  {edge("sage", "dip", sprig="l")}
</section>

{blog_section(tone="sage", to="mist", kind="hill")}
{faq_section(tone="mist", to="deep", kind="arch")}
"""
    page("/", "Life Coaching & Case Management in Lorain & Cuyahoga | Moments With Mrs. T",
         "Compassionate life coaching, case management & mental wellness programs in Cuyahoga & Lorain County. Personalized support for healing, growth & resilience.",
         body, ld=[LD_BUSINESS, faq_ld(FAQ_SHORT)])

# ---------------------------------------------------------------- ABOUT
def build_about():
    values = [("It's OK to not be OK.", "Every feeling is welcome here. Naming where you are is the first step toward where you want to be."),
              ("Your trauma does not define you.", "What happened to you is part of your story — not the end of it."),
              ("Growth is a journey, not a race.", "Progress looks different for everyone. We move at the pace that's right for you."),
              ("Every moment is a new opportunity to heal.", "Small, steady steps add up to real change."),
              ("You are never alone in your struggle.", "You'll have a partner, a plan, and a community walking with you.")]
    vals = "".join(f'<div class="value card reveal" data-tilt>{img("6826c3e0ec0ad51ce82dfb65")}<h3>{t}</h3><p>{d}</p></div>' for t, d in values)
    body = f"""
{banner("About Moments With Mrs. T", "Compassionate, evidence-based support tailored to each person — in Lorain & Cuyahoga County and online.")}
{meet_tieshia()}
<section class="section tight" data-same style="overflow:hidden"><div class="wrap"><p class="big-quote" data-split>“More ways to inspire, heal, and guide others to a future they deserve. This isn't just a business; it's my purpose.”</p></div></section>
{roots_section()}
<section class="section"><div class="wrap"><div class="vision reveal">
  <div class="motif tr" aria-hidden="true"></div>
  {img("6826713abd083aa53006a2ea", "", cls="v1")}{img("6826713ad95c622675c96b76", "", cls="v2")}
  <span class="eyebrow" style="background:#fff">Our vision</span>
  <p>To create a world where everyone knows they are not alone in their struggles — a community where people embrace their healing journey, find renewed hope, and walk confidently toward a brighter, fuller future.</p>
</div></div></section>
<section class="section" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div><div class="wrap split">
  <div class="video-stack reveal"><div class="frame" data-depth="0.3" aria-hidden="true"></div><div class="video-panel"><video autoplay muted loop playsinline preload="none" poster="/assets/video/family-poster.jpg" aria-hidden="true"><source src="/assets/video/family.mp4" type="video/mp4"></video></div>
    <div class="quote glass" data-depth="-0.3">I don't just guide you — I walk with you.</div></div>
  <div class="reveal">
    <span class="eyebrow">What makes us different</span>
    <h2 data-split>A partner in your transformation</h2>
    <p>Moments With Mrs. T isn't just another coaching service. My approach is uniquely personal, blending professional techniques with the powerful touch of lived experience. I don't just guide you — I walk with you, helping you make sense of life's complexities with compassion and clarity.</p>
    <p>The “special sauce”? The gift of enlightenment and encouragement — lifting clients' spirits daily while offering realistic, actionable strategies for long-term success.</p>
  </div>
</div></section>
<section class="section tone-green" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><img class="ghostmark l" src="/assets/layers/logo-mark-white.webp" alt="" aria-hidden="true" loading="lazy" style="opacity:.07"><div class="wrap">
  <div class="center reveal"><span class="eyebrow">Our values</span><h2 data-split>What I believe</h2><p class="lead">By equipping people with the knowledge and strategies they need, I help them build confidence, resilience, and independence in managing their mental health.</p></div>
  <div class="values">{vals}</div>
  <p class="center" style="margin-top:36px">{btn("Book a free consultation", "/contact")}</p>
</div></section>
{consult_section()}
{blog_section()}
{faq_section()}
"""
    page("/about", "About Tieshia Henry | Moments With Mrs. T Life Coaching",
         "Meet Tieshia Henry, founder of Moments With Mrs. T — a certified life coach and case management professional serving Lorain & Cuyahoga County.",
         body, active="/about", ld=[LD_BUSINESS])

# ---------------------------------------------------------------- SERVICES
def build_services():
    body = f"""
<section class="hero">
  <div class="blob sage b1" data-depth="0.2" aria-hidden="true"></div><div class="blob sky b2" data-depth="0.2" aria-hidden="true"></div>
  <img class="palm" src="/assets/layers/palm-shadow.webp" alt="" aria-hidden="true"><div class="motif bl" aria-hidden="true"></div>
  <div class="wrap hero-grid">
  <div>
    <span class="eyebrow load" style="--d:0">Empowering your mental well-being</span>
    <h1 data-split>Case management &amp; life coaching in Lorain &amp; Cuyahoga, OH</h1>
    <p class="lead load" style="--d:2">One-on-one coaching, family support, and group workshops — in person or virtual. Every plan is built around you.</p>
    <div class="load" style="--d:3">{btn("Let's talk", "/contact")}</div>
  </div>
  {hero_stage("tieshia-cutout-2.webp")}
</div></section>
<section class="section tone-green" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><img class="ghostmark r" src="/assets/layers/logo-mark-white.webp" alt="" aria-hidden="true" loading="lazy" style="opacity:.07"><div class="wrap">
  {leaf_divider()}
  <div class="center reveal" style="margin-bottom:44px"><h2 data-split>Services</h2><p class="lead">Expert guidance, practical tools, and a compassionate community where you can find direction, inspiration, and encouragement.</p></div>
  {service_cards()}
</div></section>
{consult_section()}
{why_section()}
{blog_section()}
{faq_section()}
"""
    page("/services", "Services | Moments With Mrs. T | Lorain & Cuyahoga, OH",
         "Case management, life coaching, family coaching, communication and coping skills workshops in Lorain & Cuyahoga County. Compassionate support for lasting change.",
         body, active="/services", ld=[LD_BUSINESS])

    for s in services:
        others = [o for o in services if o["slug"] != s["slug"]]
        other_links = "".join(f'<li><a href="/services/{o["slug"]}">{o["label"]}</a></li>' for o in others)
        body = f"""
<section class="banner has-photo">{navy_layers()}
  <div class="bphoto" data-depth="0.35" aria-hidden="true">{img(s["photo-service"]["fileId"], "", eager=True)}</div>
  <div class="wrap">
  <div class="crumbs"><a href="/services">Services</a> / {esc(s["label"])}</div>
  <div class="chip" style="position:static;display:inline-flex;margin-bottom:18px">{img(s["main-image"]["fileId"], "", style="width:30px;height:30px")}{esc(s["label"])}</div>
  <h1 data-split>{esc(s["name"])}</h1><p class="lead reveal">{esc(s["short"])}</p>
  <div class="reveal">{btn("Book a free consultation", "#book", "light")}</div>
</div></section>
<section class="section" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap split" style="align-items:start">
  <article class="prose reveal">{clean_rich(s["post-body"])}</article>
  <aside class="reveal" style="position:sticky;top:110px;display:grid;gap:20px">
    <div class="loc"><h3>Ready to start?</h3><p style="margin-bottom:12px">Free consultation · In person or virtual</p>{btn("Book now", "#book")}<p style="margin:14px 0 0"><a href="tel:{PHONE_TEL}">{PHONE}</a></p></div>
    <div class="loc"><h3>Other services</h3><ul style="padding-left:1.1em;margin:0">{other_links}</ul></div>
  </aside>
</div></section>
{consult_section()}
{faq_section()}
"""
        ld = [LD_BUSINESS, {"@context": "https://schema.org", "@type": "Service", "name": s["label"], "description": s["meta-description"],
                            "provider": {"@type": "ProfessionalService", "name": "Moments With Mrs. T", "url": SITE_URL},
                            "areaServed": ["Lorain County, OH", "Cuyahoga County, OH"]}]
        page(f"/services/{s['slug']}", s["meta-title"], s["meta-description"], body, active="/services", ld=ld,
             og_image="/assets/img/" + IMGS[s["photo-service"]["fileId"]]["f"])

# ---------------------------------------------------------------- BLOG
def build_blog():
    feats = "".join(f"""<article class="post-feature reveal">
  <a class="pf-img stack" href="/blog/{p["slug"]}" tabindex="-1" aria-hidden="true"><div class="back" data-depth="0.25"></div>{img(p["main-image"]["fileId"], p.get("alt-text") or "", cls="main")}</a>
  <div><span class="eyebrow">{p["mins"]} min read</span><h2><a href="/blog/{p["slug"]}">{esc(p["name"])}</a></h2><p>{esc(p["post-summary"])}</p>{btn("Read now", "/blog/" + p["slug"], "ghost small")}</div>
</article>""" for p in posts)
    body = f"""
{banner("Mrs. T's Chair | Blog", "Real talk on mental wellness, family communication, and coping skills — from a certified life coach in Lorain & Cuyahoga County.")}
<section class="section" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap">{feats}</div></section>
{consult_section()}
{faq_section()}
"""
    page("/blog", "Mental Wellness Tips and Life Coaching Advice | Moments With Mrs. T Blog",
         "Expert insights on mental wellness, family communication, and coping skills. Real healing, real talk from a certified life coach in Cuyahoga & Lorain County.",
         body, active="/blog")

    for p in posts:
        published = p["_published"][:10]
        body = f"""
<section class="section" style="padding-bottom:0"><div class="wrap">
  <div class="article-head reveal">
    <p class="crumbs" style="color:var(--muted)"><a href="/blog" style="color:var(--navy)">← All posts</a></p>
    <span class="eyebrow">Becoming aware is the first step</span>
    <h1>{esc(p["name"])}</h1>
    <p class="lead" style="margin:0 auto 14px">{esc(p["post-summary"])}</p>
    <div class="meta"><span>By {esc(p.get("author-name") or "Tieshia Henry")}</span><span>·</span><span>{p["mins"]} min read</span></div>
  </div>
  {img(p["main-image"]["fileId"], p.get("alt-text") or "", cls="article-hero", eager=True)}
</div></section>
<section class="section" data-same style="padding-top:0"><div class="wrap"><div class="article">
  <article class="prose">{p["body"]}</article>
  <div class="author">{img("68267d6bb4f4b628f1483e75", "Tieshia Henry")}<div><strong>Tieshia Henry</strong>Founder &amp; Certified Life Coach, Moments With Mrs. T</div></div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px"><button class="btn ghost small" type="button" data-copy>Copy link</button><a class="btn ghost small" href="https://www.facebook.com/sharer/sharer.php?u={SITE_URL}/blog/{p['slug']}" target="_blank" rel="noopener">Share on Facebook</a></div>
</div></div></section>
{consult_section()}
{blog_section("Keep reading", exclude=p["slug"])}
"""
        ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["name"], "description": p.get("meta-description") or p["post-summary"],
               "image": SITE_URL + "/assets/img/" + IMGS[p["main-image"]["fileId"]]["f"], "datePublished": published,
               "author": {"@type": "Person", "name": "Tieshia Henry"}, "publisher": {"@type": "Organization", "name": "Moments With Mrs. T"},
               "mainEntityOfPage": f"{SITE_URL}/blog/{p['slug']}"}]
        page(f"/blog/{p['slug']}", p.get("meta-title") or p["name"], p.get("meta-description") or p["post-summary"], body,
             active="/blog", ld=ld, og_image="/assets/img/" + IMGS[p["main-image"]["fileId"]]["f"])

# ---------------------------------------------------------------- FAQ / CONTACT / LEGAL / 404
def build_faq():
    body = f"""
{banner("FAQs about life coaching &amp; mental wellness", "Empathetic, evidence-based support tailored to the needs of each person in Cuyahoga &amp; Lorain County.")}
<section class="section" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><img class="ghostmark l" src="/assets/layers/logo-mark.webp" alt="" aria-hidden="true" loading="lazy"><div class="wrap">{faq_block(FAQ_LONG)}{CRISIS}</div></section>
{meet_tieshia(photo="69094569c7c1946df49788b0", photo_alt="Tieshia Henry seated in front of a mural of golden wings")}
{consult_section()}
{blog_section()}
"""
    page("/faq", "FAQs | Life Coaching & Mental Wellness in Cuyahoga & Lorain | Moments With Mrs. T",
         "Answers about life coaching, case management, insurance, virtual sessions, and ages served at Moments With Mrs. T in Cuyahoga & Lorain County.",
         body, active="/faq", ld=[faq_ld(FAQ_LONG)])

def build_contact():
    body = f"""
{banner("Contact Moments With Mrs. T", "Trusted life coaching and mental wellness support in Cuyahoga &amp; Lorain County. Schedule a free consultation today.", cta=False)}
<section class="section" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div><div class="wrap split">
  {photo_stack("69094569c7c1946df49788b0", "Tieshia Henry seated in front of a mural of golden wings", inset="6909481faeb0fef5f77d5bbd", inset_alt="Tieshia Henry with clients")}
  <div class="reveal">
    <span class="eyebrow">Let's connect</span>
    <h2 data-split>Let's talk. Let's heal. Let's grow.</h2>
    <p class="lead">I'm so glad you're here.</p>
    <p>Whether you're ready to schedule a session, have questions about services, or just need someone to talk to, Moments With Mrs. T is ready to help you take the next step. Making life make sense — one conversation at a time.</p>
    <div class="loc-list" style="margin-top:24px">
      <div class="loc"><h3>Call or text</h3><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
      <div class="loc"><h3>Email</h3><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="loc"><h3>Where</h3><p style="margin:0">In person in Lorain &amp; Cuyahoga County · Virtual sessions anywhere</p></div>
    </div>
  </div>
</div></section>
{consult_section("Schedule your free consultation", "A free, no-obligation consultation to explore your options and see if coaching is a good fit for you.")}
<section class="section tight" data-same><div class="wrap"><div class="vision reveal" style="background:#fff">
  <span class="eyebrow">A helpful local reminder</span>
  <p>Ohio weather can take a toll on mental health — especially in winter and during seasonal transitions. That's why virtual sessions are available too, so you never have to face things alone, rain or shine.</p>
</div></div></section>
{why_section()}
"""
    page("/contact", "Contact Moments With Mrs. T | Life Coaching & Mental Wellness in Cuyahoga",
         "Reach out to Moments With Mrs. T for trusted life coaching and mental wellness support in Cuyahoga & Lorain County. Schedule a free consultation today.",
         body, ld=[LD_BUSINESS])

def build_privacy():
    body = f"""
<section class="banner">{navy_layers()}<div class="wrap"><h1 data-split>Privacy Policy &amp; Terms of Service</h1><p class="lead">How Moments With Mrs. T collects, uses, and protects your information — in plain language.</p></div></section>
<section class="section"><div class="wrap"><div class="article prose">
<p><em>Last updated: {LEGAL_UPDATED}</em></p>
<p>Jump to: <a href="#privacy">Privacy Policy</a> · <a href="#cookies">Cookies &amp; analytics</a> · <a href="#sms">Text messages</a> · <a href="#terms">Terms of Service</a></p>

<h2 id="privacy">Privacy Policy</h2>
<p>This policy explains how <strong>Moments With Mrs. T</strong> (“we,” “us”), a life coaching and case management practice founded by Tieshia Henry and serving Lorain County, Cuyahoga County, and virtual clients, handles information when you visit this website or contact us.</p>

<h3>1. Information you give us</h3>
<p>When you request a consultation or contact us, we collect what you choose to share: your name, phone number, email address, the best time to reach you, the service you're interested in, any message you write, and whether you opted in to appointment text messages.</p>
<p>Please don't include detailed medical or mental-health information in the website form. You can share that privately during your consultation.</p>

<h3>2. Information collected automatically</h3>
<ul>
<li><strong>Hosting logs.</strong> Our hosting provider (Vercel) records basic technical data such as IP address, browser type, and pages requested. This is used to deliver the site, keep it secure, and prevent abuse.</li>
<li><strong>Analytics — only with your permission.</strong> If you choose “Allow analytics,” we use Microsoft Clarity to understand how visitors use the site: pages viewed, time on page, clicks, scrolling, device and browser type, and approximate location. Clarity may create session replays and heatmaps. Form fields are masked and never recorded. If you decline, Clarity does not load. See <a href="#cookies">Cookies &amp; analytics</a>.</li>
</ul>

<h3>3. How we use your information</h3>
<ul>
<li>To respond to your request and schedule, confirm, or reschedule appointments</li>
<li>To send reminders or updates about your sessions</li>
<li>To answer questions you send us</li>
<li>To keep the website secure and, if you allow analytics, to improve it</li>
</ul>
<p>We <strong>do not sell</strong> your personal information, share it for targeted advertising, or use it to send marketing messages.</p>

<h3>4. Who helps us run the site</h3>
<p>We share information only with service providers that help us operate, and only as needed:</p>
<ul>
<li><strong>Vercel</strong> — website hosting and security.</li>
<li><strong>FormSubmit</strong> — delivers your consultation request from the website to our email inbox.</li>
<li><strong>Google</strong> — our email inbox (Gmail). Google Maps loads only if you click “Show map.”</li>
<li><strong>Microsoft Clarity</strong> — website analytics, only if you allow it.</li>
</ul>
<p>We may also disclose information if required by law, or to protect someone's safety in an emergency.</p>

<h3>5. How long we keep it</h3>
<p>We keep consultation requests and contact details only as long as needed to respond and to provide services, and we delete them when you ask (unless we're required to keep them). Clarity keeps analytics data according to Microsoft's retention policy (recordings for about 30 days, aggregated data for up to about 13 months).</p>

<h3>6. How we protect it</h3>
<p>The site is served only over encrypted HTTPS with modern security settings, access to your information is limited to Moments With Mrs. T, and we never sell or rent it. No method of transmission or storage is 100% secure, but we take reasonable steps to protect your information.</p>

<h3>7. Children and teens</h3>
<p>We work with children (4th grade and up), teens, and families, but services for anyone under 18 are arranged by a parent or legal guardian. This website is not directed to children under 13, and we do not knowingly collect personal information online from children under 13. If you believe a child has sent us information through this site, contact us and we'll delete it.</p>

<h3>8. Your choices and rights</h3>
<ul>
<li>Ask to see, correct, or delete the information we have about you.</li>
<li>Stop appointment texts any time by replying STOP, or contact us.</li>
<li>Change your analytics choice any time with the <a href="#cookies" data-privacy-choices>Privacy choices</a> link in the footer.</li>
<li>We honor the Global Privacy Control (GPC) browser signal as a request to opt out of analytics.</li>
</ul>
<p>To make a request, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a>. We'll respond within 30 days.</p>

<h2 id="cookies">Cookies &amp; analytics</h2>
<p>This site uses no advertising cookies. We store your privacy choice in your browser so we don't ask again. If, and only if, you choose “Allow analytics,” Microsoft Clarity sets these first-party cookies:</p>
<ul>
<li><code>_clck</code> — keeps a random Clarity user ID (up to 1 year)</li>
<li><code>_clsk</code> — connects page views into one session (1 day)</li>
</ul>
<p>Microsoft may also use its own cookies when processing Clarity data. Learn more in the <a href="https://privacy.microsoft.com/privacystatement" target="_blank" rel="noopener">Microsoft Privacy Statement</a> and the <a href="https://learn.microsoft.com/clarity/setup-and-installation/cookie-list" target="_blank" rel="noopener">Clarity cookie list</a>.</p>
<p><button type="button" class="btn small ghost" data-privacy-choices>Change my privacy choices</button></p>

<h2 id="sms">Text messages (SMS)</h2>
<p>Texting is optional. If you check the box on our booking form, you agree to receive text messages from Moments With Mrs. T <strong>only</strong> about your appointments (confirmations, reminders, and rescheduling). Consent is not required to book.</p>
<ul>
<li>Message frequency varies. Message and data rates may apply.</li>
<li>Reply <strong>STOP</strong> to opt out at any time, or <strong>HELP</strong> for help.</li>
<li>We do not send promotional or marketing texts.</li>
<li>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Text-messaging opt-in data and consent are never shared with any third party.</li>
</ul>

<h3>Changes to this policy</h3>
<p>If we update this policy, we'll change the “Last updated” date above. Significant changes will be noted on this page.</p>

<h2 id="terms">Terms of Service</h2>
<p>By using this website or scheduling services with Moments With Mrs. T, you agree to these terms.</p>

<h3>1. What we offer</h3>
<p>Moments With Mrs. T provides life coaching, case management, family coaching, and skills workshops. <strong>These services are not therapy, counseling, medical care, or legal advice</strong>, and they are not a substitute for care from a licensed professional. Coaching works best alongside any clinical care you already receive.</p>

<h3>2. Not for emergencies</h3>
<p>This website and our services are not for emergencies. If you or someone else is in crisis or thinking about self-harm, call or text <a href="tel:988">988</a> (Suicide &amp; Crisis Lifeline) or dial 911.</p>

<h3>3. Website content</h3>
<p>Articles and other content on this site are for general information and encouragement. Every person's situation is different, and results from coaching vary.</p>

<h3>4. Booking and communication</h3>
<p>Submitting the website form is a request for a consultation, not a confirmed appointment. We'll contact you by phone, email, or (if you opted in) text to confirm. Program details, fees, payment, and cancellation terms are provided separately before services begin.</p>

<h3>5. Using this site</h3>
<p>Please don't misuse the site: no attempts to disrupt or hack it, send spam or harmful code, or submit false information.</p>

<h3>6. Ownership</h3>
<p>The Moments With Mrs. T name, logo, text, and images on this site belong to Moments With Mrs. T or are used with permission. Please don't copy or reuse them without written permission.</p>

<h3>7. Links to other sites</h3>
<p>We may link to other websites, like Facebook or Google Maps. We're not responsible for their content or privacy practices.</p>

<h3>8. Disclaimers and limitation of liability</h3>
<p>This website is provided “as is.” To the fullest extent allowed by law, Moments With Mrs. T is not liable for indirect or consequential damages arising from your use of the website.</p>

<h3>9. Governing law</h3>
<p>These terms are governed by the laws of the State of Ohio.</p>

<h3>10. Contact</h3>
<p>Questions about these terms or your privacy: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
</div></div></section>
"""
    page("/privacy-policy-terms-and-agreements", "Privacy Policy & Terms | Moments With Mrs. T",
         "How Moments With Mrs. T collects, uses, and protects your information, our cookie and text-message policies, and the terms for using this website.", body)

def build_404():
    body = f"""<section class="section"><div class="wrap center"><span class="eyebrow">Page not found</span><h1>This page took a different path.</h1>
<p class="lead">The page you're looking for doesn't exist or has moved.</p><p>{btn("Back to home", "/")}</p></div></section>"""
    page("/404", "Page not found | Moments With Mrs. T", "The page you're looking for doesn't exist.", body)
    SITEMAP.pop()

# ---------------------------------------------------------------- run
if __name__ == "__main__":
    build_home(); build_about(); build_services(); build_blog(); build_faq(); build_contact(); build_privacy(); build_404()
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in SITEMAP) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(SITEMAP) + 1} pages into {OUT}")
