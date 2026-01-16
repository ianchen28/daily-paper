# Daily Paper

自动获取 daily papers 列表，使用大模型分析并推送结果到邮箱。

## 功能特性

- 📰 自动从 HuggingFace Papers RSS 获取最新论文
- 🤖 支持多种大模型（DeepSeek、Gemini、OpenAI 等）自动分析论文
- 📧 推送精美的 HTML 格式邮件到你的邮箱
- ⏰ 支持 GitHub Actions 定时运行
- 💰 完全免费：GitHub Actions 免费，Gemini Flash 免费层，Gmail 发信免费

## 技术栈

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) - 快速 Python 包管理器
- OpenAI 兼容 API（支持 DeepSeek、Gemini、OpenAI 等）

## 支持的 LLM

项目支持所有 OpenAI 兼容的 API，包括：

- **DeepSeek**: `LLM_BASE_URL=https://api.deepseek.com`, `MODEL_NAME=deepseek-chat`
- **Gemini**: `LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/`, `MODEL_NAME=gemini-1.5-flash`
- **OpenAI**: `LLM_BASE_URL=https://api.openai.com/v1`, `MODEL_NAME=gpt-3.5-turbo`

## 快速开始

### 1. 安装 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 克隆项目

```bash
git clone <your-repo-url>
cd daily-paper
```

### 3. 安装依赖

```bash
uv sync
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置以下变量：

#### LLM 配置（必需）

- `LLM_API_KEY`: 你的 LLM API Key（必需）
- `LLM_BASE_URL`: LLM API 地址（可选，根据使用的 LLM 设置）
- `MODEL_NAME`: 模型名称（可选，默认: deepseek-chat）

#### 邮件配置（必需）

- `EMAIL_SENDER`: 发件邮箱地址（必需）
- `EMAIL_PASSWORD`: 邮箱应用专用密码（必需，**不是登录密码**）
- `EMAIL_RECEIVER`: 接收邮箱地址（必需）
- `SMTP_SERVER`: SMTP 服务器地址（可选，默认: smtp.gmail.com）
- `SMTP_PORT`: SMTP 端口（可选，默认: 587）

#### 其他配置（可选）

- `KEYWORDS`: 关注的关键词（可选，默认: RAG, Agent, Multimodal, Efficient Training）
- `FEED_URL`: 论文源 RSS 地址（可选，默认: HuggingFace）
- `MAX_PAPERS`: 最大论文数量（可选，默认: 6）

### 5. 获取 Gmail 应用专用密码

如果使用 Gmail，需要生成应用专用密码（App Password）：

1. 访问 [Google 账号设置](https://myaccount.google.com/)
2. 进入 **安全** > **两步验证**（需要先启用两步验证）
3. 在底部找到 **应用专用密码**
4. 生成一个新密码，名称填写 "GitHubDaily" 或任意名称
5. 复制生成的 16 位密码（格式：`xxxx xxxx xxxx xxxx`），填入 `EMAIL_PASSWORD`

### 6. 运行

```bash
uv run python main.py
```

## GitHub Actions 配置

### 1. 设置 Secrets

在 GitHub 仓库的 Settings > Secrets and variables > Actions 中添加以下 secrets：

#### 必需配置

- `LLM_API_KEY`: LLM API Key
- `EMAIL_SENDER`: 发件邮箱地址
- `EMAIL_PASSWORD`: 邮箱应用专用密码
- `EMAIL_RECEIVER`: 接收邮箱地址

#### 可选配置

- `LLM_BASE_URL`: LLM API 地址
  - DeepSeek: `https://api.deepseek.com`
  - Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - OpenAI: `https://api.openai.com/v1`
- `MODEL_NAME`: 模型名称
  - DeepSeek: `deepseek-chat`
  - Gemini: `gemini-1.5-flash`
  - OpenAI: `gpt-3.5-turbo`
- `SMTP_SERVER`: SMTP 服务器（默认: smtp.gmail.com）
- `SMTP_PORT`: SMTP 端口（默认: 587）
- `KEYWORDS`: 关注的关键词
- `FEED_URL`: 论文源 RSS 地址
- `MAX_PAPERS`: 最大论文数量

### 2. 定时运行

工作流默认每天 UTC 时间 8:00（北京时间 16:00）运行。你也可以手动触发：

1. 进入 Actions 页面
2. 选择 "Daily Paper" workflow
3. 点击 "Run workflow"

### 3. 修改运行时间

编辑 `.github/workflows/daily-paper.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 8 * * *'  # UTC 时间 8:00
```

## 项目结构

```text
daily-paper/
├── daily_paper/          # 主包
│   ├── __init__.py
│   ├── config.py         # 配置管理
│   ├── paper_fetcher.py  # 论文获取
│   ├── llm_analyzer.py   # LLM 分析
│   ├── notifier.py       # 邮件推送
│   └── main.py           # 主逻辑
├── main.py               # 命令行入口
├── pyproject.toml        # 项目配置（uv）
├── .env.example          # 环境变量模板
├── .github/
│   └── workflows/
│       └── daily-paper.yml  # GitHub Actions 工作流
└── README.md
```

## 开发

### 安装开发依赖

```bash
uv sync --extra dev
```

### 代码检查

```bash
uv run ruff check .
```

## 为什么选择这个方案？

- ✅ **完全免费**：GitHub Actions 免费，Gemini Flash 免费层，Gmail 发信免费
- ✅ **排版精美**：LLM 生成 HTML，邮件里支持粗体、链接跳转，体验比纯文本好得多
- ✅ **零依赖**：不需要注册任何第三方推送平台，不用担心它们跑路或收费
- ✅ **灵活配置**：支持多种 LLM，可根据需求选择

## 许可证

MIT
