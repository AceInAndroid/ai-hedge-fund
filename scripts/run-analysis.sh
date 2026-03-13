#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ $# -lt 1 ]; then
  echo "Usage: bash scripts/run-analysis.sh <tickers> [extra args...]"
  echo "Example: bash scripts/run-analysis.sh AAPL,MSFT,NVDA"
  echo "Example: bash scripts/run-analysis.sh 600519.SH,000001.SZ --analysts-all"
  echo "Example: bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only"
  exit 1
fi

TICKERS="$1"
shift || true

cd "$ROOT_DIR"
poetry run python src/main.py --ticker "$TICKERS" "$@"
