#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ $# -lt 1 ]; then
  echo "Usage: bash scripts/run-backtest.sh <tickers> [extra args...]"
  echo "Example: bash scripts/list-agents.sh"
  echo "Example: bash scripts/run-backtest.sh AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01"
  echo "Example: bash scripts/run-backtest.sh KO,AXP --analysts ben_graham,warren_buffett"
  echo "Example: bash scripts/run-backtest.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only"
  exit 1
fi

TICKERS="$1"
shift || true

cd "$ROOT_DIR"
poetry run python src/backtester.py --ticker "$TICKERS" "$@"
