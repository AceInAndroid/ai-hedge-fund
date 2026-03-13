#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT_DIR"

poetry install

cd "$ROOT_DIR/app/frontend"
npm install

cd "$ROOT_DIR"
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created $ROOT_DIR/.env from .env.example"
else
  echo "$ROOT_DIR/.env already exists"
fi

echo "Setup complete"
