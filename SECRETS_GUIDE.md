# GitHub Secrets 填写指南

## 📋 需要配置的 Secrets 清单

### 🔑 必需配置（必须填写，否则程序无法运行）

#### 1. LLM_API_KEY
- **Name**: `LLM_API_KEY`
- **Value**: 你的 LLM API Key
- **示例**: `sk-xxxxxxxxxxxxxxxxxxxxx`（DeepSeek API Key）
- **如何获取**:
  - DeepSeek: 访问 https://platform.deepseek.com/ 注册并获取 API Key
  - Gemini: 访问 https://aistudio.google.com/ 获取 API Key
  - OpenAI: 访问 https://platform.openai.com/ 获取 API Key

#### 2. EMAIL_SENDER
- **Name**: `EMAIL_SENDER`
- **Value**: 发件邮箱地址
- **示例**: 
  - `1516812461@qq.com`（QQ 邮箱）
  - `your_email@gmail.com`（Gmail）
- **注意**: 填写完整的邮箱地址，不要有空格

#### 3. EMAIL_PASSWORD
- **Name**: `EMAIL_PASSWORD`
- **Value**: 邮箱授权码（**不是登录密码**）
- **示例**: `goffxobxgetgfiii`（16位授权码）
- **如何获取**:
  - **QQ 邮箱**:
    1. 登录 QQ 邮箱 → 设置 → 账户
    2. 开启 POP3/SMTP 服务
    3. 生成授权码（16位）
    4. 复制授权码，填入此处
  - **Gmail**:
    1. 访问 Google 账号设置
    2. 安全 → 两步验证（需先启用）
    3. 应用专用密码 → 生成新密码
    4. 复制 16 位密码，填入此处
- **⚠️ 重要**: 必须使用授权码，不能使用邮箱登录密码

#### 4. EMAIL_RECEIVER
- **Name**: `EMAIL_RECEIVER`
- **Value**: 接收邮件的邮箱地址
- **示例**: `ianchen289@gmail.com`
- **注意**: 可以填写与发件邮箱相同的地址

---

### ⚙️ 可选配置（如果不填写，会使用默认值）

#### 5. SMTP_SERVER
- **Name**: `SMTP_SERVER`
- **Value**: SMTP 服务器地址
- **默认值**: `smtp.gmail.com`（如果不填写）
- **示例**:
  - QQ 邮箱: `smtp.qq.com`
  - Gmail: `smtp.gmail.com`
  - Outlook: `smtp-mail.outlook.com`

#### 6. SMTP_PORT
- **Name**: `SMTP_PORT`
- **Value**: SMTP 端口号
- **默认值**: `587`（如果不填写）
- **示例**:
  - QQ 邮箱 SSL: `465`
  - QQ 邮箱 TLS: `587`
  - Gmail TLS: `587`

#### 7. SMTP_USE_SSL
- **Name**: `SMTP_USE_SSL`
- **Value**: 是否使用 SSL
- **默认值**: `false`（如果不填写）
- **示例**:
  - QQ 邮箱（465端口）: `true`
  - Gmail（587端口）: `false`（或不填写）

#### 8. SMTP_USE_TLS
- **Name**: `SMTP_USE_TLS`
- **Value**: 是否使用 TLS
- **默认值**: `true`（如果不填写）
- **示例**:
  - Gmail（587端口）: `true`（或不填写）
  - QQ 邮箱（465端口）: `false`

#### 9. SMTP_TIMEOUT
- **Name**: `SMTP_TIMEOUT`
- **Value**: 连接超时时间（秒）
- **默认值**: `30`（如果不填写）
- **示例**: `60`（如果网络较慢，可以增加）

#### 10. LLM_BASE_URL
- **Name**: `LLM_BASE_URL`
- **Value**: LLM API 地址
- **默认值**: 如果不填写，DeepSeek 使用默认地址
- **示例**:
  - DeepSeek: `https://api.deepseek.com`
  - Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - OpenAI: `https://api.openai.com/v1`

#### 11. MODEL_NAME
- **Name**: `MODEL_NAME`
- **Value**: 模型名称
- **默认值**: `deepseek-chat`（如果不填写）
- **示例**:
  - DeepSeek: `deepseek-chat` 或 `deepseek-reasoner`
  - Gemini: `gemini-1.5-flash`
  - OpenAI: `gpt-3.5-turbo`

#### 12. INCLUDE_REASONING
- **Name**: `INCLUDE_REASONING`
- **Value**: 是否包含推理过程
- **默认值**: `false`（如果不填写）
- **示例**: `true`（仅对 `deepseek-reasoner` 有效）

#### 13. KEYWORDS
- **Name**: `KEYWORDS`
- **Value**: 关注的关键词（用逗号分隔）
- **默认值**: `RAG, Agent, Multimodal, Efficient Training`（如果不填写）
- **示例**: `RAG, Agent, Multimodal, Efficient Training, LLM, Transformer`
- **注意**: 不要有引号，直接填写关键词

#### 14. MAX_PAPERS
- **Name**: `MAX_PAPERS`
- **Value**: 每天获取的论文数量
- **默认值**: `6`（如果不填写）
- **示例**: `5`、`8`、`10`
- **建议**: 5-10 篇

---

## 📝 配置示例

### 示例 1: QQ 邮箱 + DeepSeek（推荐配置）

```
必需配置：
LLM_API_KEY = sk-xxxxxxxxxxxxxxxxxxxxx
EMAIL_SENDER = 1516812461@qq.com
EMAIL_PASSWORD = goffxobxgetgfiii
EMAIL_RECEIVER = ianchen289@gmail.com

推荐配置：
SMTP_SERVER = smtp.qq.com
SMTP_PORT = 465
SMTP_USE_SSL = true
SMTP_USE_TLS = false
MODEL_NAME = deepseek-chat
KEYWORDS = RAG, Agent, Multimodal, Efficient Training
MAX_PAPERS = 6
```

### 示例 2: Gmail + DeepSeek Reasoner

```
必需配置：
LLM_API_KEY = sk-xxxxxxxxxxxxxxxxxxxxx
EMAIL_SENDER = your_email@gmail.com
EMAIL_PASSWORD = xxxx xxxx xxxx xxxx
EMAIL_RECEIVER = your_email@gmail.com

推荐配置：
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SMTP_USE_SSL = false
SMTP_USE_TLS = true
MODEL_NAME = deepseek-reasoner
INCLUDE_REASONING = true
KEYWORDS = RAG, Agent, Multimodal
MAX_PAPERS = 5
```

---

## 🔧 如何填写 Secrets

### 步骤 1: 进入 Secrets 页面

1. 打开你的 GitHub 仓库
2. 点击 **Settings**（设置）
3. 左侧菜单：**Secrets and variables** > **Actions**
4. 点击 **New repository secret**（新建仓库密钥）

### 步骤 2: 填写 Secret

1. **Name**（名称）: 输入 secret 的名称（如 `LLM_API_KEY`）
2. **Value**（值）: 输入对应的值
3. 点击 **Update secret**（更新密钥）

### 步骤 3: 重复添加

按照上面的清单，逐个添加所有需要的 secrets。

---

## ⚠️ 注意事项

### 1. 不要有空格
- ✅ 正确: `smtp.qq.com`
- ❌ 错误: ` smtp.qq.com `（前后有空格）

### 2. 不要有引号
- ✅ 正确: `RAG, Agent, Multimodal`
- ❌ 错误: `"RAG, Agent, Multimodal"`（不要引号）

### 3. 布尔值填写
- ✅ 正确: `true` 或 `false`（小写）
- ❌ 错误: `True`、`TRUE`、`1`、`yes`

### 4. 数字填写
- ✅ 正确: `465`、`587`、`6`
- ❌ 错误: `"465"`（不要引号）

### 5. 授权码 vs 密码
- ✅ 使用: 授权码（16位）
- ❌ 不要: 邮箱登录密码

---

## ✅ 配置检查清单

完成配置后，检查以下项目：

- [ ] LLM_API_KEY 已填写
- [ ] EMAIL_SENDER 已填写（完整邮箱地址）
- [ ] EMAIL_PASSWORD 已填写（授权码，不是登录密码）
- [ ] EMAIL_RECEIVER 已填写（完整邮箱地址）
- [ ] SMTP_SERVER 已填写（如果使用 QQ 邮箱）
- [ ] SMTP_PORT 已填写（如果使用 QQ 邮箱 465 端口）
- [ ] SMTP_USE_SSL 已填写（如果使用 QQ 邮箱）
- [ ] SMTP_USE_TLS 已填写（如果使用 QQ 邮箱）
- [ ] 所有值都没有多余的空格
- [ ] 所有值都没有引号

---

## 🧪 测试配置

配置完成后：

1. 进入 **Actions** 页面
2. 选择 **Daily Paper** workflow
3. 点击 **Run workflow** 手动触发
4. 查看运行日志，确认配置正确

如果看到错误，检查：
- Secrets 名称是否正确（区分大小写）
- 值是否正确（没有空格、引号）
- 必需配置是否都已填写

---

## 📚 相关文档

- [快速配置清单](QUICK_START.md)
- [详细配置指南](GITHUB_ACTIONS_SETUP.md)
- [故障排查](TROUBLESHOOTING.md)
