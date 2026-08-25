# Internship Alert Agent

Scrapes **Internshala**, **Naukri**, and **LinkedIn (public search pages only)**
for AI/ML, IoT, Edge AI, and Computer Vision internships, and emails you when
new ones show up. Runs on a schedule via GitHub Actions — no server needed.

## How it works

```
agent/
  config.py              # keywords, categories, email settings
  filters.py              # keyword relevance matching
  dedup.py                 # tracks which listings you've already been emailed about
  notify.py                # builds and sends the email
  main.py                    # orchestrates: fetch -> filter -> dedup -> email
  sources/
    internshala.py          # public category pages, no login
    naukri.py                # public search pages, no login
    linkedin_public.py        # public "jobs-guest" search endpoint, no login
seen_listings.json         # state file, committed back to the repo each run
.github/workflows/scrape.yml  # runs every 4 hours
```

## Setup

### 1. Push this to a GitHub repo
```bash
cd internship-agent
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<you>/internship-agent.git
git push -u origin main
```

### 2. Set up email sending
Easiest path: a Gmail account with an **App Password** (not your real password —
Google requires 2FA enabled, then generate one at
myaccount.google.com → Security → App passwords).

### 3. Add GitHub Actions secrets
In your repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret | Value |
|---|---|
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | your Gmail address |
| `SMTP_PASS` | the 16-character app password |
| `EMAIL_TO` | where alerts should be sent (can be the same address) |

### 4. Enable Actions and test it
Go to the **Actions** tab → "Internship Alert Agent" → **Run workflow** to trigger
it manually first, instead of waiting 4 hours. Check the run logs to confirm each
source fetched listings.

## Tuning

- Edit `KEYWORDS` in `config.py` to widen/narrow what counts as relevant.
- Edit `INTERNSHALA_CATEGORIES`, `NAUKRI_SEARCH_KEYWORDS`, `LINKEDIN_KEYWORDS`
  to change what's searched per source.
- Change the cron schedule in `.github/workflows/scrape.yml` (currently every 4h).

## Important caveats — read before relying on this

**Site markup changes.** Naukri and Internshala redesign their pages
periodically, and the CSS selectors in `sources/*.py` will break when they do.
If a run's logs show "0 listings" from a source that used to work, open that
site in a browser, view the page source, and update the `soup.select(...)`
line to match the new markup.

**Naukri may render client-side.** If `sources/naukri.py` consistently returns
nothing even though naukri.com clearly has listings for your query, it likely
means the results are loaded via JavaScript rather than present in the raw
HTML. The fix at that point is swapping `requests` for a headless browser
(Playwright), which is a bigger change — happy to help build that if it comes
to that, but it also costs more in CI minutes.

**LinkedIn is intentionally limited to public, unauthenticated search
results** — the same guest endpoint LinkedIn serves to logged-out visitors
and search-engine crawlers. This deliberately avoids logging in, using
cookies/sessions, or working around any bot-detection wall. The tradeoff is
fewer results and less detail than the logged-in Jobs UI, and LinkedIn may
still rate-limit or block the IP the requests come from (GitHub Actions
runners share IP ranges other people have used for scraping). If that
happens consistently, the more sustainable path is LinkedIn's own **Job
Alert emails** (set one up in the LinkedIn UI) forwarded into a parsing
rule, rather than pushing harder on the scraper — I'd rather flag that now
than have this quietly turn into something that fights LinkedIn's
anti-bot systems.

**Respect rate limits.** The `DELAY_BETWEEN_REQUESTS_SEC` setting in
`config.py` adds a pause between requests. Don't remove it or drop the
schedule below a few hours — hammering these sites is how you get an IP
or account blocked.

## Running locally (for testing/debugging selectors)
```bash
pip install -r requirements.txt
export SMTP_USER=... SMTP_PASS=... EMAIL_TO=...
python -m agent.main
```
