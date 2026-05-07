#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 -m news_bot -q
