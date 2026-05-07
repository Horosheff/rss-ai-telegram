import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _b(name: str, default: str = "") -> bool:
    v = os.getenv(name, default).lower().strip()
    return v in ("1", "true", "yes", "on")


def _p(name: str, default: str) -> Path:
    return Path(os.getenv(name, default)).expanduser().resolve()


DEFAULT_TELEGRAM_CHAT_ID = "449374770"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = (os.getenv("TELEGRAM_CHAT_ID") or DEFAULT_TELEGRAM_CHAT_ID).strip()

PIPELINE_DRY_RUN = _b("PIPELINE_DRY_RUN", "false")
TRANSLATE_TO_RUSSIAN = _b("TRANSLATE_TO_RUSSIAN", "true")

DATABASE_PATH = _p("DATABASE_PATH", "data/posted_news.sqlite3")
POSTED_NEWS_STATE_PATH = _p("POSTED_NEWS_STATE_PATH", "state/posted_news.tsv")

# Встроенные RSS: ИИ / нейросети / ML (без переменных окружения)
RSS_FEEDS: list[str] = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.artificialintelligence-news.com/feed/",
    "https://spectrum.ieee.org/rss/fulltext",
    "https://www.wired.com/feed/tag/ai/latest/rss",
]


def telegram_ready() -> bool:
    return bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
