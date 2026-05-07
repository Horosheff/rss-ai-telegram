# Agent instructions

- When the user asks to run the bot (for example: `запусти`), run the production command `./scripts/run_once.sh`.
- Do not set `PIPELINE_DRY_RUN=true` unless the user explicitly asks for a dry run or preview.
- The bot has a default Telegram chat id in `news_bot/config.py`; `TELEGRAM_BOT_TOKEN` still comes from the environment or Cursor Cloud Secrets.
- `./scripts/run_once.sh` persists dedupe state in `state/posted_news.tsv`; keep that file tracked and let the script commit/push it after successful posts.
