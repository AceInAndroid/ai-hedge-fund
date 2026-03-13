---
name: "ai-hedge-fund"
description: "Use when working in this repository to run or modify the AI hedge fund system, configure compatible LLM providers, run analysis or backtests, inject external ticker data directly into the CLI, or extend the A-share data-source stack."
---

# AI Hedge Fund Skill

Use this skill when the task is repository-local and involves any of these:

- configure LLM providers, base URLs, API keys, or custom model names
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

## Task routing

- Configure providers or fix `.env`: use `scripts/skill-setup.sh`, then open `references/configuration.md`.
- Run one-shot analysis: use `scripts/run-analysis.sh`.
- Run a backtest: use `scripts/run-backtest.sh`.
- Start the full web app: use `scripts/run-web.sh`.
- Start backend/frontend separately: use `scripts/run-backend.sh` and `scripts/run-frontend.sh`.
- Validate Python and frontend state after edits: use `scripts/validate.sh`.
- Inject external data: keep execution on `run-analysis.sh` or `run-backtest.sh`, and add `--data-file`.

## Model/provider behavior

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

## Guardrails

- Prefer `scripts/*.sh` wrappers first.
- Do not hand-write long `poetry run ...` commands when a repo script already exists.
- Do not fetch remote data if the task explicitly provides a `--data-file` workflow.
- Do not assume A-share fundamentals/news coverage is complete just because prices are available.
- When a task is only about provider setup or data-file shape, avoid loading unrelated references.
