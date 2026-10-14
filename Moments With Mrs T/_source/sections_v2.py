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
            f'<img class="ghost {ghost}" src="/assets/layers/logo-mark-white.webp" alt="" aria-hidden="true" loading="lazy" data-depth="0.35">')

def horizon(to="var(--cream)"):
    return f"""<div class="horizon" style="--to:{to}" aria-hidden="true">
  <svg class="back" viewBox="0 0 1440 120" preserveAspectRatio="none"><path d="M0 70C160 30 300 20 470 46s300 62 480 40 330-70 490-48V120H0Z"/></svg>
  <svg viewBox="0 0 1440 120" preserveAspectRatio="none"><path d="M0 92c180-34 360-40 540-14s340 40 520 14 300-46 380-40V120H0Z"/></svg>
</div>"""

def consult_section(title="Take the first step toward improving your mental well-being today.",
                    text="Whether you're looking for a personalized game plan, group support, or a wellness program, Tieshia is here to guide you.",
                    eyebrow="Book a free consultation", section_cls="section", form_id="book"):
    return f"""<section class="{section_cls}" id="{form_id}"><div class="wrap"><div class="consult reveal">
  {navy_layers("l")}
  <div>
    <span class="eyebrow light">{eyebrow}</span>
    <h2 data-split>{title}</h2>
    <p>{text}</p>
    <ul><li>Get tailored advice based on where you are right now.</li><li>Talk through your specific needs and build a personalized plan.</li><li>Confidential, compassionate support — no judgment.</li></ul>
    <div class="direct"><span>Prefer to talk now?</span><a href="tel:{PHONE_TEL}">Call {PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
  {booking_form(form_id)}
</div></div></section>"""

def booking_form(fid):
    svc_opts = "".join(f"<option>{s['label']}</option>" for s in services)
    return f"""<form class="form" novalidate aria-label="Book a consultation">
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
    <span class="consent">By submitting, you agree to receive appointment-related calls, texts, or emails only. See the <a href="/privacy-policy-terms-and-agreements">Privacy Policy</a>.</span>
    <button class="btn" type="submit">Request my consultation</button>
    <div class="form-status" role="status" aria-live="polite"></div>
  </form>"""

__DATA_WHY__

def why_section(bg="bg-mint"):
    items = "".join(f'<div class="why-item reveal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg><h3>{t}</h3><p>{d}</p></div>' for t, d, p in WHY)
    words = ["Wholeness", "Mindfulness", "Freedom", "Balance", "Compassion", "Empowerment", "Integrity", "Collaboration"]
    row = "".join(f"<li><b>{w}</b></li>" for w in words)
    return f"""<section class="section {bg}" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div>
  <div class="wrap">
  <div class="center reveal"><span class="eyebrow">The moments matter</span><h2 data-split>Why choose Moments With Mrs. T?</h2></div>
  <div class="why" style="margin-top:36px">{items}</div>
  </div>
  <div class="marquee" style="margin-top:44px" aria-hidden="true"><ul>{row}</ul><ul>{row}</ul></div>
</section>"""

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

def blog_section(title="Discover valuable resources", exclude=None):
    items = [p for p in posts if p["slug"] != exclude][:3]
    return f"""<section class="section"><div class="motif tr" aria-hidden="true"></div><div class="wrap">
  <div class="reveal" style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:36px">
    <div><span class="eyebrow">Mrs. T's Chair — the blog</span><h2 style="margin:0" data-split>{title}</h2></div>
    {btn("All articles", "/blog", "ghost small")}
  </div>
  {post_cards(items)}
</div></section>"""

__DATA_FAQ__

CRISIS = f"""<div class="crisis reveal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10Z"/></svg><p style="margin:0"><strong>In crisis or thinking about harming yourself?</strong> Coaching isn't emergency care. Call or text <a href="tel:988">988</a> (Suicide &amp; Crisis Lifeline) any time, or dial 911.</p></div>"""

def faq_block(items, open_first=True):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"{" open" if (i == 0 and open_first) else ""}><summary>{esc(q)}</summary><div>{a if a.startswith("<") else f"<p>{a}</p>"}</div></details>' for i, (q, a) in enumerate(items)) + "</div>"
def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}

def faq_section(bg="bg-mint"):
    return f"""<section class="section {bg}" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div>
  <img class="ghost r" src="/assets/layers/logo-mark.webp" alt="" aria-hidden="true" loading="lazy" data-depth="0.35">
  <div class="wrap">
  <div class="center reveal" style="margin-bottom:36px"><span class="eyebrow">FAQs</span><h2 data-split>Questions I hear often</h2><p class="lead">Here to answer your worries and put your mind at ease.</p></div>
  {faq_block(FAQ_SHORT)}
  {CRISIS}
  <p class="center" style="margin-top:28px"><a href="/faq">See all FAQs →</a></p>
</div></section>"""

def banner(h1, lead, crumbs=None, cta=True, cta_href="/contact", cta_label="Let's talk"):
    cr = f'<div class="crumbs">{crumbs}</div>' if crumbs else ""
    return f"""<section class="banner">{navy_layers()}<div class="motif tr light" aria-hidden="true"></div><div class="wrap">{cr}
  <h1 data-split>{h1}</h1><p class="lead reveal">{lead}</p>
  <div class="reveal">{checks(["From pain to purpose", "Tailored to your journey", "Real healing, real talk"])}</div>
  {f'<div class="reveal">{btn(cta_label, cta_href, "light")}</div>' if cta else ""}
</div></section>{horizon()}"""

def photo_stack(main, alt, inset=None, inset_alt="", ratio="4/5", badge=""):
    ins = img(inset, inset_alt, cls="inset") if inset else ""
    return f"""<div class="stack reveal">
    <div class="back" data-depth="0.25" aria-hidden="true"></div>
    {img(main, alt, cls="main", style=f"aspect-ratio:{ratio}")}
    {ins}
    {layer_img("/assets/img/6826713a4d81fd6d0725b0f7.webp", "leafy tl", depth=-0.5)}
    {layer_img("/assets/img/6826713ad95c622675c96b76.webp", "leafy br", depth=-0.8)}
    {badge}
  </div>"""

def meet_tieshia():
    badge = '<div class="chip badge"><span class="dot"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z"/></svg></span>Certified Life Coach</div>'
    return f"""<section class="section" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div><div class="wrap split">
  {photo_stack("69094569c7c1946df49788b0", "Tieshia Henry, founder of Moments With Mrs. T, seated in front of golden wings", inset="68269cecaa5f55bde312e14a", inset_alt="Tieshia with family and friends", badge=badge)}
  <div class="reveal">
    <span class="eyebrow">Meet your coach</span>
    <h2 data-split>Meet Tieshia Henry</h2>
    <p style="font-weight:600;color:var(--navy)">Founder &amp; Certified Life Coach · Passionate | Empathetic | Purpose-driven</p>
    <p>Tieshia brings a rare blend of professional expertise and real-world understanding to every coaching session. With a natural gift for encouraging others and a heart fueled by service, she's committed to helping clients feel empowered, validated, and hopeful — every step of the way.</p>
    {btn("Book a consultation", "/contact")}
  </div>
</div></section>"""

def roots_section():
    return f"""<section class="section bg-mint" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap split reverse">
  {photo_stack("68269cecaa5f55bde312e14a", "Tieshia Henry with family and friends", inset="690947824620ec722b9268f7", inset_alt="Tieshia with clients", ratio="4/3")}
  <div class="reveal">
    <span class="eyebrow">Our story</span>
    <h2 data-split>The roots of Moments With Mrs. T</h2>
    <p class="lead">The seeds were planted in 2019, when Tieshia recognized a deeper calling — a desire to help others move beyond pain, uncertainty, and past trauma.</p>
    <p>Officially launched in 2023 after extensive coursework and Life Coach certification, Moments With Mrs. T is the culmination of personal experience, professional training, and an unwavering passion for people.</p>
    {btn("Book a consultation", "/contact")}
  </div>
</div></section>"""

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
  <div class="blob sage b1" data-depth="0.6" aria-hidden="true"></div><div class="blob sky b2" data-depth="0.4" aria-hidden="true"></div><div class="blob sand b3" data-depth="0.3" aria-hidden="true"></div>
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

<section class="feelings" aria-label="From how you feel to where you're headed">
  <h2 class="reveal">Wherever you are right now, there's a way forward.</h2>
  {marquee_rows()}
</section>

<section class="section who" style="overflow:hidden;padding-top:clamp(40px,5vw,70px)">
  <div class="scene bokeh" data-depth="0.5" aria-hidden="true"></div><div class="veil" aria-hidden="true"></div>
  <div class="wrap">
  <div class="center reveal" style="margin-bottom:36px"><span class="eyebrow">Is this right for you?</span><h2 data-split>Who this is for</h2></div>
  <div class="fit">
    <div class="fit-card glass reveal"><h3>This is for you if you're…</h3><ul><li>An overwhelmed parent needing support</li><li>A teen struggling with communication or identity</li><li>A woman navigating trauma, stress, or life transitions</li><li>A family needing guidance and emotional tools</li></ul></div>
    <div class="fit-card not glass reveal"><h3>This isn't the right fit if you're…</h3><ul><li>Unwilling to engage in the healing process</li><li>Seeking crisis clinical therapy (call or text <a href="tel:988">988</a> any time)</li><li>Looking for quick fixes without personal work</li></ul></div>
  </div>
  <div class="center reveal" style="margin-top:56px"><span class="eyebrow">Not sure where to start?</span><h2 data-split>Where are you right now?</h2></div>
  <div class="picker">{picks_html}</div>
</div></section>

<section class="chair-scene chair">
  <div class="scene" data-depth="0.45" aria-hidden="true"></div><div class="veil" aria-hidden="true"></div>
  <div class="wrap">
  {leaf_divider()}
  <div class="chair-panel glass reveal">
    <h2><span class="light-sweep">Mrs. T's Chair</span></h2>
    <p><em>Mrs. T's Chair</em> isn't just a name — it's a symbol of <strong>stillness</strong>, <strong>safety</strong>, and <strong>support</strong>. It's where the overwhelmed parent finally exhales. It's where the teen who's been misunderstood finds their voice. It's where organizations send those they care about most — because they know they'll be met with <strong>warmth</strong>, <strong>wisdom</strong>, and <strong>real help</strong>.</p>
    <p><strong>This chair represents a moment to pause and breathe</strong> — without judgment, without pressure. Just guidance, healing, and the kind of care that transforms lives. Whether you're navigating trauma, managing stress, or supporting someone who is, <em>Mrs. T's Chair</em> is where the healing begins.</p>
    {btn("Come sit with Mrs. T", "/contact")}
  </div>
</div></section>

<section class="section" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap split">
  {photo_stack("68269cecaa5f55bde312e14a", "Tieshia Henry with family and friends", inset="69094569c7c1946df49788b0", inset_alt="Tieshia Henry", ratio="4/3")}
  <div class="reveal">
    <span class="eyebrow">About</span>
    <h2 data-split>About Moments With Mrs. T</h2>
    <p class="lead">Healing and moving forward should be a supported, empowering journey.</p>
    <p>I'm Tieshia Henry, a certified life coach with a heart for service. I founded Moments With Mrs. T in 2023 to offer wraparound services that help you acknowledge, process, and triumph over life's challenges.</p>
    <p>My approach blends case management, coping strategies, and personalized care, so you never have to walk the path alone. I'm proudly based in Lorain County and serve the surrounding Cuyahoga areas with dedication and compassion.</p>
    {btn("More about Mrs. T", "/about", "ghost")}
  </div>
</div></section>

<section class="section bg-mist" style="overflow:hidden">
  <div class="blob mint" style="width:600px;height:600px;right:-200px;top:-100px" data-depth="0.5" aria-hidden="true"></div>
  <img class="ghost l" src="/assets/layers/logo-mark.webp" alt="" aria-hidden="true" loading="lazy" data-depth="0.4">
  <div class="wrap">
  <div class="center reveal" style="margin-bottom:44px"><span class="eyebrow">How I can help</span><h2 data-split>Explore the core services</h2><p class="lead">Coaching and wellness services tailored to help you heal, grow, and thrive — at your own pace and in your own way.</p></div>
  {service_cards()}
</div></section>

<section class="section" style="overflow:hidden"><div class="wrap split">
  <div class="video-stack reveal">
    <div class="frame" data-depth="0.3" aria-hidden="true"></div>
    <div class="video-panel"><video autoplay muted loop playsinline preload="none" poster="/assets/video/pottery-poster.jpg" aria-hidden="true"><source src="/assets/video/pottery.mp4" type="video/mp4"></video><div class="caption">Molding broken pieces into purposeful wholeness</div></div>
    <div class="quote glass" data-depth="-0.6">Reshape what's been cracked. Mold new strength where there once was pain.</div>
  </div>
  <div class="reveal">
    <span class="eyebrow">My approach</span>
    <h2 data-split>Mental health conversations should be open</h2>
    <p class="lead">My approach is gentle, intentional, and rooted in restoration.</p>
    <p>I help you reshape what's been cracked, smooth what's been rough, and mold new strength where there once was pain.</p>
    {btn("Come sit with Mrs. T", "/contact")}
  </div>
</div></section>

<section class="section bg-mint" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div><div class="wrap">
  <div class="center reveal"><span class="eyebrow">The healing process</span><h2 data-split>Start your healing journey in 4 simple steps</h2><p class="lead">From reaching out to rising up — your journey starts here.</p></div>
  <div class="steps" data-steps>{steps_html}</div>
  <div class="expect">
    <div class="reveal"><b>Free first conversation</b><span>No cost, no obligation — just see if it's a fit.</span></div>
    <div class="reveal"><b>In person or virtual</b><span>Lorain &amp; Cuyahoga County, or from home.</span></div>
    <div class="reveal"><b>3–12 month programs</b><span>One-on-one, family, or group workshops.</span></div>
    <div class="reveal"><b>Affordable &amp; flexible</b><span>No insurance needed; bundles and long-term discounts.</span></div>
  </div>
  <p class="center reveal" style="margin-top:36px">{btn("Start your session", "/contact")}</p>
</div></section>

<section class="section bg-navy">{navy_layers()}<div class="wrap">
  <div class="center reveal"><span class="eyebrow light">Holistic support</span><h2 data-split>Holistic, personalized mental wellness support</h2></div>
  <div class="pillars">{pillars_html}</div>
</div></section>
{horizon()}

{consult_section()}

{why_section()}

<section class="journey">
  <div class="scene" data-depth="0.5" aria-hidden="true"></div><div class="veil" aria-hidden="true"></div>
  <div class="wrap"><div class="glass reveal">
    <span class="eyebrow">Your journey starts here</span>
    <h2 data-split>Your path is unique, and I'll walk alongside you every step of the way.</h2>
    {checks(["A safe, supportive space", "Expert guidance, tailored to you", "A community of support"], "checks")}
    {btn("Start your session", "/contact")}
  </div></div>
</section>

<section class="section" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap locations">
  <div class="reveal map-embed"><iframe title="Map of Lorain and Cuyahoga County, Ohio" src="https://www.google.com/maps?q=Elyria,+OH&z=9&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  <div><div class="reveal"><span class="eyebrow">Locations</span><h2 data-split>Where I serve</h2></div><div class="loc-list">{locs}</div></div>
</div></section>

{blog_section()}
{faq_section()}
"""
    page("/", "Life Coaching & Case Management in Lorain & Cuyahoga | Moments With Mrs. T",
         "Compassionate life coaching, case management & mental wellness programs in Cuyahoga & Lorain County. Personalized support for healing, growth & resilience.",
         body, ld=[LD_BUSINESS, faq_ld(FAQ_SHORT)])

