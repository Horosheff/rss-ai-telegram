"""
Точка входа: один прогон конвейера (для cron / планировщика / ручного запуска).
Интервал (например каждые 5 минут) задаётся снаружи: systemd timer, Task Scheduler, GitHub Actions, etc.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from news_bot.agents.orchestrator import Orchestrator


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Telegram news bot: один цикл «поиск → дедуп → HTML → отправка».",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Только JSON-результат, без логов в stderr",
    )
    args = parser.parse_args()

    if not args.quiet:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )

    orch = Orchestrator()
    result = orch.run_once()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
