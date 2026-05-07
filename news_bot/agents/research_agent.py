"""
Суб-агент «источник»: только RSS по встроенному списку лент (нейросети / ИИ).
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import feedparser

from news_bot import config

logger = logging.getLogger(__name__)


@dataclass
class NewsItem:
    title: str
    url: str
    summary: str
    source: str
    published_hint: str | None = None
    sort_ts: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "source": self.source,
            "published_hint": self.published_hint,
        }


class ResearchAgent:
    def current_reference_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def fetch(self, *, max_per_feed: int = 15) -> list[NewsItem]:
        items: list[NewsItem] = []
        for feed_url in config.RSS_FEEDS:
            try:
                parsed = feedparser.parse(feed_url)
            except Exception as e:
                logger.warning("RSS parse failed %s: %s", feed_url, e)
                continue
            for e in parsed.entries[:max_per_feed]:
                title = (getattr(e, "title", None) or "").strip()
                link = (getattr(e, "link", None) or "").strip()
                summary = (getattr(e, "summary", None) or getattr(e, "description", None) or "")
                summary = self._strip_html(summary)[:2000]
                pub = getattr(e, "published", None) or getattr(e, "updated", None)
                pp = getattr(e, "published_parsed", None) or getattr(e, "updated_parsed", None)
                sort_ts = 0.0
                if pp:
                    try:
                        sort_ts = time.mktime(pp)
                    except (OverflowError, OSError, ValueError):
                        sort_ts = 0.0
                if title and link:
                    items.append(
                        NewsItem(
                            title=title,
                            url=link,
                            summary=summary,
                            source=f"rss:{feed_url}",
                            published_hint=str(pub) if pub else None,
                            sort_ts=sort_ts,
                        )
                    )

        # Сначала более свежие записи
        items.sort(key=lambda x: x.sort_ts, reverse=True)

        seen: set[str] = set()
        deduped: list[NewsItem] = []
        for it in items:
            key = (it.url or "").strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            deduped.append(it)

        logger.info("ResearchAgent: collected %s candidates from RSS", len(deduped))
        return deduped

    @staticmethod
    def _strip_html(s: str) -> str:
        return re.sub(r"<[^>]+>", " ", s)
