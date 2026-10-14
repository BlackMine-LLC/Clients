// Depth + motion layer for Moments With Mrs. T.
// Calm by design: slow eases, small distances, nothing loops for attention.
// Everything here is off under prefers-reduced-motion (the page is fully readable without it).

const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
const root = document.documentElement;
const SHOT = /[?&]shot/.test(location.search); // full-page screenshots: show everything

if (reduce) {
  root.classList.add("reduced");
  document.querySelectorAll("video[autoplay]").forEach((v) => { v.removeAttribute("autoplay"); v.pause(); });
} else {
  initReveals();
  initSplitHeadings();
  initParallax();
  if (finePointer) { initPointerDepth(); initTilt(); }
  initCounters();
  initStepsProgress();
}

// ---------- reveals: only elements below the fold start hidden, siblings stagger ----------
function initReveals() {
  const els = [...document.querySelectorAll(".reveal")];
  const vh = innerHeight;
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("in");
      io.unobserve(e.target);
    }
  }, { rootMargin: "0px 0px -10% 0px" });
  els.forEach((el) => {
    const parent = el.parentElement;
    const sibs = [...parent.children].filter((c) => c.classList.contains("reveal"));
    el.style.setProperty("--stagger", `${Math.min(sibs.indexOf(el), 5) * 90}ms`);
    if (SHOT || el.getBoundingClientRect().top < vh * 0.9) { el.classList.add("in"); return; }
    el.classList.add("pre");
    io.observe(el);
  });
}

// ---------- headings rise in word by word ----------
function initSplitHeadings() {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (SHOT || e.isIntersecting) { e.target.classList.add("words-in"); io.unobserve(e.target); }
  }, { rootMargin: "0px 0px -12% 0px" });
  document.querySelectorAll("[data-split]").forEach((h) => {
    let i = 0;
    const wrap = (node) => {
      [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.append(part); return; }
            const outer = document.createElement("span"); outer.className = "w";
            const inner = document.createElement("span"); inner.textContent = part;
            inner.style.setProperty("--i", i++);
            outer.append(inner); frag.append(outer);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && !n.classList.contains("w")) wrap(n);
      });
    };
    h.setAttribute("aria-label", h.textContent.trim().replace(/\s+/g, " "));
    wrap(h);
    h.classList.add("wsplit");
    io.observe(h);
  });
}

// ---------- scroll parallax: [data-depth] layers drift at different speeds ----------
// depth > 0 moves slower than the page (background), depth < 0 faster (foreground).
function initParallax() {
  const layers = [...document.querySelectorAll("[data-depth]")].map((el) => ({
    el, depth: parseFloat(el.dataset.depth), host: el.closest("section, header, .hero, .banner") || el.parentElement, on: false,
  }));
  if (!layers.length) return;
  const vis = new IntersectionObserver((entries) => {
    entries.forEach((e) => layers.filter((l) => l.host === e.target).forEach((l) => (l.on = e.isIntersecting)));
  }, { rootMargin: "20% 0px" });
  new Set(layers.map((l) => l.host)).forEach((h) => vis.observe(h));
  let ticking = false;
  const update = () => {
    ticking = false;
    const vh = innerHeight;
    for (const l of layers) {
      if (!l.on) continue;
      const r = l.host.getBoundingClientRect();
      const progress = (r.top + r.height / 2 - vh / 2) / vh; // 0 when the section is centered
      l.el.style.setProperty("--py", `${(progress * l.depth * 120).toFixed(1)}px`);
    }
  };
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener("resize", update);
  update();
}

// ---------- pointer depth: hero layers lean toward the cursor ----------
function initPointerDepth() {
  document.querySelectorAll("[data-pointer-scene]").forEach((scene) => {
    const layers = [...scene.querySelectorAll("[data-pointer]")];
    let tx = 0, ty = 0, x = 0, y = 0, raf = 0;
    const loop = () => {
      x += (tx - x) * 0.06; y += (ty - y) * 0.06; // soft follow
      layers.forEach((l) => {
        const d = parseFloat(l.dataset.pointer);
        l.style.setProperty("--mx", `${(x * d).toFixed(2)}px`);
        l.style.setProperty("--my", `${(y * d).toFixed(2)}px`);
      });
      raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.05 ? requestAnimationFrame(loop) : 0;
    };
    scene.addEventListener("pointermove", (e) => {
      const r = scene.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width - 0.5) * 2;
      ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
      if (!raf) raf = requestAnimationFrame(loop);
    });
    scene.addEventListener("pointerleave", () => { tx = 0; ty = 0; if (!raf) raf = requestAnimationFrame(loop); });
  });
}

// ---------- cards tilt slightly under the cursor ----------
function initTilt() {
  document.querySelectorAll("[data-tilt]").forEach((card) => {
    card.addEventListener("pointermove", (e) => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
      card.style.setProperty("--rx", `${(-py * 5).toFixed(2)}deg`);
      card.style.setProperty("--ry", `${(px * 6).toFixed(2)}deg`);
      card.style.setProperty("--gx", `${((px + 0.5) * 100).toFixed(0)}%`);
      card.style.setProperty("--gy", `${((py + 0.5) * 100).toFixed(0)}%`);
    });
    card.addEventListener("pointerleave", () => { card.style.setProperty("--rx", "0deg"); card.style.setProperty("--ry", "0deg"); });
  });
}

// ---------- counters ease up once ----------
function initCounters() {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      io.unobserve(e.target);
      const el = e.target, end = parseFloat(el.dataset.count), start = performance.now(), dur = 1400;
      const tick = (t) => {
        const p = Math.min(1, (t - start) / dur), eased = 1 - Math.pow(1 - p, 4);
        el.textContent = Math.round(end * eased);
        if (p < 1) requestAnimationFrame(tick);
      };
      el.textContent = "0";
      requestAnimationFrame(tick);
    }
  }, { threshold: 0.6 });
  document.querySelectorAll("[data-count]").forEach((el) => io.observe(el));
}

// ---------- the healing-steps path fills as you scroll through it ----------
function initStepsProgress() {
  const track = document.querySelector("[data-steps]");
  if (!track) return;
  const steps = [...track.querySelectorAll(".step")];
  let ticking = false;
  const update = () => {
    ticking = false;
    const r = track.getBoundingClientRect(), vh = innerHeight;
    const p = Math.min(1, Math.max(0, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
    track.style.setProperty("--progress", p.toFixed(3));
    steps.forEach((s, i) => s.classList.toggle("lit", p >= (i + 0.35) / steps.length));
  };
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();
}
