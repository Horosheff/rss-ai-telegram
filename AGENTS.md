# AGENTS.md

## Cursor Cloud specific instructions

### Overview
RSS-to-Telegram news bot (Python 3.12). Fetches AI/ML news from 7 hardcoded RSS feeds, deduplicates via SQLite, formats to Telegram HTML, and sends one article per run. See `README.md` for full details (in Russian).

### Running the bot
```bash
python3 -m news_bot          # one-shot pipeline run
```
- Use `PIPELINE_DRY_RUN=true` in `.env` to skip Telegram delivery and DB writes — useful for testing without credentials.
- The command is `python3`, not `python` (no `python` alias in this environment).
- Output is JSON to stdout; logs go to stderr.

### Environment variables
Copy `env.example` → `.env`. Key vars: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `PIPELINE_DRY_RUN`, `DATABASE_PATH`. See `env.example` for defaults.

### Testing
No test framework or test files exist in this repo. Validate changes by:
1. `python3 -m py_compile <module>` for syntax checks on changed files.
2. `python3 -m news_bot` with `PIPELINE_DRY_RUN=true` for end-to-end validation.

### Linting
No linter configuration exists (no pyproject.toml, ruff, flake8, pylint). Basic compile checks (`py_compile`) are the available static check.

### Database
SQLite at `data/posted_news.sqlite3` (auto-created on first run). The `data/` directory is gitignored.
