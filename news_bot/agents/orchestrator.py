"""
Главный оркестратор: вызывает ResearchAgent → проверка БД → FormatAgent → Telegram.
Один успешный пост за запуск (первый ещё не публикованный кандидат).
"""

from __future__ import annotations

import logging
from typing import Any

from news_bot import config
from news_bot.config import DATABASE_PATH
from news_bot.db import build_db
from news_bot.agents.format_agent import FormatAgent
from news_bot.agents.research_agent import ResearchAgent
from news_bot.agents.translation_agent import TranslationAgent
from news_bot import telegram_send

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self) -> None:
        self.research = ResearchAgent()
        self.translator = TranslationAgent()
        self.formatter = FormatAgent()
        self._db = build_db(DATABASE_PATH)

    def run_once(self) -> dict[str, Any]:
        ref = self.research.current_reference_iso()

        if not config.PIPELINE_DRY_RUN and not config.telegram_ready():
            return {
                "ok": False,
                "action": "missing_telegram",
                "ref": ref,
                "hint": "Задайте TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID или PIPELINE_DRY_RUN=1",
            }

        candidates = self.research.fetch()

        if not candidates:
            return {"ok": True, "action": "no_candidates", "ref": ref}

        for item in candidates:
            if self._db.exists(item.url, item.title):
                logger.debug("Skip duplicate: %s", item.url[:80])
                continue

            try:
                publish_item = self.translator.translate_item(item) if config.TRANSLATE_TO_RUSSIAN else item
            except Exception as e:
                logger.exception("Translation failed: %s", e)
                return {
                    "ok": False,
                    "action": "translation_failed",
                    "error": str(e),
                    "candidate": item.as_dict(),
                    "ref": ref,
                }

            html = self.formatter.to_telegram_html(
                publish_item,
                reference_time_utc=ref,
            )

            if config.PIPELINE_DRY_RUN:
                logger.info("DRY_RUN: не отправляем в Telegram, БД не пишем.")
                return {
                    "ok": True,
                    "action": "dry_run",
                    "item": publish_item.as_dict(),
                    "html_preview": html[:900],
                    "ref": ref,
                }

            try:
                telegram_send.send_html_message(html)
            except Exception as e:
                logger.exception("Send failed: %s", e)
                return {
                    "ok": False,
                    "action": "send_failed",
                    "error": str(e),
                    "candidate": item.as_dict(),
                    "ref": ref,
                }

            self._db.record(
                item.url,
                publish_item.title,
                source=item.source,
            )
            return {
                "ok": True,
                "action": "posted",
                "item": publish_item.as_dict(),
                "ref": ref,
            }

        return {
            "ok": True,
            "action": "all_duplicates",
            "checked": len(candidates),
            "ref": ref,
        }


__all__ = ["Orchestrator"]
