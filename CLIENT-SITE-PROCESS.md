# Client site process (every site, every time)

GitHub is the source of truth. Vercel only ever deploys from this repo. Nothing lives only on one computer.

## Where things live
| What | Where |
|---|---|
| Source of truth | `github.com/BlackMine-LLC/Clients`, one folder per client (e.g. `Moments With Mrs T/`) |
| Local copy | Clone `Clients` on each machine. PC: `C:\Users\Latre\BlackMine-Clients`. Mac/Lindon: record yours in `blackmine-studio/machine/devices.md` |
| Hosting | Vercel team `info-21296780s-projects`, one project per site, **Root Directory = the client folder** (+ subfolder if the site is in one) |
| Domains/DNS | Registrar (usually Namecheap). Note where DNS is actually managed (Namecheap vs Cloudflare) in the client README |

## Every client folder contains
- `README.md`: what the site is, how to build it, Vercel project name, domain, DNS host, analytics IDs, open items
- The deployable site (e.g. `site/`) and any build script
- Source material (`_source/`: original exports, raw images) so the site can be rebuilt without the old platform
- No secrets. API keys and tokens go in Vercel environment variables, never in git (this repo is public)

## Workflow
1. `git pull` in `Clients` before touching anything.
2. Work in the client folder. Preview locally.
3. Commit with a plain one-line message and push. Never force-push. On a merge conflict, stop and ask.
4. Vercel deploys automatically from `main` (production) and from branches/PRs (previews). Don't deploy from a laptop with `vercel --prod`.
5. Update HQ.

## New site checklist
1. Create the client folder with a README (copy the headings from `Moments With Mrs T/README.md`).
2. Commit + push.
3. Vercel: Add New → Project → Import `BlackMine-LLC/Clients` → Root Directory = client folder → Framework "Other", no build command for static sites. Or with the CLI from the client folder: `vercel link` then `vercel git connect`.
4. Check the preview URL.
5. Add the domain in Vercel → set DNS at whoever hosts it (A `@` → `76.76.21.21`, CNAME `www` → `cname.vercel-dns.com`). Keep existing MX/TXT email records.
6. Privacy and legal pass: privacy policy + terms, consent banner before any analytics (Microsoft Clarity), security headers in `vercel.json`.
7. Record domain, DNS host, Vercel project, and Clarity ID in the client README.
