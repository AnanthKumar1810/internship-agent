"""
Internshala scraper — public category listing pages, no login required.
URL pattern: https://internshala.com/internships/<category-slug>
"""

import time
import requests
from bs4 import BeautifulSoup

from .. import config


def fetch_internshala_listings():
    """Returns a list of dicts: {id, title, company, link, location, source}"""
    results = []
    headers = {"User-Agent": config.USER_AGENT}

    for category in config.INTERNSHALA_CATEGORIES:
        url = f"https://internshala.com/internships/{category}"
        try:
            resp = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[internshala] failed to fetch {url}: {e}")
            time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        # Internshala list items — selector may need updating if their markup changes.
        cards = soup.select("div.individual_internship")

        for card in cards:
            try:
                title_el = card.select_one("h3.job-internship-name a, a.job-title-href")
                company_el = card.select_one("p.company-name, div.company_and_premium a")
                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                link = title_el.get("href", "")
                if link and link.startswith("/"):
                    link = "https://internshala.com" + link

                listing_id = card.get("internshipid") or link
                results.append({
                    "id": f"internshala:{listing_id}",
                    "title": title,
                    "company": company_el.get_text(strip=True) if company_el else "",
                    "link": link,
                    "location": category.replace("-internship", "").replace("-", " "),
                    "source": "Internshala",
                })
            except Exception as e:
                print(f"[internshala] parse error: {e}")
                continue

        time.sleep(config.DELAY_BETWEEN_REQUESTS_SEC)

    return results
