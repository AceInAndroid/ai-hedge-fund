# Agent Capability Reference

Use this file when the task is about choosing analysts, understanding agent coverage, or exposing repo capabilities to another controller or user.

For a live catalog from code, run:

```bash
bash scripts/list-agents.sh
```

For machine-readable output:

```bash
bash scripts/list-agents.sh --format json
```

For the full external skill contract, including repo-managed LLM and data handling:

```bash
bash scripts/export-skill-manifest.sh
```

## How to choose agents

- Use `technical_analyst` when only price history is available or when A-share support needs to be the most reliable.
- Use `fundamentals_analyst` or `valuation_analyst` when you have structured financial metrics and want deterministic signals without depending on LLM synthesis.
- Use value-style persona agents such as `aswath_damodaran`, `ben_graham`, `warren_buffett`, or `mohnish_pabrai` when fundamentals and market cap are available.
- Use `news_sentiment_analyst` or `sentiment_analyst` only when company news or insider-trade coverage is actually present.
- Use `stanley_druckenmiller` when you want a hybrid of fundamentals, momentum, and narrative.
- Remember that `risk_manager` and `portfolio_manager` always run after the selected analysts.

## External-use contract

- External callers do not need to pass provider URLs, keys, or model names unless they are deliberately overriding repository defaults.
- External callers should prefer `--data-file` and, when required, `--data-only` instead of reimplementing the repo's data-fetch path.
- Deterministic, no-LLM-first external stacks usually start with `technical_analyst`, `fundamentals_analyst`, `valuation_analyst`, and the built-in `risk_manager` / `portfolio_manager` path.

## A-share guidance

- Highest readiness: `technical_analyst`, `risk_manager`, `portfolio_manager`
- Medium readiness: `fundamentals_analyst`, `growth_analyst`, `valuation_analyst`, most valuation-style persona agents if you inject the needed fundamentals
- Lowest readiness: news-heavy and insider-heavy agents unless upstream data is injected through `--data-file`

## Selection examples

Deterministic A-share run with injected fundamentals:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --analysts technical_analyst,fundamentals_analyst,valuation_analyst --data-file ./sample-data.json --data-only
```

Growth plus narrative run:

```bash
bash scripts/run-analysis.sh NVDA,TSLA --analysts cathie_wood,stanley_druckenmiller,news_sentiment_analyst
```

Classic value stack:

```bash
bash scripts/run-analysis.sh KO,AXP --analysts ben_graham,warren_buffett,aswath_damodaran
```
