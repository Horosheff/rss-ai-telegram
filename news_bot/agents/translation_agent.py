"""Перевод новости на русский перед публикацией."""

from __future__ import annotations

from html import unescape
import logging

import httpx

from news_bot.agents.research_agent import NewsItem

logger = logging.getLogger(__name__)


class TranslationAgent:
    _URL = "https://translate.googleapis.com/translate_a/single"

    def translate_item(self, item: NewsItem) -> NewsItem:
        title = self.translate_text(item.title)
        summary = self.translate_text(item.summary) if item.summary else ""
        return NewsItem(
            title=title,
            url=item.url,
            summary=summary,
            source=item.source,
            published_hint=item.published_hint,
            sort_ts=item.sort_ts,
        )

    def translate_text(self, text: str) -> str:
        cleaned = self._clean_text(text)
        if not cleaned:
            return ""

        with httpx.Client(timeout=20.0) as client:
            response = client.get(
                self._URL,
                params={
                    "client": "gtx",
                    "sl": "auto",
                    "tl": "ru",
                    "dt": "t",
                    "q": cleaned,
                },
            )
            response.raise_for_status()
            data = response.json()

        translated = "".join(
            chunk[0]
            for chunk in data[0]
            if isinstance(chunk, list) and chunk and chunk[0]
        )
        translated = self._clean_text(translated)
        if not translated:
            raise RuntimeError("Translation API returned empty text")
        logger.debug("Translated text from %s to %s chars", len(cleaned), len(translated))
        return translated

    @staticmethod
    def _clean_text(text: str) -> str:
        return " ".join(unescape(str(text or "")).strip().split())


__all__ = ["TranslationAgent"]
