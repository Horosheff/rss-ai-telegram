#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

branch="$(git branch --show-current)"
if [[ -n "$branch" ]] && git rev-parse --verify "origin/$branch" >/dev/null 2>&1; then
  git pull --ff-only origin "$branch"
fi

python3 -m news_bot -q

if [[ -n "$(git status --porcelain -- state/posted_news.tsv)" ]]; then
  git add state/posted_news.tsv
  git commit -m "Update posted news state"
  if [[ -n "$branch" ]]; then
    git push -u origin "$branch"
  fi
fi
