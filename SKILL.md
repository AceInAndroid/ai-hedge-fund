---
name: "ai-hedge-fund"
description: "Use when working in this repository to expose agent capabilities and analysis methods to external callers, inspect agent capabilities, configure compatible LLM providers, run analysis or backtests, inject external ticker data directly into the CLI, or extend the A-share data-source stack."
---

# AI Hedge Fund Skill

Use this skill when the task is repository-local and involves any of these:

- configure LLM providers, base URLs, API keys, or custom model names
- inspect which analyst or system agent fits a task
- run CLI analysis, backtests, or web flows from this repo
- inject upstream-prepared market/fundamental/news data instead of fetching again
- extend A-share data-source fallbacks or compatible transport logic
- patch or validate the scripts and docs that control these flows

Do not use this skill for generic finance questions that are not tied to this codebase.

## Execution style

Prefer the bundled `scripts/` entrypoints over reconstructing shell commands from prose. This keeps execution deterministic and easier for OpenClaw, Codex, or Claude to control.

Read only the reference file needed for the current task:

- provider or `.env` setup: `references/configuration.md`
- run flow, validation, or troubleshooting: `references/workflows.md`
- agent catalog and selection guidance: `references/agents.md`
- external interface and repo-managed execution contract: `references/external-interface.md`
- injected JSON payload shape: `references/preloaded-data.md`

## Quick start

Setup:

```bash
bash scripts/skill-setup.sh
```

## Default entrypoints

Pick the narrowest script that matches the request.

Analysis:

```bash
bash scripts/run-analysis.sh AAPL,MSFT,NVDA
bash scripts/run-analysis.sh 600519.SH,000001.SZ
```

Backtest:

```bash
bash scripts/run-backtest.sh AAPL,MSFT,NVDA
```

Web app:

```bash
bash scripts/run-web.sh
```

Manual web startup:

```bash
bash scripts/run-backend.sh
bash scripts/run-frontend.sh
```

Validation:

```bash
bash scripts/validate.sh
```

Agent catalog:

```bash
bash scripts/list-agents.sh
bash scripts/list-agents.sh --format json
bash scripts/export-skill-manifest.sh
bash scripts/package-openclaw-skill.sh
```

## Task routing

- Configure providers or fix `.env`: use `scripts/skill-setup.sh`, then open `references/configuration.md`.
- Run one-shot analysis: use `scripts/run-analysis.sh`.
- Run a backtest: use `scripts/run-backtest.sh`.
- Start the full web app: use `scripts/run-web.sh`.
- Start backend/frontend separately: use `scripts/run-backend.sh` and `scripts/run-frontend.sh`.
- Validate Python and frontend state after edits: use `scripts/validate.sh`.
- Explain which analyst or system agent does what: use `scripts/list-agents.sh`, then open `references/agents.md` if needed.
- Expose this repo to another controller or teammate: use `scripts/export-skill-manifest.sh`, then open `references/external-interface.md` if needed.
- Package this repo as an OpenClaw-installable skill: use `scripts/package-openclaw-skill.sh`.
- Inject external data: keep execution on `run-analysis.sh` or `run-backtest.sh`, and add `--data-file`.

## Model/provider behavior

- External callers should not be required to pass LLM credentials or model names unless they explicitly want to override repo defaults.
- CLI now prefers `.env`-configured providers and model names instead of a built-in model catalog.
- If one provider is configured, CLI uses it automatically.
- If multiple providers are configured, CLI asks only among configured providers.
- `--model-provider` and `--model` are optional overrides.
- DashScope Anthropic-compatible config is supported:

```bash
ANTHROPIC_AUTH_TOKEN=...
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

## Direct data injection

If an upstream system already prepared detailed data, inject it instead of fetching again:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
bash scripts/run-backtest.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

- `--data-file` points to a JSON file with preloaded ticker data.
- `--data-only` disables all external fetching and uses only the injected data.
- If `--data-file` is provided without `--data-only`, the runtime uses injected data first and only fetches missing parts externally.

Read `references/preloaded-data.md` for the JSON schema.

Use `--data-only` when the caller requires deterministic execution without network dependence.

When exposing this repo outward, prefer `--data-file` over telling callers to reimplement data fetches.

## A-share data behavior

- Price fallback order is controlled by `PRICE_DATA_SOURCES`.
- Supported price sources: `financial_datasets`, `akshare`, `baostock`, `tushare`, `tencent`, `xueqiu`, `baidu`.
- `TUSHARE_TOKEN` is only required when `tushare` is enabled.
- A-share fallback currently focuses on price/history retrieval. Fundamentals/news/insider coverage is still partial.

## Important files

- Main Python app code lives in `src/`.
- Web app code lives under `app/backend` and `app/frontend`.
- Compatible LLM transport logic lives in `src/llm/compatible.py`.
- A-share market data fallback logic lives in `src/tools/a_share_data.py`.
- Preloaded-data injection logic lives in `src/tools/preloaded_data.py`.
- CLI model/provider selection lives in `src/cli/input.py`.

## References

Open only what you need:

- provider setup and `.env` behavior: `references/configuration.md`
- run flows and troubleshooting: `references/workflows.md`
- injected data schema: `references/preloaded-data.md`
- agent capability catalog and selection guidance: `references/agents.md`
- external interface and repo-managed usage contract: `references/external-interface.md`

## Guardrails

- Prefer `scripts/*.sh` wrappers first.
- Do not hand-write long `poetry run ...` commands when a repo script already exists.
- Do not require external callers to provide LLM setup if the repository can resolve it from `.env`.
- Do not fetch remote data if the task explicitly provides a `--data-file` workflow.
- OpenClaw-installed copies of this skill assume the active workspace is still the ai-hedge-fund repository root.
- Do not assume A-share fundamentals/news coverage is complete just because prices are available.
- When a task is only about provider setup or data-file shape, avoid loading unrelated references.
