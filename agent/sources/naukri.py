"""
Naukri scraper — public search result pages, no login required.
Naukri's markup and API shape change fairly often; if selectors stop
matching, inspect the page source and update the CSS selectors below.
"""

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from .. import config


def fetch_naukri_listings():
    results = []
    headers = {"User-Agent": config.USER_AGENT}

    query = quote(config.NAUKRI_SEARCH_KEYWORDS + " internship")
    url = f"https://www.naukri.com/{query.replace('%20', '-')}-jobs"

    try:
        resp = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[naukri] failed to fetch {url}: {e}")
        return results

    soup = BeautifulSoup(resp.text, "html.parser")
    # Naukri renders listings client-side in many cases; this selector targets
    # the server-rendered job cards where available. If results come back empty,
    # Naukri may require a headless browser (Playwright) for this query — see README.
    cards = soup.select("div.cust-job-tuple, article.jobTuple")

    for card in cards:
        try:
            title_el = card.select_one("a.title, a.title.ellipsis")
            company_el = card.select_one("a.comp-name, span.comp-name")
            loc_el = card.select_one("span.locWdth, span.ellipsis.locWdth")
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            link = title_el.get("href", "")
            listing_id = link

            results.append({
                "id": f"naukri:{listing_id}",
                "title": title,
                "company": company_el.get_text(strip=True) if company_el else "",
                "link": link,
                "location": loc_el.get_text(strip=True) if loc_el else "",
                "source": "Naukri",
            })
        except Exception as e:
            print(f"[naukri] parse error: {e}")
            continue

    time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)
    return results
