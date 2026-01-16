# GitHub Actions 配置指南

本文档详细说明如何配置 GitHub Actions 来定时运行 Daily Paper 项目。

## 步骤 1: 推送代码到 GitHub

如果还没有推送代码，先推送到 GitHub：

```bash
git push origin main
```

## 步骤 2: 配置 GitHub Secrets

### 2.1 进入 Secrets 设置页面

1. 打开你的 GitHub 仓库
2. 点击 **Settings**（设置）
3. 在左侧菜单中找到 **Secrets and variables** > **Actions**
4. 点击 **New repository secret**（新建仓库密钥）

### 2.2 添加必需的 Secrets

按照以下顺序添加所有必需的配置：

#### 🔑 必需配置（必须添加）

**1. LLM_API_KEY**

- **Name**: `LLM_API_KEY`
- **Value**: 你的 LLM API Key
- **示例**: `sk-xxxxxxxxxxxxxxxxxxxxx`

**2. EMAIL_SENDER**

- **Name**: `EMAIL_SENDER`
- **Value**: 发件邮箱地址
- **示例**: `your_email@gmail.com` 或 `your_email@qq.com`

**3. EMAIL_PASSWORD**

- **Name**: `EMAIL_PASSWORD`
- **Value**: 邮箱应用专用密码（**不是登录密码**）
  - Gmail: 应用专用密码（16位）
  - QQ 邮箱: 授权码（16位）
- **示例**: `xxxx xxxx xxxx xxxx`（可以包含或不包含空格）

**4. EMAIL_RECEIVER**

- **Name**: `EMAIL_RECEIVER`
- **Value**: 接收邮箱地址
- **示例**: `your_email@gmail.com`

#### ⚙️ 可选配置（根据需要添加）

**5. LLM_BASE_URL**

- **Name**: `LLM_BASE_URL`
- **Value**: LLM API 地址
- **默认值**: 如果不设置，DeepSeek 使用默认地址
- **示例**:
  - DeepSeek: `https://api.deepseek.com`
  - Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - OpenAI: `https://api.openai.com/v1`

**6. MODEL_NAME**

- **Name**: `MODEL_NAME`
- **Value**: 模型名称
- **默认值**: `deepseek-chat`
- **示例**:
  - DeepSeek: `deepseek-chat` 或 `deepseek-reasoner`
  - Gemini: `gemini-1.5-flash`
  - OpenAI: `gpt-3.5-turbo`

**7. INCLUDE_REASONING**

- **Name**: `INCLUDE_REASONING`
- **Value**: 是否包含推理过程（仅对推理模式有效）
- **默认值**: `false`
- **可选值**: `true` 或 `false`

**8. SMTP_SERVER**

- **Name**: `SMTP_SERVER`
- **Value**: SMTP 服务器地址
- **默认值**: `smtp.gmail.com`
- **示例**:
  - Gmail: `smtp.gmail.com`
  - QQ 邮箱: `smtp.qq.com`
  - Outlook: `smtp-mail.outlook.com`

**9. SMTP_PORT**

- **Name**: `SMTP_PORT`
- **Value**: SMTP 端口
- **默认值**: `587`
- **示例**:
  - Gmail TLS: `587`
  - QQ 邮箱 SSL: `465`
  - QQ 邮箱 TLS: `587`

**10. SMTP_USE_SSL**

- **Name**: `SMTP_USE_SSL`
- **Value**: 是否使用 SSL（用于 465 端口）
- **默认值**: `false`
- **可选值**: `true` 或 `false`
- **注意**: 如果使用 465 端口，设置为 `true`

**11. SMTP_USE_TLS**

- **Name**: `SMTP_USE_TLS`
- **Value**: 是否使用 TLS（用于 587 端口）
- **默认值**: `true`
- **可选值**: `true` 或 `false`
- **注意**: 如果使用 587 端口，设置为 `true`

**12. SMTP_TIMEOUT**

- **Name**: `SMTP_TIMEOUT`
- **Value**: SMTP 连接超时时间（秒）
- **默认值**: `30`
- **示例**: `60`（如果网络较慢，可以增加）

**13. KEYWORDS**

- **Name**: `KEYWORDS`
- **Value**: 关注的关键词（用逗号分隔）
- **默认值**: `RAG, Agent, Multimodal, Efficient Training`
- **示例**: `RAG, Agent, Multimodal, Efficient Training, LLM, Transformer`

**14. MAX_PAPERS**

- **Name**: `MAX_PAPERS`
- **Value**: 每天获取和分析的论文数量
- **默认值**: `6`
- **建议范围**: `5-10`

## 步骤 3: 配置示例

### 示例 1: 使用 Gmail + DeepSeek

```
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_RECEIVER=your_email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_SSL=false
SMTP_USE_TLS=true
KEYWORDS=RAG, Agent, Multimodal
MAX_PAPERS=6
```

### 示例 2: 使用 QQ 邮箱 + DeepSeek Reasoner

```
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-reasoner
INCLUDE_REASONING=true
EMAIL_SENDER=your_email@qq.com
EMAIL_PASSWORD=xxxxxxxxxxxxxxxx
EMAIL_RECEIVER=your_email@gmail.com
SMTP_SERVER=smtp.qq.com
SMTP_PORT=465
SMTP_USE_SSL=true
SMTP_USE_TLS=false
SMTP_TIMEOUT=60
KEYWORDS=RAG, Agent, Multimodal, Efficient Training
MAX_PAPERS=5
```

## 步骤 4: 验证配置

### 4.1 手动触发工作流

1. 进入仓库的 **Actions** 页面
2. 在左侧选择 **Daily Paper** workflow
3. 点击 **Run workflow** 按钮
4. 选择分支（通常是 `main`）
5. 点击 **Run workflow** 确认

### 4.2 查看运行日志

1. 点击运行中的工作流
2. 查看 **Run daily paper** 步骤的日志
3. 检查是否有错误

### 4.3 检查邮件

- 如果配置正确，你应该会收到邮件
- 如果邮件发送失败，检查日志中的错误信息
- 参考 [故障排查指南](TROUBLESHOOTING.md) 解决问题

## 步骤 5: 定时运行

工作流默认每天 UTC 时间 8:00（北京时间 16:00）运行。

### 修改运行时间

编辑 `.github/workflows/daily-paper.yml` 文件中的 cron 表达式：

```yaml
schedule:
  - cron: '0 8 * * *'  # UTC 时间 8:00
```

**Cron 表达式说明**：

- `0 8 * * *` = 每天 UTC 8:00
- `0 0 * * *` = 每天 UTC 0:00（北京时间 8:00）
- `0 16 * * *` = 每天 UTC 16:00（北京时间 0:00）

**时区转换**：

- UTC 8:00 = 北京时间 16:00
- UTC 0:00 = 北京时间 8:00

## 常见问题

### Q: Secrets 在哪里设置？

A: 仓库 Settings > Secrets and variables > Actions > New repository secret

### Q: 如何知道 Secrets 是否配置正确？

A: 手动触发一次工作流，查看日志输出。如果配置错误，会在日志中显示。

### Q: 可以同时配置多个邮箱吗？

A: 目前只支持一个接收邮箱。如果需要多个，可以修改代码或使用邮件转发。

### Q: 工作流运行失败怎么办？

A:

1. 查看 Actions 页面的错误日志
2. 检查 Secrets 是否全部配置
3. 参考 [故障排查指南](TROUBLESHOOTING.md)

### Q: 如何禁用定时运行？

A: 编辑 `.github/workflows/daily-paper.yml`，注释掉 `schedule` 部分：

```yaml
# schedule:
#   - cron: '0 8 * * *'
```

## 安全检查

⚠️ **重要提示**：

1. **不要将 Secrets 提交到代码仓库**
   - `.env` 文件已在 `.gitignore` 中
   - 只使用 GitHub Secrets 存储敏感信息

2. **定期更新 API Key**
   - 如果 API Key 泄露，立即重新生成

3. **使用应用专用密码**
   - 不要使用邮箱登录密码
   - Gmail 和 QQ 邮箱都需要生成应用专用密码

## 下一步

配置完成后：

1. ✅ 手动触发一次工作流测试
2. ✅ 检查是否收到邮件
3. ✅ 确认定时运行正常
4. ✅ 根据需要调整配置

如有问题，请查看 [故障排查指南](TROUBLESHOOTING.md)。
