---
name: "ai-hedge-fund"
description: "Use when working in this repository to run or modify the AI hedge fund system, configure compatible LLM endpoints, debug CLI or web flows, and analyze US or A-share tickers with the project's backtesting and data-source stack."
---

# AI Hedge Fund Skill

Use this skill when the task is about this repository's hedge-fund workflow: configuring LLM providers, running CLI or web analysis, backtesting, or extending A-share data support.

## Execution style

Prefer the bundled `scripts/` entrypoints over manually composing long shell commands. This keeps the skill deterministic and easier for OpenClaw, Codex, or Claude to control.

## Quick start

Preferred setup command:

```bash
bash scripts/skill-setup.sh
```

## Canonical run paths

CLI analysis:

```bash
bash scripts/run-analysis.sh AAPL,MSFT,NVDA
bash scripts/run-analysis.sh 600519.SH,000001.SZ
```

CLI backtest:

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

## Model selection rules

- CLI now prefers `.env`-configured providers and model names instead of a built-in model catalog.
- If one provider is configured, CLI uses it automatically.
- If multiple providers are configured, CLI asks only among configured providers.
- `--model-provider` and `--model` are optional overrides.
- Anthropic-compatible DashScope style config is supported through:

```bash
ANTHROPIC_AUTH_TOKEN=...
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

## A-share data behavior

- Price fallback order is controlled by `PRICE_DATA_SOURCES`.
- Supported A-share price sources: `financial_datasets`, `akshare`, `baostock`, `tushare`, `tencent`, `xueqiu`, `baidu`.
- `TUSHARE_TOKEN` is only required when `tushare` is enabled.
- A-share fallback currently focuses on price/history retrieval. Financial metrics, company news, and insider data still primarily follow the original financial-data flow.

## Important repo conventions

- Main Python app code lives in `src/`.
- Web app code lives under `app/backend` and `app/frontend`.
- Compatible LLM transport logic lives in `src/llm/compatible.py`.
- A-share market data fallback logic lives in `src/tools/a_share_data.py`.
- CLI model/provider selection lives in `src/cli/input.py`.

## Common validation commands

```bash
bash scripts/validate.sh
```

## References

Open only what you need:

- Setup and environment details: `references/configuration.md`
- Run flows and troubleshooting: `references/workflows.md`

## Review findings

- The initial skill version depended on chained shell commands and multi-step `cd` changes, which is higher-friction for controller-style agents.
- The initial skill version had no deterministic `scripts/` entrypoints, so agents had to reconstruct commands from prose.
- The current skill fixes that by providing stable wrapper scripts for setup, analysis, backtest, web startup, and validation.
