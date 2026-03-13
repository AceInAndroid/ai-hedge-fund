#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${HOME}/.agents/skills/ai-hedge-fund"

bash "$ROOT_DIR/scripts/package-openclaw-skill.sh"

mkdir -p "${HOME}/.agents/skills"
rm -rf "$TARGET_DIR"
cp -R "$ROOT_DIR/dist/openclaw-skill/ai-hedge-fund" "$TARGET_DIR"

echo "Installed OpenClaw skill to $TARGET_DIR"
