from .sources.internshala import fetch_internshala_listings
from .sources.naukri import fetch_naukri_listings
from .sources.linkedin_public import fetch_linkedin_listings
from .filters import filter_relevant
from .dedup import load_seen_ids, save_seen_ids, split_new
from .notify import send_email


def run():
    all_listings = []

    for fetch_fn, name in [
        (fetch_internshala_listings, "Internshala"),
        (fetch_naukri_listings, "Naukri"),
        (fetch_linkedin_listings, "LinkedIn"),
    ]:
        try:
            listings = fetch_fn()
            print(f"[{name}] fetched {len(listings)} listings")
            all_listings.extend(listings)
        except Exception as e:
            print(f"[{name}] fetch failed entirely: {e}")

    relevant = filter_relevant(all_listings)
    print(f"{len(relevant)} relevant after keyword filtering")

    seen_ids = load_seen_ids()
    new_listings, updated_ids = split_new(relevant, seen_ids)
    print(f"{len(new_listings)} are new since last run")

    send_email(new_listings)
    save_seen_ids(updated_ids)


if __name__ == "__main__":
    run()
