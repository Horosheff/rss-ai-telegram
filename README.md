# RSS → Telegram (нейросети / ИИ)

Минимальный пайплайн без внешних «сетевых моделей» и без ключей к LLM: только **Telegram Bot API**, **встроенные RSS-ленты** в коде и **SQLite** для дедупликации.

Подходит для запуска в [**Cursor Cloud Agents**](https://cursor.com/docs/cloud-agent): секреты (`TELEGRAM_BOT_TOKEN`, при необходимости `TELEGRAM_CHAT_ID`) задаются в [Dashboard → Cloud Agents → Secrets](https://cursor.com/dashboard/cloud-agents), репозиторий — на GitHub/GitLab.

## Что внутри

1. `ResearchAgent` — читает фиксированный список RSS из [`news_bot/config.py`](news_bot/config.py) (`RSS_FEEDS`), сортирует записи по дате.
2. `FormatAgent` — собирает пост в **Telegram HTML** через `html.escape` ([документы Bot API](https://core.telegram.org/bots/api#html-style)).
3. `posted_news` (SQLite) — не публикуем повтор по URL / отпечатку заголовка.
4. Один «цикл» = одна новая публикация за запуск (если есть непубликованный кандидат).

Картинок нет; превью ссылок в Telegram отключено.

## Переменные окружения

Скопируйте `env.example` → `.env`:

| Переменная | Нужна? |
|------------|--------|
| `TELEGRAM_BOT_TOKEN` | Да (токен у [@BotFather](https://t.me/BotFather)) |
| `TELEGRAM_CHAT_ID` | Да для отправки в **конкретный** чат/канал (узнать: [@userinfobot](https://t.me/userinfobot), `getUpdates`, боты с id) |
| `PIPELINE_DRY_RUN` | `true` = только собрать текст, без отправки и без записи в БД |
| `DATABASE_PATH` | По умолчанию `data/posted_news.sqlite3` |

Отдельных переменных для RSS нет — список лент меняется в коде (`RSS_FEEDS`).

## Установка и один запуск

```bash
pip install -r requirements.txt
python -m news_bot
```

В stdout — JSON со статусом (`posted`, `all_duplicates`, `no_candidates`, `missing_telegram`, …).

## Расписание и Cloud Agent

Интервал и триггеры (например, периодический запуск) задаются в [**Cursor Cloud Agents**](https://cursor.com/docs/cloud-agent) или вашем CI — не в этом репозитории.

В Dashboard добавьте Secrets `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`; команда запуска, например: `pip install -r requirements.txt && python -m news_bot`. Репозиторий подключите к Cursor с GitHub.

Токен бота **не храните** в коде; `chat_id` — идентификатор чата/канала в Bot API для `sendMessage`.
