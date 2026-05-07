# AGENTS.md

## Cursor Cloud specific instructions

This is a minimal Python RSS-to-Telegram news bot. See `README.md` for full docs (in Russian).

### Running the application

- **Dry run** (no Telegram credentials needed): `PIPELINE_DRY_RUN=true python3 -m news_bot`
- **Live run** (requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`): `python3 -m news_bot`
- Use `python3` (not `python`) — the VM does not alias `python` to `python3`.
- Each invocation publishes at most one new article and exits. There is no long-running server.

### Key caveats

- No linter, test framework, or build step is configured in this repo. Validation is done by running the bot in dry-run mode.
- The SQLite database is auto-created at `data/posted_news.sqlite3` (configurable via `DATABASE_PATH`). The `data/` directory is gitignored.
- RSS feeds are hardcoded in `news_bot/config.py` (`RSS_FEEDS` list) — there are no env vars for feed URLs.
- Output is a JSON object to stdout with `"ok": true/false` and an `"action"` field describing what happened.
