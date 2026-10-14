// Analytics consent for Moments With Mrs. T.
// Microsoft Clarity only loads after a visitor chooses "Allow analytics".
// - Nothing is tracked by default (opt-in).
// - A browser Global Privacy Control signal is treated as "decline".
// - Visitors can change their choice any time from "Privacy choices" in the footer.
// Set the Clarity project ID below (Clarity dashboard → Settings → Setup). Empty = analytics off.
const CLARITY_ID = document.documentElement.dataset.clarity || "";
const KEY = "mrst-privacy-choice"; // stores { analytics: "granted" | "denied", at: ISO date }

const read = () => { try { return JSON.parse(localStorage.getItem(KEY)); } catch { return null; } };
const write = (analytics) => { try { localStorage.setItem(KEY, JSON.stringify({ analytics, at: new Date().toISOString() })); } catch {} };

function loadClarity() {
  if (!CLARITY_ID || window.clarity) return;
  (function (c, l, a, r, i, t, y) {
    c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
    t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
    y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
  })(window, document, "clarity", "script", CLARITY_ID);
  // Clarity Consent API v2: analytics cookies allowed, no ad storage ever.
  window.clarity("consentv2", { ad_Storage: "denied", analytics_Storage: "granted" });
}

function clearClarity() {
  if (window.clarity) window.clarity("consentv2", { ad_Storage: "denied", analytics_Storage: "denied" });
  ["_clck", "_clsk", "CLID", "ANONCHK", "MR", "MUID", "SM"].forEach((n) => {
    document.cookie = `${n}=; Max-Age=0; path=/`;
    document.cookie = `${n}=; Max-Age=0; path=/; domain=.${location.hostname.replace(/^www\./, "")}`;
  });
}

function banner() {
  if (document.getElementById("privacy-banner")) return;
  const el = document.createElement("div");
  el.id = "privacy-banner";
  el.setAttribute("role", "dialog");
  el.setAttribute("aria-live", "polite");
  el.setAttribute("aria-label", "Privacy choices");
  el.innerHTML = `
    <p><strong>Your privacy matters here.</strong> With your permission, we use Microsoft Clarity to see how visitors use this site (pages viewed, clicks, scrolling) so we can make it easier to use. Form fields are never recorded, and we never sell your data. <a href="/privacy-policy-terms-and-agreements#cookies">Learn more</a></p>
    <div class="pb-actions">
      <button type="button" class="btn small ghost" data-choice="denied">Decline</button>
      <button type="button" class="btn small" data-choice="granted">Allow analytics</button>
    </div>`;
  document.body.append(el);
  requestAnimationFrame(() => el.classList.add("show"));
  el.addEventListener("click", (e) => {
    const b = e.target.closest("[data-choice]");
    if (!b) return;
    const choice = b.dataset.choice;
    const prev = read()?.analytics;
    write(choice);
    el.classList.remove("show");
    setTimeout(() => el.remove(), 400);
    if (choice === "granted") loadClarity();
    else { clearClarity(); if (prev === "granted") location.reload(); }
  });
}

const gpc = navigator.globalPrivacyControl === true;
const saved = read();
if (gpc && !saved) write("denied");
const choice = read()?.analytics;
if (choice === "granted" && !gpc) loadClarity();
else if (!choice && CLARITY_ID) banner();

// Footer "Privacy choices" link reopens the banner.
document.addEventListener("click", (e) => {
  if (e.target.closest("[data-privacy-choices]")) { e.preventDefault(); banner(); }
});
