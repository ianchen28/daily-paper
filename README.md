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
  - DeepSeek: `deepseek-chat`（普通模式）或 `deepseek-reasoner`（推理模式）
  - Gemini: `gemini-1.5-flash`
  - OpenAI: `gpt-3.5-turbo`
- `INCLUDE_REASONING`: 是否包含推理过程（可选，默认: false）
  - 仅对支持推理的模型（如 `deepseek-reasoner`）有效
  - 设置为 `true` 时，邮件中会包含模型的思考过程（以可折叠形式显示）

#### 邮件配置（必需）

- `EMAIL_SENDER`: 发件邮箱地址（必需）
- `EMAIL_PASSWORD`: 邮箱应用专用密码（必需，**不是登录密码**）
- `EMAIL_RECEIVER`: 接收邮箱地址（必需）
- `SMTP_SERVER`: SMTP 服务器地址（可选，默认: smtp.gmail.com）
- `SMTP_PORT`: SMTP 端口（可选，默认: 587）

#### 其他配置（可选）

- `KEYWORDS`: 关注的关键词（可选，默认: RAG, Agent, Multimodal, Efficient Training）
  - 格式：用逗号分隔的关键词，例如：`RAG, Agent, Multimodal, Efficient Training, LLM, Transformer`
  - LLM 会根据这些关键词评估论文与你的关注领域的相关性
  - 建议：3-8 个关键词，涵盖你主要关注的研究方向
  
- `MAX_PAPERS`: 最大论文数量（可选，默认: 6）
  - 设置每天获取和分析的论文数量
  - 建议范围：5-10 篇（太少可能错过重要论文，太多会增加分析时间和成本）
  
- `FEED_URL`: 论文源 RSS 地址（可选，已废弃，保留用于兼容性）
  - 现在直接使用 HuggingFace Daily Papers API，此参数不再使用

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

📖 **快速开始**：查看 [QUICK_START.md](QUICK_START.md) 获取快速配置清单

📚 **详细指南**：查看 [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) 获取完整配置说明

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
- `KEYWORDS`: 关注的关键词（默认: RAG, Agent, Multimodal, Efficient Training）
  - 格式：用逗号分隔，例如：`RAG, Agent, Multimodal, Efficient Training, LLM`
  - LLM 会根据这些关键词评估论文相关性
- `MAX_PAPERS`: 最大论文数量（默认: 6）
  - 建议范围：5-10 篇
- `FEED_URL`: 论文源 RSS 地址（已废弃，保留用于兼容性）

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
- ✅ **容错机制**：邮件发送失败时自动保存报告，不会丢失内容

## 故障排查

### 邮件发送问题

#### 邮件发送成功但未收到

如果程序显示"邮件发送成功"但收件箱中没有邮件：

1. **检查 Gmail 的"所有邮件"标签**：Gmail 可能将邮件放在"所有邮件"而不是"收件箱"
2. **检查垃圾邮件文件夹**：QQ 邮箱发送到 Gmail 可能被标记为垃圾邮件
3. **等待几分钟**：跨服务商邮件可能需要 5-15 分钟才能到达
4. **将发件人添加到联系人**：在 Gmail 中添加发件人到联系人，提高邮件到达率

#### 连接超时

如果遇到连接超时错误：

1. **增加超时时间**：在 `.env` 中设置 `SMTP_TIMEOUT=60`
2. **检查网络连接**：测试 SMTP 服务器是否可达
3. **检查防火墙/代理**：确保端口未被阻止
4. **尝试其他端口**：如果 465 端口不行，尝试 587 端口（TLS）

#### 认证失败

如果遇到认证失败：

1. **检查授权码**：确保使用的是授权码（不是登录密码）
2. **验证邮箱地址**：确保格式正确，没有多余空格
3. **检查服务启用**：确保已启用 SMTP 服务

### QQ 邮箱配置

如果使用 QQ 邮箱，需要：

1. **启用 SMTP 服务**：登录 QQ 邮箱 → 设置 → 账户 → 开启 POP3/SMTP 服务
2. **生成授权码**：在同一页面生成授权码（16位），**不是登录密码**
3. **配置参数**：

   ```bash
   SMTP_SERVER=smtp.qq.com
   SMTP_PORT=465
   SMTP_USE_SSL=true
   SMTP_USE_TLS=false
   EMAIL_PASSWORD=你的授权码（16位）
   ```

### 其他问题

- **LLM API 调用失败**：检查 API Key、余额、网络连接
- **论文获取失败**：检查网络连接、HuggingFace API 可访问性
- **报告内容为空**：检查 LLM API 配置、查看日志错误信息

**提示**：如果邮件发送失败，程序会自动保存报告到 HTML 文件（`daily_paper_report_*.html`），可以在浏览器中打开查看。

更多详细的故障排查信息，请查看 [故障排查指南](TROUBLESHOOTING.md)。

## 许可证

MIT
