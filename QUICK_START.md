# 快速配置清单

## 第一步：推送代码

```bash
git push origin main
```

## 第二步：配置 GitHub Secrets

访问：`https://github.com/你的用户名/你的仓库名/settings/secrets/actions`

点击 **New repository secret**，按顺序添加：

### 🔑 必需配置（4个）

1. **LLM_API_KEY**
   - 值：你的 LLM API Key（如 DeepSeek API Key）

2. **EMAIL_SENDER**
   - 值：发件邮箱（如 `your_email@qq.com`）

3. **EMAIL_PASSWORD**
   - 值：邮箱授权码（**不是登录密码**）
   - Gmail: 应用专用密码（16位）
   - QQ 邮箱: 授权码（16位）

4. **EMAIL_RECEIVER**
   - 值：接收邮箱（如 `your_email@gmail.com`）

### ⚙️ 推荐配置（根据你的情况选择）

5. **SMTP_SERVER**
   - Gmail: `smtp.gmail.com`
   - QQ 邮箱: `smtp.qq.com`

6. **SMTP_PORT**
   - Gmail: `587`
   - QQ 邮箱: `465`（SSL）或 `587`（TLS）

7. **SMTP_USE_SSL**
   - QQ 邮箱（465端口）: `true`
   - Gmail（587端口）: `false`

8. **SMTP_USE_TLS**
   - Gmail（587端口）: `true`
   - QQ 邮箱（465端口）: `false`

9. **MODEL_NAME**
   - DeepSeek: `deepseek-chat` 或 `deepseek-reasoner`
   - 默认: `deepseek-chat`

10. **KEYWORDS**
    - 值：`RAG, Agent, Multimodal, Efficient Training`
    - 根据你的关注领域修改

11. **MAX_PAPERS**
    - 值：`6`（建议 5-10）

## 第三步：测试运行

1. 进入仓库的 **Actions** 页面
2. 选择 **Daily Paper** workflow
3. 点击 **Run workflow** 手动触发
4. 查看运行日志，确认成功

## 第四步：验证邮件

- 检查收件箱（可能需要等待几分钟）
- 检查垃圾邮件文件夹
- 检查"所有邮件"标签（Gmail）

## 完成！

工作流将每天自动运行（默认 UTC 8:00，北京时间 16:00）

---

📖 详细配置说明请查看 [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)
