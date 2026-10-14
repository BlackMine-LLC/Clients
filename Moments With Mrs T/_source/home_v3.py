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

<section class="feelings tone-cream edged" style="position:relative" aria-label="From how you feel to where you're headed">
  <h2 class="reveal">Wherever you are right now, there's a way forward.</h2>
  {marquee_rows()}
  {edge("sage", "wave", sprig="r")}
</section>

<section class="section who tone-sage edged" style="overflow:hidden;padding-top:clamp(40px,5vw,70px)">
  <div class="blob mint" style="width:620px;height:620px;left:-220px;top:-80px" data-depth="0.5" aria-hidden="true"></div>
  <div class="blob sky" style="width:460px;height:460px;right:-160px;bottom:10%" data-depth="0.35" aria-hidden="true"></div>
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
  <div class="blob" style="width:640px;height:640px;right:-220px;top:-160px;background:#3f8a7b;opacity:.45" data-depth="0.5" aria-hidden="true"></div>
  <img class="ghostmark l" src="/assets/layers/logo-mark-white.webp" alt="" aria-hidden="true" loading="lazy" data-depth="0.4" style="opacity:.07">
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
    <div class="quote glass" data-depth="-0.6">Reshape what's been cracked. Mold new strength where there once was pain.</div>
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
  <div class="blob sky" style="width:520px;height:520px;right:-180px;top:-60px" data-depth="0.5" aria-hidden="true"></div>
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
  <div class="reveal map-embed"><iframe title="Map of Lorain and Cuyahoga County, Ohio" src="https://www.google.com/maps?q=Elyria,+OH&z=9&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
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
