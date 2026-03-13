#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT_DIR"
poetry run uvicorn app.backend.main:app --reload --host 127.0.0.1 --port 8000
