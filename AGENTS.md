# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python 3.12 RSS-to-Telegram bot (`news_bot`). It fetches AI/ML news from hardcoded RSS feeds, deduplicates via SQLite, formats into Telegram HTML, and posts one article per run.

### Running the bot

```bash
python3 -m news_bot
```

The command `python` is not available — always use `python3`.

### Dry-run mode (no Telegram credentials needed)

Set `PIPELINE_DRY_RUN=true` in `.env` (copy from `env.example`). This skips Telegram send and DB writes, but still fetches RSS and formats the post. Useful for testing pipeline logic without secrets.

### Required secrets for live mode

- `TELEGRAM_BOT_TOKEN` — from @BotFather
- `TELEGRAM_CHAT_ID` — numeric chat/channel ID

### No lint/test tooling

This repository has no configured linting (no ruff, flake8, mypy) or test framework (no pytest). Verification is done via:
- `python3 -m py_compile <file>` for syntax checking
- `python3 -m news_bot` in dry-run mode for end-to-end validation

### Data directory

The SQLite DB is stored at `data/posted_news.sqlite3` by default (configured via `DATABASE_PATH` env var). The `data/` directory is created automatically on first run.
