# The Tax Team — Funnel Landing Page

A static landing page (single `index.html` + `assets/`). No build step, no framework — it deploys as-is to Vercel, Netlify, GitHub Pages, or any static host.

## Structure

```
taxteam-funnel-site/
├── index.html        # the page
├── assets/           # all images (referenced as assets/…)
├── vercel.json       # static-host config
└── README.md
```

All image paths in `index.html` are relative (`assets/…`), so images load correctly wherever the folder is deployed — this is what makes it publish cleanly instead of as one broken single file.

## Two assets to add before launch

These two files live in the Claude design project but were too large to pull automatically. Download them from the design project's `uploads/` folder and drop them into `assets/` with these exact names:

- `assets/hero-team.jpg` — the wide hero team photo
- `assets/walkthrough.mp4` — the walkthrough video

The page is built to degrade gracefully: until you add them, the hero shows a branded gradient panel and the video section hides itself. Once the files are in `assets/`, they appear automatically — no code change needed.

## Run locally

Any static server works, e.g.:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy to Vercel

This repo is a static site, so Vercel needs no framework preset:

1. Push this folder to a GitHub repo.
2. In Vercel → **Add New → Project** → import the repo.
3. Framework preset: **Other**. Build command: none. Output directory: `.` (root).
4. Deploy.

Every push to the default branch redeploys automatically.

## Notes / before-launch checklist

- Testimonials in the "Proof" section are **placeholders** — replace with real, permissioned client quotes.
- The "5.0★ Google rating" stat is marked **(verify)** — confirm before publishing.
- The booking form is a live GoHighLevel embed (`brand.gotaxteam.com`) and works as-is.
- Celebrity/athlete photos load from the live gotaxteam.com CDN (external URLs).
