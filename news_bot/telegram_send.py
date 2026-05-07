"""Отправка сообщения в Telegram Bot API (HTML)."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from news_bot import config

logger = logging.getLogger(__name__)


def send_html_message(text: str) -> dict[str, Any]:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        raise RuntimeError(
            "Задайте TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID в окружении (.env)."
        )

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    with httpx.Client(timeout=40.0) as client:
        r = client.post(url, json=payload)
        try:
            data = r.json()
        except Exception:
            data = {"raw": r.text}

        if r.status_code >= 400 or not data.get("ok", False):
            logger.error(
                "Telegram sendMessage failed: %s %s",
                r.status_code,
                data,
            )
            raise RuntimeError(f"Telegram API error: {data}")

        logger.info("Telegram message sent, message_id=%s", data.get("result", {}).get("message_id"))
        return data
