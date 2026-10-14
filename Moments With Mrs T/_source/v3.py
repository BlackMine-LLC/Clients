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
        extra += f'<img class="sprig {sprig}" src="/assets/img/{sid}.webp" alt="" loading="lazy" data-depth="-0.4">'
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
                    eyebrow="Book a free consultation", tone="cream", to=None, kind="wave", form_id="book"):
    e = edge(to, kind, sprig="l") if to else ""
    return f"""<section class="section tone-{tone}{" edged" if to else ""}" id="{form_id}"><div class="wrap"><div class="consult reveal">
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

def why_section(tone="sand", to=None, kind="hill"):
    items = "".join(f'<div class="why-item reveal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg><h3>{t}</h3><p>{d}</p></div>' for t, d, p in WHY)
    words = ["Wholeness", "Mindfulness", "Freedom", "Balance", "Compassion", "Empowerment", "Integrity", "Collaboration"]
    row = "".join(f"<li><b>{w}</b></li>" for w in words)
    e = edge(to, kind, sprig="r") if to else ""
    return f"""<section class="section tone-{tone}{" edged" if to else ""}" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div>
  <div class="blob sage" style="width:480px;height:480px;left:-160px;top:10%" data-depth="0.5" aria-hidden="true"></div>
  <div class="wrap">
  <div class="center reveal"><span class="eyebrow">The moments matter</span><h2 data-split>Why choose Moments With Mrs. T?</h2></div>
  <div class="why" style="margin-top:36px">{items}</div>
  </div>
  <div class="marquee" style="margin-top:44px" aria-hidden="true"><ul>{row}</ul><ul>{row}</ul></div>
{e}</section>"""

def blog_section(title="Discover valuable resources", exclude=None, tone="sage", to=None, kind="wave"):
    items = [p for p in posts if p["slug"] != exclude][:3]
    e = edge(to, kind, sprig="l") if to else ""
    return f"""<section class="section tone-{tone}{" edged" if to else ""}" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap">
  <div class="reveal" style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:36px">
    <div><span class="eyebrow" style="background:#fff">Mrs. T's Chair — the blog</span><h2 style="margin:0" data-split>{title}</h2></div>
    {btn("All articles", "/blog", "ghost small")}
  </div>
  {post_cards(items)}
</div>{e}</section>"""

def faq_section(tone="mist", to="deep", kind="arch"):
    e = edge(to, kind) if to else ""
    return f"""<section class="section tone-{tone}{" edged" if to else ""}" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div>
  <img class="ghostmark r" src="/assets/layers/logo-mark.webp" alt="" aria-hidden="true" loading="lazy" data-depth="0.35">
  <div class="wrap">
  <div class="center reveal" style="margin-bottom:36px"><span class="eyebrow" style="background:#fff">FAQs</span><h2 data-split>Questions I hear often</h2><p class="lead">Here to answer your worries and put your mind at ease.</p></div>
  {faq_block(FAQ_SHORT)}
  {CRISIS}
  <p class="center" style="margin-top:28px"><a href="/faq">See all FAQs →</a></p>
</div>{e}</section>"""

def meet_tieshia(tone="cream", to=None, kind="hill"):
    badge = '<div class="chip badge"><span class="dot"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z"/></svg></span>Certified Life Coach</div>'
    e = edge(to, kind, sprig="r") if to else ""
    return f"""<section class="section tone-{tone}{" edged" if to else ""}" style="overflow:hidden"><div class="motif bl" aria-hidden="true"></div><div class="wrap split">
  {photo_stack("69bf2ac5b74b01ad68f9dafa", "Tieshia Henry, founder of Moments With Mrs. T and certified life coach", badge=badge)}
  <div class="reveal">
    <span class="eyebrow">Meet your coach</span>
    <h2 data-split>Meet Tieshia Henry</h2>
    <p style="font-weight:600;color:var(--navy)">Founder &amp; Certified Life Coach · Passionate | Empathetic | Purpose-driven</p>
    <p>Tieshia brings a rare blend of professional expertise and real-world understanding to every coaching session. With a natural gift for encouraging others and a heart fueled by service, she's committed to helping clients feel empowered, validated, and hopeful — every step of the way.</p>
    {btn("Book a consultation", "/contact")}
  </div>
</div>{e}</section>"""

def roots_section(tone="sage", to=None, kind="wave"):
    e = edge(to, kind, sprig="l") if to else ""
    return f"""<section class="section tone-{tone}{" edged" if to else ""}" style="overflow:hidden"><div class="motif tr" aria-hidden="true"></div><div class="wrap split reverse">
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
  <div class="blob sand" style="width:560px;height:560px;right:-180px;top:-120px;opacity:.9" data-depth="0.5" aria-hidden="true"></div>
  <div class="blob mint" style="width:420px;height:420px;left:-140px;bottom:0" data-depth="0.4" aria-hidden="true"></div>
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
    return f"""<section class="banner edged" style="padding-bottom:calc(clamp(56px,8vw,100px) + var(--edge-h))">{navy_layers()}<div class="motif tr light" aria-hidden="true"></div><div class="wrap">{cr}
  <h1 data-split>{h1}</h1><p class="lead reveal">{lead}</p>
  <div class="reveal">{checks(["From pain to purpose", "Tailored to your journey", "Real healing, real talk"])}</div>
  {f'<div class="reveal">{btn(cta_label, cta_href, "light")}</div>' if cta else ""}
</div>{edge(to, "wave", sprig="r")}</section>"""
