import json
import os
from . import config


def load_seen_ids():
    if not os.path.exists(config.STATE_FILE):
        return set()
    try:
        with open(config.STATE_FILE, "r") as f:
            return set(json.load(f))
    except (json.JSONDecodeError, IOError):
        return set()


def save_seen_ids(ids):
    with open(config.STATE_FILE, "w") as f:
        json.dump(sorted(ids), f, indent=2)


def split_new(listings, seen_ids):
    """Returns (new_listings, updated_seen_ids)."""
    new_listings = [l for l in listings if l["id"] not in seen_ids]
    updated = set(seen_ids) | {l["id"] for l in listings}
    return new_listings, updated
