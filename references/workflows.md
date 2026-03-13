# Workflow Reference

## Analyze tickers from CLI

US tickers:

```bash
bash scripts/run-analysis.sh AAPL,MSFT,NVDA
```

A-share tickers:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ
```

With explicit model override:

```bash
bash scripts/run-analysis.sh AAPL,MSFT,NVDA --model-provider anthropic --model qwen3.5-plus
```

With externally prepared data:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

## Run a backtest

```bash
bash scripts/run-backtest.sh AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

Backtest with externally prepared data:

```bash
bash scripts/run-backtest.sh 600519.SH,000001.SZ --start-date 2025-01-01 --end-date 2025-12-31 --data-file ./sample-data.json --data-only
```

## Start the web app

One command:

```bash
bash scripts/run-web.sh
```

Manual startup:

```bash
bash scripts/run-backend.sh
bash scripts/run-frontend.sh
```

## Troubleshooting

Missing Poetry modules:

```bash
bash scripts/skill-setup.sh
```

Python syntax validation:

```bash
bash scripts/validate.sh
```

Frontend build validation:

```bash
bash scripts/validate.sh
```

DashScope 404 checks:

- Anthropic-compatible endpoint should resolve to `/v1/messages`
- `ANTHROPIC_BASE_URL` may be configured as either `.../apps/anthropic` or `.../apps/anthropic/v1`

A-share caveat:

- Price fallback is implemented.
- Some valuation/fundamentals agents still rely on non-A-share financial endpoints and may need further adaptation for complete mainland market support.
