# Moments With Mrs. T — static site

Rebuild of the Webflow site (Webflow site id `682662003bf94e763652ae1c`) as plain HTML/CSS/JS, ready for Vercel.

- `site/` — the deployable site. Set Vercel's root directory to `site` (no build step). `vercel.json` gives clean URLs and redirects old `/blog-posts/*` links.
- `build.py` — regenerates every page in `site/` from `_source/cms.json` (services + blog posts exported from the Webflow CMS) and the page copy in the script. Run `python build.py` after edits.
- `_source/` — the raw Webflow export (page trees, CMS, asset list) for reference.

Before launch:
1. Set `SITE_URL` in `build.py` to the client's real domain and rebuild (canonical links, sitemap, social cards).
2. Booking forms post to FormSubmit (`site/assets/js/main.js`). The first submission sends an activation email to momentswithmrst@gmail.com; click it once.
3. Point DNS at Vercel.

## Privacy, analytics and security
- Microsoft Clarity: set `CLARITY_ID` in `build.py`, then `python build.py`. Clarity loads only after a visitor clicks "Allow analytics" (opt-in, Consent API v2, GPC honored). Form fields carry `data-clarity-mask`. In the Clarity dashboard, set Masking to **Strict**.
- Security headers + CSP live in `site/vercel.json`. If you change the inline `<script>` in `build.py`, recompute its sha256 hash in the CSP.
- Fonts are self-hosted (`site/assets/fonts`), and the Google map loads only on click.
