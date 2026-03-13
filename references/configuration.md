# Configuration Reference

## Root `.env`

Create the root file from `.env.example`:

```bash
bash scripts/skill-setup.sh
```

The `.env` file lives at the repository root beside `pyproject.toml`.

If `.env` already exists, edit it directly instead of recreating it.

## Common provider configs

DashScope Anthropic-compatible:

```bash
ANTHROPIC_AUTH_TOKEN=your-api-key
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

OpenAI-compatible:

```bash
OPENAI_COMPATIBLE_API_KEY=your-api-key
OPENAI_COMPATIBLE_BASE_URL=https://your-host/v1
OPENAI_COMPATIBLE_MODEL=your-model-name
```

LM Studio:

```bash
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=your-local-model
```

## Financial data

Base financial dataset:

```bash
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

A-share fallback order:

```bash
PRICE_DATA_SOURCES=financial_datasets,akshare,baostock,tushare,tencent,xueqiu,baidu
TUSHARE_TOKEN=your-tushare-token
```

## CLI model behavior

- `src/main.py` and `src/backtester.py` read configured providers from `.env`.
- If only one provider is configured, it is auto-selected.
- If the provider has no configured `*_MODEL`, the CLI prompts for a model name.
- `--model-provider` and `--model` override `.env` for a single run.

## Direct data injection

If external data is already available, use:

```bash
--data-file /absolute/or/relative/path/to/data.json
```

Add:

```bash
--data-only
```

when you want to prevent all external data fetching.

See `references/preloaded-data.md` for the exact JSON schema.
