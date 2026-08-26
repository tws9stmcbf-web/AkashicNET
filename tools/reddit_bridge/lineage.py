from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .canonicalize import extract_post_id, normalize_reddit_url


def _parent_id(parent: Dict[str, Any]) -> Optional[str]:
    return parent.get("id") or extract_post_id(parent.get("permalink") or parent.get("url") or "")


def extract_crosspost_lineage(payload: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], List[str], str]:
    parents = payload.get("crosspost_parent_list") or []
    if not parents:
        parent = payload.get("crosspost_parent")
        if isinstance(parent, str) and "_" in parent:
            post_id = parent.split("_", 1)[1]
            return post_id, post_id, [post_id], "official_crosspost_parent"
        return None, None, [], "none"

    chain = [pid for pid in (_parent_id(item) for item in parents) if pid]
    parent_id = chain[0] if chain else None
    root_id = chain[-1] if chain else parent_id
    return parent_id, root_id, chain, "official_crosspost"


def canonical_parent_url(parent: Dict[str, Any]) -> Optional[str]:
    permalink = parent.get("permalink")
    subreddit = parent.get("subreddit")
    if not permalink:
        return None
    try:
        return normalize_reddit_url(permalink, subreddit)
    except ValueError:
        return None
