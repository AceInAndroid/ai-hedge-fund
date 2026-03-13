# External Skill Interface

Use this file when another controller, skill runner, or teammate needs to consume this repository as a packaged capability instead of reading the codebase manually.

## Contract

- The caller does not need to provide LLM credentials, base URLs, or model names by default.
- The repository resolves LLM settings from the root `.env` file or saved web settings.
- The caller does not need to fetch market or fundamentals data if they already have it.
- The preferred external mode is to inject a JSON file with `--data-file`.
- Add `--data-only` when the caller wants deterministic execution with zero remote fetching.

## Discover the interface

Full machine-readable manifest:

```bash
bash scripts/export-skill-manifest.sh
```

OpenClaw packaging:

```bash
bash scripts/package-openclaw-skill.sh
```

Local install into `~/.agents/skills`:

```bash
bash scripts/install-openclaw-skill.sh
```

Live agent catalog:

```bash
bash scripts/list-agents.sh --format json
```

## Minimum external inputs

- Required: `tickers`
- Optional: `analysts`, `start_date`, `end_date`, `data_file`, `data_only`, `initial_cash`, `margin_requirement`

## Recommended external workflows

External caller wants the repo to manage LLM and only pass tickers:

```bash
bash scripts/run-analysis.sh AAPL,MSFT,NVDA
```

External caller already has full data and wants zero fetching:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --analysts technical_analyst,fundamentals_analyst,valuation_analyst --data-file ./sample-data.json --data-only
```

External caller wants a machine-readable description before choosing agents:

```bash
bash scripts/export-skill-manifest.sh
bash scripts/list-agents.sh --format json
```

## Practical guidance

- For external A-share workflows, prefer `technical_analyst`, `fundamentals_analyst`, `valuation_analyst`, and the built-in `risk_manager` / `portfolio_manager` path.
- For external users without LLM config, do not ask them to supply API keys unless they explicitly want to override the repository defaults.
- For external users with upstream data, do not ask them to refetch company news, prices, or financial metrics if those fields are already present in the injected JSON.
- The OpenClaw-installed skill is metadata plus references; actual execution still assumes the active workspace is the `ai-hedge-fund` repository root.
