// Form submissions go to FormSubmit (free, no backend). The first submission sends an
// activation email to the inbox below; click it once and every later booking request arrives there.
const FORM_ENDPOINT = "https://formsubmit.co/ajax/momentwithmrst@gmail.com";

// Mobile menu
const nav = document.getElementById("nav");
const scrim = document.querySelector(".scrim");
const toggles = document.querySelectorAll("[data-menu]");
function setMenu(open) {
  nav.classList.toggle("open", open);
  scrim.classList.toggle("show", open);
  document.querySelector(".menu-toggle").setAttribute("aria-expanded", String(open));
  document.body.style.overflow = open ? "hidden" : "";
}
toggles.forEach((b) => b.addEventListener("click", () => setMenu(!nav.classList.contains("open"))));
scrim?.addEventListener("click", () => setMenu(false));
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

// Booking forms
document.querySelectorAll("form.form").forEach((form) => {
  const status = form.querySelector(".form-status");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (form.querySelector(".hp input").value) return;
    const btn = form.querySelector("button[type=submit]");
    const label = btn.textContent;
    btn.disabled = true; btn.textContent = "Sending…";
    status.className = "form-status";
    const data = Object.fromEntries(new FormData(form));
    delete data._honey;
    data._subject = "New consultation request — Moments With Mrs. T";
    data._template = "table";
    data.Page = location.pathname;
    try {
      const res = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      status.textContent = "Thank you! Mrs. T will reach out within 1–2 business days.";
      status.classList.add("ok");
    } catch {
      status.innerHTML = 'Something went wrong sending your request. Please call <a href="tel:+13302491042">(330) 249-1042</a> or email <a href="mailto:momentwithmrst@gmail.com">momentwithmrst@gmail.com</a>.';
      status.classList.add("err");
    } finally {
      btn.disabled = false; btn.textContent = label;
    }
  });
});

// Copy link (blog posts)
document.querySelectorAll("[data-copy]").forEach((b) => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(location.href); b.textContent = "Link copied"; } catch { b.textContent = location.href; }
}));

document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

// Google map loads only when the visitor asks for it
document.querySelectorAll("[data-load-map]").forEach((btn) => btn.addEventListener("click", () => {
  const box = btn.closest("[data-map]");
  const f = document.createElement("iframe");
  f.title = "Map of Lorain and Cuyahoga County, Ohio";
  f.src = box.dataset.map;
  f.referrerPolicy = "no-referrer-when-downgrade";
  box.replaceChildren(f);
}));
