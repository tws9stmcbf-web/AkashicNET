"""Read-only Reddit Bridge for AkashicNET community ingestion."""

from .models import RedditPostRecord, RedditSource
from .registry import load_registry

__all__ = ["RedditPostRecord", "RedditSource", "load_registry"]
