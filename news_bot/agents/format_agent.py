"""
Суб-агент «оформление»: пост в Telegram HTML без внешних моделей.
См. https://core.telegram.org/bots/api#html-style
"""

from __future__ import annotations

from html import escape, unescape
from typing import Any


class FormatAgent:
    def to_telegram_html(
        self,
        item: Any,
        *,
        reference_time_utc: str,
    ) -> str:
        title = self._clean_text(getattr(item, "title", ""))
        summary = self._clean_text(getattr(item, "summary", ""))
        url = str(getattr(item, "url", "") or "").strip()
        pub = self._clean_text(getattr(item, "published_hint", "") or "")

        summary = summary[:2000]
        lines: list[str] = [
            f"<b>{escape(title)}</b>",
            "",
            escape(summary) if summary else escape("—"),
        ]

        if pub:
            lines.extend(["", f"<i>{escape(f'Опубликовано: {pub}')}</i>"])

        if url.startswith(("http://", "https://")):
            lines.extend(
                ["", f'<a href="{escape(url, quote=True)}">Источник</a>']
            )
        elif url:
            lines.extend(["", escape(url)])

        text = "\n".join(lines).strip()
        return self._enforce_length(text, limit=3900)

    @staticmethod
    def _clean_text(value: Any) -> str:
        return " ".join(unescape(str(value or "")).strip().split())

    @staticmethod
    def _enforce_length(text: str, *, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 1].rstrip() + "…"
