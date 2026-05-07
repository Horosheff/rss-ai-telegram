# Инструкции для агентов

## Cursor Cloud — окружение и секреты

Этот репозиторий рассчитан на запуск `python3 -m news_bot` в [Cloud Agents](https://cursor.com/docs/cloud-agent).

### Секреты (обязательно через Dashboard)

В [Cursor Dashboard → Cloud Agents → Secrets](https://cursor.com/dashboard/cloud-agents) задайте **имена переменных как в коде** (они попадут в окружение ВМ):

| Переменная | Назначение |
|------------|------------|
| `TELEGRAM_BOT_TOKEN` | токен бота от [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | числовой id чата или канала, куда слать посты |

Токен и chat id **не коммитьте** в репозиторий. Локально можно использовать копию `env.example` → `.env` (файл `.env` в git не входит).

Опционально: `PIPELINE_DRY_RUN=true` — собрать текст без отправки в Telegram и без записи в БД.

### Установка зависимостей

В корне репозитория задан [`.cursor/environment.json`](.cursor/environment.json): перед работой агента выполняется `pip3 install -r requirements.txt`.

### Проверочный запуск

```bash
python3 -m news_bot
```

В stdout — JSON (`posted`, `all_duplicates`, `missing_telegram`, …). Код выхода `0`, если `ok` в ответе `true`.
