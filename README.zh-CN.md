# AI Hedge Fund

[English](./README.md) | [简体中文](./README.zh-CN.md)

这是一个 AI 驱动的量化对冲基金原型项目，目标是探索如何使用多智能体系统辅助生成交易决策。项目仅用于**学习、研究与演示**，不用于真实交易或投资建议。

系统内置多个投资风格代理协同工作，包括：

1. Aswath Damodaran Agent：重视叙事、数字和严谨估值
2. Ben Graham Agent：价值投资，强调安全边际
3. Bill Ackman Agent：激进投资和事件驱动
4. Cathie Wood Agent：成长与创新驱动
5. Charlie Munger Agent：优质公司与长期复利
6. Michael Burry Agent：逆向投资与深度价值
7. Mohnish Pabrai Agent：低风险高赔率机会
8. Peter Lynch Agent：寻找高成长“ten-bagger”
9. Phil Fisher Agent：深度调研与“scuttlebutt”
10. Rakesh Jhunjhunwala Agent：印度市场成长风格
11. Stanley Druckenmiller Agent：宏观趋势与非对称机会
12. Warren Buffett Agent：好公司与合理价格
13. Valuation Agent：计算内在价值并输出信号
14. Sentiment Agent：分析市场情绪并输出信号
15. Fundamentals Agent：分析基本面并输出信号
16. Technicals Agent：分析技术指标并输出信号
17. Risk Manager：控制风险并设置仓位限制
18. Portfolio Manager：汇总信号并给出最终交易决策

<img width="1042" alt="Screenshot 2025-03-22 at 6 19 07 PM" src="https://github.com/user-attachments/assets/cbae3dcf-b571-490d-b0ad-3f0f035ac0d4" />

说明：系统不会真实下单。

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## 免责声明

本项目仅用于**教育和研究**。

- 不用于真实交易或投资
- 不构成任何投资建议
- 作者不对金融损失承担责任
- 请在真实投资前咨询专业顾问
- 历史表现不代表未来结果

使用本软件即表示你同意仅将其用于学习和研究目的。

## 目录

- [安装方法](#安装方法)
- [OpenClaw Skill 安装](#openclaw-skill-安装)
- [环境配置](#环境配置)
- [使用方法](#使用方法)
  - [⌨️ 命令行](#️-命令行)
  - [🖥️ Web 应用](#️-web-应用)
- [如何贡献](#如何贡献)
- [功能需求](#功能需求)
- [许可证](#许可证)

## 安装方法

运行项目前，请先安装 Python 和前端依赖。

### 1. 克隆仓库

```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

### 2. 安装 Python 依赖

项目使用 Poetry，建议 Python 版本为 `3.11`。

```bash
poetry install
```

### 3. 安装前端依赖

Web 前端位于 `app/frontend`。

```bash
cd app/frontend
npm install
cd ../..
```

## OpenClaw Skill 安装

这个仓库也可以打包成 OpenClaw 可安装的 Skill。

### 方式 1：直接安装到 `~/.agents/skills`

```bash
bash scripts/install-openclaw-skill.sh
```

默认会安装到：

```text
~/.agents/skills/ai-hedge-fund
```

### 方式 2：先生成可分发安装包

```bash
bash scripts/package-openclaw-skill.sh
```

生成后的 Skill 目录在：

```text
dist/openclaw-skill/ai-hedge-fund
```

然后可以手动复制或软链接：

```bash
mkdir -p ~/.agents/skills
cp -R dist/openclaw-skill/ai-hedge-fund ~/.agents/skills/
```

### OpenClaw 使用说明

- 打包后的 Skill 包含 `SKILL.md`、`SKILL.toon`、`agents/openai.yaml` 和必需的 `references/` 文件。
- 安装后的 Skill 默认假设当前工作目录仍然是 `ai-hedge-fund` 仓库根目录。
- 实际执行仍然调用本仓库自己的 `scripts/` 入口。
- 如果要把 Skill 接口暴露给外部控制器，可以运行：

```bash
bash scripts/export-skill-manifest.sh
```

## 环境配置

### 1. 创建 `.env`

```bash
cp .env.example .env
```

`.env` 文件必须放在项目根目录，也就是和 `README.md`、`pyproject.toml`、`src/` 同一级的位置。

目录示意：

```text
ai-hedge-fund/
├── .env
├── .env.example
├── README.md
├── pyproject.toml
├── src/
└── app/
```

你可以用下面的命令确认自己当前就在项目根目录：

```bash
pwd
ls -la .env .env.example
```

如何打开 `.env`：

- 使用 VS Code：
  ```bash
  code .env
  ```
- macOS / Linux 终端编辑：
  ```bash
  nano .env
  ```
- Windows PowerShell：
  ```powershell
  notepad .env
  ```

如果你使用 `nano`，编辑完成后按 `Ctrl+O` 保存，再按 `Ctrl+X` 退出。

### 2. 最低必需配置

至少配置一个 LLM 提供方，否则 agent 无法运行。

可选方式包括：

- 官方 OpenAI
- 官方 Anthropic
- OpenAI 兼容协议
- Anthropic 兼容协议
- LM Studio 本地服务

### 3. 环境变量示例

下面这些环境变量示例，都是写进项目根目录的 `.env` 文件里，不是写在 JSON 文件里，也不是写在代码里。

每一行格式都是：

```bash
KEY=value
```

不要在每一行末尾加逗号，也不要写成 JSON。

例如：

```bash
OPENAI_API_KEY=sk-xxxxx
OPENAI_API_BASE=https://api.openai.com/v1
```

#### 示例 A：官方 OpenAI

```bash
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1
```

#### 示例 B：DashScope Anthropic 兼容接口

```bash
ANTHROPIC_AUTH_TOKEN=your-dashscope-api-key
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

#### 示例 C：OpenAI 兼容网关

```bash
OPENAI_COMPATIBLE_API_KEY=your-compatible-api-key
OPENAI_COMPATIBLE_BASE_URL=https://your-openai-compatible-host/v1
OPENAI_COMPATIBLE_MODEL=your-model-name
```

#### 示例 D：Anthropic 兼容网关

```bash
ANTHROPIC_COMPATIBLE_API_KEY=your-compatible-api-key
ANTHROPIC_COMPATIBLE_BASE_URL=https://your-anthropic-compatible-host/v1
ANTHROPIC_COMPATIBLE_MODEL=your-model-name
```

#### 示例 E：LM Studio

```bash
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=your-local-model-name
```

#### 一个完整的 `.env` 示例

下面是一份可以直接参考的根目录 `.env` 示例：

```bash
# LLM 提供方：DashScope Anthropic 兼容接口
ANTHROPIC_AUTH_TOKEN=your-dashscope-api-key
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus

# 金融数据
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# A 股价格兜底顺序
PRICE_DATA_SOURCES=financial_datasets,akshare,baostock,tushare,tencent,xueqiu,baidu
TUSHARE_TOKEN=your-tushare-token
```

修改完 `.env` 后，记得保存文件，并重新启动命令行任务或 Web 后端，这样新配置才会生效。

### 3.2 直接把外部数据塞给 CLI

如果外部系统已经准备好了详细行情、财务或新闻数据，可以直接把这些数据文件传给脚本，避免再次联网抓取。

使用：

```bash
--data-file ./sample-data.json
```

如果你希望完全禁止外部抓取，只使用注入的数据，再加上：

```bash
--data-only
```

示例：

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

这个 JSON 文件里可以按 ticker 提供 `prices`、`financial_metrics`、`line_items`、`company_news`、`insider_trades`、`market_cap`。完整格式见 [references/preloaded-data.md](./references/preloaded-data.md)。

### 3.1 CLI 如何选择模型

现在命令行不会再先让你从一大串内置模型列表里选。

当前规则是：

- CLI 先从 `.env` 读取已经配置好的 provider
- 再从对应的 `*_MODEL` 环境变量里读取 model name
- 如果只配置了一个 provider，就自动使用它
- 如果配置了多个 provider，CLI 只会让你在“已配置”的 provider 里选
- 如果 provider 已配置，但没有填对应的 `*_MODEL`，CLI 才会让你手动输入 model name

例如你的 `.env` 里如果是：

```bash
ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

那么执行：

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

CLI 会直接使用：

- provider：`Anthropic`
- model：`qwen3.5-plus`

不会再弹出内置 Claude / GPT 模型列表让你选。

### 4. 金融数据配置

美股等原有数据流仍然主要使用 `FINANCIAL_DATASETS_API_KEY`。

```bash
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

### 5. A 股价格兜底配置

针对中国大陆股票，项目现在支持以下价格数据源兜底：

- `financial_datasets`
- `akshare`
- `baostock`
- `tushare`
- `tencent`
- `xueqiu`
- `baidu`

如果你希望显式控制兜底顺序，可以在 `.env` 中设置：

```bash
PRICE_DATA_SOURCES=financial_datasets,akshare,baostock,tushare,tencent,xueqiu,baidu
TUSHARE_TOKEN=your-tushare-token
```

说明：

- 只有当 `PRICE_DATA_SOURCES` 中包含 `tushare` 时，才需要配置 `TUSHARE_TOKEN`。
- `Akshare`、`Baostock`、`Tushare` 已经加入 `pyproject.toml`，拉取最新代码后请重新执行一次 `poetry install`。
- 当前 A 股扩展主要覆盖价格数据。财务指标、公司新闻、内幕交易仍然沿用原有金融数据接口。

### 6. Web 设置页与 `.env` 的关系

如果你使用 Web 应用：

- `.env` 适合作为本地默认配置。
- Web 界面的 Settings 页面也可以保存模型 Key、URL、`PRICE_DATA_SOURCES` 和 `TUSHARE_TOKEN`。
- Web 页面保存的配置会随请求传入后端，可用于补足或覆盖缺失的环境变量。

可以这样理解“在哪配置”：

- 想配本地默认值：改项目根目录的 `.env`
- 想在浏览器里改：打开 Web 应用后进入 `Settings`
- 两种都想用：把稳定配置放 `.env`，把临时调整放在 Settings 页面

## 使用方法

### ⌨️ 命令行

命令行适合研究、调试和脚本化运行。

<img width="992" alt="Screenshot 2025-01-06 at 5 50 17 PM" src="https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b" />

#### 查看可用 Agent 和能力目录

在选择分析师之前，可以先查看项目内置的 agent 能力目录：

```bash
bash scripts/list-agents.sh
```

如果要给外部控制器、脚本或其他 agent 使用，可以输出 JSON：

```bash
bash scripts/list-agents.sh --format json
```

如果要给外部控制器直接消费完整 Skill 接口，可以导出 manifest：

```bash
bash scripts/export-skill-manifest.sh
```

这个目录会暴露：

- 可选择的 analyst agents
- 始终参与流程的 system agents，例如 `risk_manager` 和 `portfolio_manager`
- 每个 agent 的策略类型、分析方法、执行模式、适用场景、A 股适配度和数据依赖
- 一个默认由仓库自己管理 LLM 配置的外部调用接口，外部方默认不需要传 key 和 model

#### 分析股票

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

如果你的 `.env` 已经配置了模型，CLI 会直接使用该配置。

例如 DashScope Anthropic 兼容配置：

```bash
ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
ANTHROPIC_BASE_URL=https://coding.dashscope.aliyuncs.com/apps/anthropic
ANTHROPIC_MODEL=qwen3.5-plus
```

运行：

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

CLI 会自动使用 `qwen3.5-plus`。

如果要直接使用外部准备好的数据：

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

#### 分析 A 股

```bash
poetry run python src/main.py --ticker 600519.SH,000001.SZ
```

可以指定日期范围：

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

如果你要通过 Ollama 使用本地模型：

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --ollama
```

#### 运行回测

```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

回测同样支持 `--start-date`、`--end-date` 和 `--ollama`。

#### 命令行使用说明

- `--ticker` 使用逗号分隔多个股票代码。
- A 股 ticker 支持 `600519.SH`、`000001.SZ`，也支持纯六位代码如 `600519`。
- 执行命令前，请先确认 `.env` 已配置完成。
- `--model-provider` 和 `--model` 可以作为 CLI 的临时覆盖参数。
- 如果 `.env` 里已经定义了 `ANTHROPIC_MODEL`、`OPENAI_COMPATIBLE_MODEL`、`LM_STUDIO_MODEL` 等值，CLI 会直接使用它们。

覆盖示例：

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --model-provider anthropic --model qwen3.5-plus
```

直接注入数据示例：

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

指定分析师示例：

```bash
bash scripts/run-analysis.sh KO,AXP --analysts ben_graham,warren_buffett,valuation_analyst
```

### 🖥️ Web 应用

如果你希望可视化编辑流程、切换节点模型或管理保存的设置，建议使用 Web 应用。

#### 方式 1：一条命令启动前后端

macOS / Linux：

```bash
bash app/run.sh
```

Windows：

```bat
app\run.bat
```

#### 方式 2：手动分别启动后端和前端

后端：

```bash
poetry run uvicorn app.backend.main:app --reload --host 127.0.0.1 --port 8000
```

前端：

```bash
cd app/frontend
npm run dev
```

启动后访问：

- 前端：`http://localhost:5173`
- 后端 API：`http://localhost:8000`
- Swagger 文档：`http://localhost:8000/docs`

#### Web 使用流程

1. 打开 Settings 页面，填写模型与数据源配置。
2. 按需为各个节点选择模型提供方和模型名称。
3. 输入 ticker 与日期范围。
4. 在页面中运行分析或回测。

更多 Web 端细节可参考 [app/README.md](./app/README.md)。

<img width="1721" alt="Screenshot 2025-06-28 at 6 41 03 PM" src="https://github.com/user-attachments/assets/b95ab696-c9f4-416c-9ad1-51feb1f5374b" />

## 如何贡献

1. Fork 本仓库
2. 创建功能分支
3. 提交修改
4. 推送到远端分支
5. 发起 Pull Request

建议保持 PR 小而聚焦，方便 review 和合并。

## 功能需求

如果你有新功能建议，请在 [Issues](https://github.com/virattt/ai-hedge-fund/issues) 中提交，并标注 `enhancement`。

## 许可证

本项目基于 MIT License 开源，详情见 `LICENSE` 文件。
