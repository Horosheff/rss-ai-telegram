"""
Суб-агент «оформление»: пост в Telegram HTML без внешних моделей (только html.escape).
См. https://core.telegram.org/bots/api#html-style
"""

from __future__ import annotations

from html import escape
from typing import Any


class FormatAgent:
    def to_telegram_html(
        self,
        item: Any,
        *,
        reference_time_utc: str,
    ) -> str:
        title = str(getattr(item, "title", "") or "").strip()
        summary = str(getattr(item, "summary", "") or "").strip()
        url = str(getattr(item, "url", "") or "").strip()
        pub = getattr(item, "published_hint", None)

        summary = " ".join(summary.split())[:2000]
        lines: list[str] = [
            f"<b>{escape(title)}</b>",
            "",
            escape(summary) if summary else escape("—"),
            "",
        ]

        meta = f"UTC: {reference_time_utc}"
        if pub:
            meta = f"{meta} · {pub}"
        lines.append(f"<i>{escape(meta)}</i>")

        if url.startswith(("http://", "https://")):
            lines.extend(
                ["", f'<a href="{escape(url, quote=True)}">Источник</a>']
            )
        elif url:
            lines.extend(["", escape(url)])

        text = "\n".join(lines).strip()
        return self._enforce_length(text, limit=3900)

    @staticmethod
    def _enforce_length(text: str, *, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 1].rstrip() + "…"
