#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PACKAGE_ROOT="$ROOT_DIR/dist/openclaw-skill/ai-hedge-fund"
RELEASE_DIR="$ROOT_DIR/dist/releases"
RELEASE_DATE="$(date +%Y%m%d)"
ARCHIVE_NAME="ai-hedge-fund-openclaw-skill-${RELEASE_DATE}.tar.gz"

rm -rf "$PACKAGE_ROOT"
mkdir -p "$PACKAGE_ROOT/agents" "$PACKAGE_ROOT/references"
mkdir -p "$RELEASE_DIR"

cp "$ROOT_DIR/SKILL.md" "$PACKAGE_ROOT/SKILL.md"
cp "$ROOT_DIR/SKILL.toon" "$PACKAGE_ROOT/SKILL.toon"
cp "$ROOT_DIR/agents/openai.yaml" "$PACKAGE_ROOT/agents/openai.yaml"
cp "$ROOT_DIR/references/agents.md" "$PACKAGE_ROOT/references/agents.md"
cp "$ROOT_DIR/references/configuration.md" "$PACKAGE_ROOT/references/configuration.md"
cp "$ROOT_DIR/references/external-interface.md" "$PACKAGE_ROOT/references/external-interface.md"
cp "$ROOT_DIR/references/preloaded-data.md" "$PACKAGE_ROOT/references/preloaded-data.md"
cp "$ROOT_DIR/references/workflows.md" "$PACKAGE_ROOT/references/workflows.md"

tar -czf "$RELEASE_DIR/$ARCHIVE_NAME" -C "$ROOT_DIR/dist/openclaw-skill" ai-hedge-fund

echo "Packaged OpenClaw skill at $PACKAGE_ROOT"
echo "Created release archive at $RELEASE_DIR/$ARCHIVE_NAME"
echo "Install by copying or symlinking $PACKAGE_ROOT to ~/.agents/skills/ai-hedge-fund"
echo "This skill assumes the active workspace is the ai-hedge-fund repository root and uses the repository's own scripts/ entrypoints."
