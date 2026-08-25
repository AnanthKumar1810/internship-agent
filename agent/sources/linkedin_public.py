"""
LinkedIn — PUBLIC job search results only. No login, no cookies, no
session reuse, no bypassing any wall. This hits the same guest endpoint
LinkedIn uses to render public "Jobs" search results for logged-out users
and unauthenticated crawlers (e.g. Google). If LinkedIn returns a login
wall or CAPTCHA for a request, back off — do not try to work around it.

Because this is unauthenticated, expect fewer/less detailed results than
the logged-in Jobs UI. That's the deliberate tradeoff for staying inside
LinkedIn's public-access boundary.
"""

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from .. import config


def fetch_linkedin_listings():
    results = []
    headers = {"User-Agent": config.USER_AGENT}

    for keyword in config.LINKEDIN_KEYWORDS:
        params_url = (
            "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            f"?keywords={quote(keyword)}&location={quote(config.LINKEDIN_LOCATION)}"
            "&f_E=1"  # entry level / internship-ish filter
        )
        try:
            resp = requests.get(params_url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            if resp.status_code != 200:
                print(f"[linkedin] non-200 ({resp.status_code}) for '{keyword}' — skipping")
                time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)
                continue
        except requests.RequestException as e:
            print(f"[linkedin] failed to fetch for '{keyword}': {e}")
            time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("li")

        for card in cards:
            try:
                title_el = card.select_one("h3.base-search-card__title")
                company_el = card.select_one("h4.base-search-card__subtitle")
                link_el = card.select_one("a.base-card__full-link")
                loc_el = card.select_one("span.job-search-card__location")
                if not title_el or not link_el:
                    continue

                link = link_el.get("href", "").split("?")[0]
                results.append({
                    "id": f"linkedin:{link}",
                    "title": title_el.get_text(strip=True),
                    "company": company_el.get_text(strip=True) if company_el else "",
                    "link": link,
                    "location": loc_el.get_text(strip=True) if loc_el else "",
                    "source": "LinkedIn",
                })
            except Exception as e:
                print(f"[linkedin] parse error: {e}")
                continue

        time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)

    return results
