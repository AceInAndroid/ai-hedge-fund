# AI Hedge Fund

[English](./README.md) | [简体中文](./README.zh-CN.md)

This is a proof of concept for an AI-powered hedge fund.  The goal of this project is to explore the use of AI to make trading decisions.  This project is for **educational** purposes only and is not intended for real trading or investment.

This system employs several agents working together:

1. Aswath Damodaran Agent - The Dean of Valuation, focuses on story, numbers, and disciplined valuation
2. Ben Graham Agent - The godfather of value investing, only buys hidden gems with a margin of safety
3. Bill Ackman Agent - An activist investor, takes bold positions and pushes for change
4. Cathie Wood Agent - The queen of growth investing, believes in the power of innovation and disruption
5. Charlie Munger Agent - Warren Buffett's partner, only buys wonderful businesses at fair prices
6. Michael Burry Agent - The Big Short contrarian who hunts for deep value
7. Mohnish Pabrai Agent - The Dhandho investor, who looks for doubles at low risk
8. Peter Lynch Agent - Practical investor who seeks "ten-baggers" in everyday businesses
9. Phil Fisher Agent - Meticulous growth investor who uses deep "scuttlebutt" research 
10. Rakesh Jhunjhunwala Agent - The Big Bull of India
11. Stanley Druckenmiller Agent - Macro legend who hunts for asymmetric opportunities with growth potential
12. Warren Buffett Agent - The oracle of Omaha, seeks wonderful companies at a fair price
13. Valuation Agent - Calculates the intrinsic value of a stock and generates trading signals
14. Sentiment Agent - Analyzes market sentiment and generates trading signals
15. Fundamentals Agent - Analyzes fundamental data and generates trading signals
16. Technicals Agent - Analyzes technical indicators and generates trading signals
17. Risk Manager - Calculates risk metrics and sets position limits
18. Portfolio Manager - Makes final trading decisions and generates orders

<img width="1042" alt="Screenshot 2025-03-22 at 6 19 07 PM" src="https://github.com/user-attachments/assets/cbae3dcf-b571-490d-b0ad-3f0f035ac0d4" />

Note: the system does not actually make any trades.

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions
- Past performance does not indicate future results

By using this software, you agree to use it solely for learning purposes.

## Table of Contents
- [How to Install](#how-to-install)
- [OpenClaw Skill Install](#openclaw-skill-install)
- [Environment Configuration](#environment-configuration)
- [How to Run](#how-to-run)
  - [⌨️ Command Line Interface](#️-command-line-interface)
  - [🖥️ Web Application](#️-web-application)
- [How to Contribute](#how-to-contribute)
- [Feature Requests](#feature-requests)
- [License](#license)

## How to Install

Before you can run the AI Hedge Fund, install the Python and frontend dependencies first.

### 1. Clone the Repository

```bash
git clone https://github.com/AceInAndroid/ai-hedge-fund.git
cd ai-hedge-fund
```

### 2. Install Python Dependencies

This project uses Poetry and supports Python `3.11` and `3.12`. The recommended version is `3.11`.

If Python is not installed yet, one practical way is to install it with `pyenv`.

Install `pyenv` first:

```bash
brew install pyenv
```

Install Python `3.11`:

```bash
pyenv install 3.11.11
pyenv local 3.11.11
python3 --version
```

Install Python `3.12`:

```bash
pyenv install 3.12.9
pyenv local 3.12.9
python3 --version
```

If `poetry` is not installed yet, install it first:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

If the shell still cannot find `poetry`, add Poetry to your `PATH` and reopen the terminal:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then install project dependencies:

```bash
poetry env use python3
poetry install
```

If `poetry install` fails, check these common issues first:

- `poetry: command not found`: install Poetry with the command above, then reopen the terminal.
- Python version mismatch: make sure `python3 --version` is compatible with this project.
- Broken environment from an earlier install: try `poetry env remove --all` and then run `poetry install` again.

### 3. Install Frontend Dependencies

The web UI lives in `app/frontend`.

```bash
cd app/frontend
npm install
cd ../..
```

## OpenClaw Skill Install

This repository can also be packaged as an OpenClaw-installable skill.

### Option 1: Install directly into `~/.agents/skills`

```bash
bash scripts/install-openclaw-skill.sh
```

This installs the skill to:

```text
~/.agents/skills/ai-hedge-fund
```

### Option 2: Generate a distributable package first

```bash
bash scripts/package-openclaw-skill.sh
```

The packaged skill directory will be created at:

```text
dist/openclaw-skill/ai-hedge-fund
```

You can then copy or symlink it manually:

```bash
mkdir -p ~/.agents/skills
cp -R dist/openclaw-skill/ai-hedge-fund ~/.agents/skills/
```

### OpenClaw Notes

- The packaged skill contains `SKILL.md`, `SKILL.toon`, `agents/openai.yaml`, and the required `references/` files.
- The installed skill assumes the active workspace is still the `ai-hedge-fund` repository root.
- Runtime execution still uses this repository's own `scripts/` entrypoints.
- To expose the skill contract to external controllers, run:

```bash
bash scripts/export-skill-manifest.sh
```

## Environment Configuration

### 1. Create the `.env` File

```bash
cp .env.example .env
```

The `.env` file must be created in the project root directory, at the same level as `README.md`, `pyproject.toml`, and `src/`.

Example root path:

```text
ai-hedge-fund/
├── .env
├── .env.example
├── README.md
├── pyproject.toml
├── src/
└── app/
```

You can confirm you are in the project root with:

```bash
pwd
ls -la .env .env.example
```

How to open `.env`:

- VS Code:
  ```bash
  code .env
  ```
- macOS terminal editor:
  ```bash
  nano .env
  ```
- Linux terminal editor:
  ```bash
  nano .env
  ```
- Windows PowerShell:
  ```powershell
  notepad .env
  ```

If you use `nano`, edit the file, then press `Ctrl+O` to save and `Ctrl+X` to exit.

### 2. Minimum Required Configuration

At least one LLM provider must be configured, otherwise the agents cannot run.

You can use any one of these methods:

- Official OpenAI
- Official Anthropic
- OpenAI-compatible API
- Anthropic-compatible API
- LM Studio local server

### 3. Environment Variable Examples

All environment variable examples below must be written into the root `.env` file you just created.

Each line uses this format:

```bash
KEY=value
```

Do not wrap values in JSON. Do not add commas at the end of lines.

Example:

```bash
OPENAI_API_KEY=sk-xxxxx
OPENAI_API_BASE=https://api.openai.com/v1
```

#### Example A: Official OpenAI

```bash
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1
```

#### Example B: DashScope Anthropic-Compatible

```bash
ANTHROPIC_AUTH_TOKEN=your-dashscope-api-key
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

#### Example C: OpenAI-Compatible Gateway

```bash
OPENAI_COMPATIBLE_API_KEY=your-compatible-api-key
OPENAI_COMPATIBLE_BASE_URL=https://your-openai-compatible-host/v1
OPENAI_COMPATIBLE_MODEL=your-model-name
```

#### Example D: Anthropic-Compatible Gateway

```bash
ANTHROPIC_COMPATIBLE_API_KEY=your-compatible-api-key
ANTHROPIC_COMPATIBLE_BASE_URL=https://your-anthropic-compatible-host/v1
ANTHROPIC_COMPATIBLE_MODEL=your-model-name
```

#### Example E: LM Studio

```bash
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=your-local-model-name
```

#### Complete `.env` Example

This is a valid example of what the root `.env` file can look like:

```bash
# LLM provider: DashScope Anthropic-compatible
ANTHROPIC_AUTH_TOKEN=your-dashscope-api-key
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus

# Financial data
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# A-share price fallback order
PRICE_DATA_SOURCES=financial_datasets,akshare,baostock,tushare,tencent,xueqiu,baidu
TUSHARE_TOKEN=your-tushare-token
```

After editing `.env`, save the file and restart the CLI command or web backend so the new values are loaded.

### 3.2 Directly Inject External Data Into CLI

If another system already prepared detailed market or fundamental data, you can pass it directly to the scripts and skip repeated fetching.

Use:

```bash
--data-file ./sample-data.json
```

Add:

```bash
--data-only
```

when you want to disable all external fetching and use only the supplied file.

Example:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

The JSON file can contain per-ticker `prices`, `financial_metrics`, `line_items`, `company_news`, `insider_trades`, and `market_cap`. See the skill reference file [references/preloaded-data.md](./references/preloaded-data.md) for the full schema.

### 3.1 How CLI Model Selection Works

The CLI no longer requires you to choose from a built-in model catalog first.

Current behavior:

- CLI reads the configured provider from `.env`
- CLI reads the configured model name from the matching `*_MODEL` variable
- If only one provider is configured, it is selected automatically
- If multiple providers are configured, CLI asks you to choose among the configured providers only
- If a provider is configured but its `*_MODEL` value is missing, CLI asks you to type the model name manually

For example, if your `.env` contains:

```bash
ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

then running:

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

will use:

- provider: `Anthropic`
- model: `qwen3.5-plus`

without asking you to pick from built-in Claude or GPT model lists.

### 4. Financial Data Configuration

For US tickers, the existing `FINANCIAL_DATASETS_API_KEY` flow remains the main source.

```bash
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

### 5. A-Share Price Fallback Configuration

For mainland China tickers, the project now supports price fallback across:

- `financial_datasets`
- `akshare`
- `baostock`
- `tushare`
- `tencent`
- `xueqiu`
- `baidu`

Use this configuration in `.env` if you want to control the fallback order:

```bash
PRICE_DATA_SOURCES=financial_datasets,akshare,baostock,tushare,tencent,xueqiu,baidu
TUSHARE_TOKEN=your-tushare-token
```

Notes:

- `TUSHARE_TOKEN` is only required if `tushare` is included in `PRICE_DATA_SOURCES`.
- `Akshare`, `Baostock`, and `Tushare` are declared in `pyproject.toml`; run `poetry install` after pulling the latest changes.
- The A-share fallback currently applies to price data. Financial metrics, company news, and insider trades still use the original financial data flow.

### 6. Web Settings Page vs `.env`

If you use the web application:

- `.env` is the easiest way to set default configuration for local development.
- The Settings page in the web UI can also save provider keys, URLs, `PRICE_DATA_SOURCES`, and `TUSHARE_TOKEN`.
- Web-saved settings are passed into the backend request and can override missing environment values.

Where to configure what:

- Want defaults for local development: edit the root `.env` file.
- Want to change configuration from the browser: open the Web app, then go to `Settings`.
- Want both: keep stable defaults in `.env`, and use the Settings page for temporary or per-environment adjustments.

## How to Run

### ⌨️ Command Line Interface

You can run the AI Hedge Fund directly from the terminal for research, scripting, or debugging.

<img width="992" alt="Screenshot 2025-01-06 at 5 50 17 PM" src="https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b" />

#### List Available Agents and Capabilities

Before selecting analysts, you can inspect the built-in capability catalog:

```bash
bash scripts/list-agents.sh
```

For JSON output that another controller or script can consume:

```bash
bash scripts/list-agents.sh --format json
```

For a full external-skill manifest that another controller can consume directly:

```bash
bash scripts/export-skill-manifest.sh
```

This catalog includes:

- selectable analyst agents
- always-on system agents such as `risk_manager` and `portfolio_manager`
- each agent's strategy family, analysis method, execution mode, best-fit use case, A-share readiness, and data requirements
- a repo-managed external interface where callers do not need to supply LLM keys or model names by default

#### Analyze Tickers

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

If your `.env` already contains model settings, CLI uses them directly.

Example with DashScope Anthropic-compatible:

```bash
ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

Run:

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

CLI will use `qwen3.5-plus` automatically.

With external preloaded data:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

#### Analyze A-Share Tickers

```bash
poetry run python src/main.py --ticker 600519.SH,000001.SZ
```

You can optionally pass a time range:

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

If you want to use local models through Ollama:

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --ollama
```

#### Run the Backtester

```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

Backtester also supports `--start-date`, `--end-date`, and `--ollama`.

#### Common CLI Usage Notes

- `--ticker` uses a comma-separated list.
- A-share tickers can be written as `600519.SH`, `000001.SZ`, or six-digit codes such as `600519`.
- Make sure your `.env` is configured before running CLI commands.
- `--model-provider` and `--model` are optional overrides for CLI runs.
- If `.env` already defines `ANTHROPIC_MODEL`, `OPENAI_COMPATIBLE_MODEL`, `LM_STUDIO_MODEL`, and similar variables, CLI uses those values directly.

Example override:

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --model-provider anthropic --model qwen3.5-plus
```

Example with direct injected data:

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

Example with explicit analyst selection:

```bash
bash scripts/run-analysis.sh KO,AXP --analysts ben_graham,warren_buffett,valuation_analyst
```

### 🖥️ Web Application

The web application is the easiest way to switch models, edit flows, and manage saved settings.

#### Method 1: Start Both Services with One Command

macOS / Linux:

```bash
bash app/run.sh
```

Windows:

```bat
app\run.bat
```

#### Method 2: Start Backend and Frontend Manually

Backend:

```bash
poetry run uvicorn app.backend.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd app/frontend
npm run dev
```

After startup:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

#### Web Usage Flow

1. Open the Settings page and fill in your LLM/data-source configuration.
2. Choose model provider and model for each node if needed.
3. Enter tickers and date range.
4. Run the analysis or the backtest from the UI.

You can still find app-specific details in [app/README.md](./app/README.md).

<img width="1721" alt="Screenshot 2025-06-28 at 6 41 03 PM" src="https://github.com/user-attachments/assets/b95ab696-c9f4-416c-9ad1-51feb1f5374b" />


## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

**Important**: Please keep your pull requests small and focused.  This will make it easier to review and merge.

## Feature Requests

If you have a feature request, please open an [issue](https://github.com/AceInAndroid/ai-hedge-fund/issues) and make sure it is tagged with `enhancement`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
