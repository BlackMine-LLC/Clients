# Moments With Mrs. T

Life coaching and case management site for Tieshia Henry (Lorain & Cuyahoga County, OH). Rebuilt in October 2026 as static HTML from the unpaid Webflow site (Webflow site id `682662003bf94e763652ae1c`, unpublished Sept 2026). Follow `../CLIENT-SITE-PROCESS.md`.

| Item | Value |
|---|---|
| Domain | `mrstschair.com` (Namecheap, account AdminBlackMine, expires Nov 4, 2027). Canonical: `https://mrstschair.com`, `www` redirects to it |
| DNS host | **Cloudflare** (nameservers `perla` / `oswald.ns.cloudflare.com`), not Namecheap. Keep the Namecheap email-forwarding MX records (`eforward*.registrar-servers.com`) |
| Vercel project | `moments-with-mrs-t` (`prj_Lyoh0zVsEwo62raA9nRp7qJZ7wnw`), connected to `BlackMine-LLC/Clients`, Root Directory `Moments With Mrs T/site`, Framework "Other", no build command. Pushes to `main` deploy to production |
| Live (Vercel URL) | https://moments-with-mrs-t.vercel.app |
| Analytics | Microsoft Clarity project `yxqjh4jbps` (set in `CLARITY_ID` in `build.py`; empty = off) |
| Forms | FormSubmit → `momentswithmrst@gmail.com` (first submission sends a one-time activation email) |

## DNS cutover (Cloudflare → DNS records for mrstschair.com)
Both domains are already added and verified on the Vercel project. In Cloudflare, set these records to **DNS only** (grey cloud, not proxied):
| Type | Name | Value | Replaces |
|---|---|---|---|
| A | `@` | `216.150.1.1` | A `@` → `198.202.211.1` (Webflow) |
| A | `@` | `216.150.16.1` | |
| CNAME | `www` | `cfca04aacd306ae2.vercel-dns-016.com` | CNAME `www` → `cdn.webflow.com` |

Leave the MX (`eforward1-5.registrar-servers.com`) and any SPF TXT records alone so the email forwarding keeps working.

## Layout
- `site/`: the deployable site (20 pages). Don't hand-edit HTML; it's generated.
- `build.py`: generates every page from `_source/cms.json` (services + blog) and the copy in the script. Run `python build.py` after any change.
- `site/assets/css/styles.css` (base) + `depth.css` (layers, color rhythm, section edges, motion).
- `site/assets/js/main.js` (menu, forms, map), `motion.js` (reveals, parallax), `consent.js` (privacy banner + Clarity).
- `site/vercel.json`: clean URLs, redirects from old Webflow URLs, security headers + CSP, caching.
- `_source/`: Webflow export (page trees, CMS, asset list), full-size original photos (`originals/`), and helper scripts.

## Preview locally
```
npx serve site -l 4321
```
Add `?shot` to a URL to show every reveal at once (for full-page screenshots).

## Privacy, analytics and security
- Clarity loads only after a visitor clicks "Allow analytics" (opt-in, Consent API v2). The Global Privacy Control signal counts as decline. The footer has a "Privacy choices" link. Form fields carry `data-clarity-mask`. In the Clarity dashboard, set Masking to **Strict**.
- The privacy policy, cookies section, SMS policy and Terms are at `/privacy-policy-terms-and-agreements`. Update `LEGAL_UPDATED` in `build.py` when they change.
- The CSP in `site/vercel.json` pins a sha256 hash for the one inline `<script>`. If that script in `build.py` changes, recompute the hash.
- Fonts are self-hosted. The Google map loads only on click.

## Open items
- Confirm the business email: the site uses `momentswithmrst@gmail.com` (from the live Webflow site), but Tieshia's onboarding form says `Momentwithmrst@gmail.com`.
- Cloudflare DNS cutover (see above). Needs a Cloudflare login.
- Testimonials (2–3, first name + city) and a real photo of "the chair" would strengthen the site.
