#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT_DIR"
python -m compileall src app/backend

cd "$ROOT_DIR/app/frontend"
npm run build

echo "Validation complete"
