from . import config


def is_relevant(listing):
    """Case-insensitive substring match against title (+ company as light signal)."""
    haystack = (listing.get("title", "") + " " + listing.get("company", "")).lower()
    return any(kw.lower() in haystack for kw in config.KEYWORDS)


def filter_relevant(listings):
    return [l for l in listings if is_relevant(l)]
