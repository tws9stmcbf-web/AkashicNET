from __future__ import annotations

import hashlib
import re
from typing import Optional, Tuple
from urllib.parse import urlparse, urlunparse

REDDIT_HOSTS = {"reddit.com", "www.reddit.com", "old.reddit.com", "new.reddit.com", "m.reddit.com"}
_TRACKING_PREFIXES = ("utm_",)
_TRACKING_KEYS = {"share_id", "rdt", "context"}


def extract_post_id(value: str) -> Optional[str]:
    if not value:
        return None
    match = re.search(r"/comments/([A-Za-z0-9]+)", value)
    return match.group(1) if match else None


def extract_subreddit(value: str) -> Optional[str]:
    parsed = urlparse(value if value.startswith("http") else f"https://{value}")
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) >= 2 and parts[0].lower() == "r":
        return parts[1]
    return None


def normalize_reddit_url(value: str, registry_subreddit: Optional[str] = None) -> str:
    if not value or not value.strip():
        raise ValueError("Reddit URL is required")
    text = value.strip()
    if text.startswith("/"):
        text = "https://www.reddit.com" + text
    if text.startswith("http://"):
        text = "https://" + text[7:]
    if not text.startswith("http"):
        text = "https://" + text
    parsed = urlparse(text)
    host = parsed.netloc.lower()
    if host not in REDDIT_HOSTS:
        raise ValueError(f"Unsupported Reddit host: {parsed.netloc}")
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 4 or parts[0].lower() != "r" or parts[2].lower() != "comments":
        if len(parts) == 2 and parts[0].lower() == "r":
            subreddit = registry_subreddit or parts[1]
            return f"https://www.reddit.com/r/{subreddit}/"
        raise ValueError(f"Not a Reddit post or subreddit URL: {value}")
    subreddit = registry_subreddit or parts[1]
    post_id = parts[3]
    slug = parts[4] if len(parts) > 4 else ""
    path = f"/r/{subreddit}/comments/{post_id}/"
    if slug:
        path += f"{slug}/"
    return urlunparse(("https", "www.reddit.com", path, "", "", ""))


def post_identity(value: str, registry_subreddit: Optional[str] = None) -> Tuple[str, str]:
    canonical = normalize_reddit_url(value, registry_subreddit)
    post_id = extract_post_id(canonical)
    if not post_id:
        raise ValueError(f"Reddit post ID is required: {value}")
    return post_id, canonical


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
