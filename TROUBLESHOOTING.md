# 故障排查指南

## 邮件发送问题

### 问题：连接超时 (TimeoutError)

**症状**：
```
❌ 邮件发送失败: 连接超时（30秒）
```

**解决方案**：

#### 1. 增加超时时间

在 `.env` 文件中添加或修改：
```bash
SMTP_TIMEOUT=60
```

#### 2. 检查网络连接

测试 SMTP 服务器是否可达：
```bash
# macOS/Linux
telnet smtp.gmail.com 587

# 或者使用 nc (netcat)
nc -zv smtp.gmail.com 587
```

如果无法连接，可能是：
- 网络防火墙阻止
- 需要配置代理
- ISP 阻止了 SMTP 端口

#### 3. 检查防火墙/代理设置

- **macOS**: 系统设置 > 网络 > 防火墙
- **Linux**: 检查 `iptables` 或 `ufw`
- **公司网络**: 可能需要配置代理或使用 VPN

#### 4. 验证 SMTP 配置

确保 `.env` 中的配置正确：
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**其他邮箱的 SMTP 设置**：
- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **QQ 邮箱**: `smtp.qq.com:587` 或 `smtp.qq.com:465` (SSL)
- **163 邮箱**: `smtp.163.com:25` 或 `smtp.163.com:465` (SSL)

#### 5. 使用备用端口

如果 587 端口被阻止，可以尝试：
- **Gmail SSL**: `smtp.gmail.com:465` (需要修改代码使用 `SMTP_SSL`)
- **Gmail TLS**: `smtp.gmail.com:587` (当前使用的)

#### 6. 检查 Gmail 应用密码

确保：
1. 已启用两步验证
2. 生成了应用专用密码（不是登录密码）
3. 密码格式正确（16位，可能有空格）

#### 7. 临时解决方案

如果邮件发送持续失败，程序会自动保存报告到 HTML 文件：
- 文件名格式：`daily_paper_report_YYYYMMDD_HHMMSS.html`
- 可以在浏览器中打开查看
- 可以手动转发或分享

---

### 问题：认证失败 (SMTPAuthenticationError)

**症状**：
```
❌ 邮件发送失败: 认证失败
```

**解决方案**：

1. **检查应用专用密码**
   - 确保使用的是应用专用密码，不是 Gmail 登录密码
   - 重新生成应用专用密码

2. **验证邮箱地址**
   - 确保 `EMAIL_SENDER` 和 `EMAIL_RECEIVER` 格式正确
   - 确保邮箱地址没有多余空格

3. **检查两步验证**
   - 必须启用两步验证才能使用应用专用密码

---

### 问题：无法连接到 SMTP 服务器 (SMTPConnectError)

**症状**：
```
❌ 邮件发送失败: 无法连接到 SMTP 服务器
```

**解决方案**：

1. **检查服务器地址**
   ```bash
   # 测试 DNS 解析
   nslookup smtp.gmail.com
   ```

2. **检查端口**
   - Gmail: 587 (TLS) 或 465 (SSL)
   - 确保端口没有被防火墙阻止

3. **尝试其他邮箱服务**
   - 如果 Gmail 无法连接，可以尝试其他邮箱服务商

---

## 其他常见问题

### LLM API 调用失败

**检查项**：
1. API Key 是否正确
2. API 余额是否充足
3. 网络连接是否正常
4. 模型名称是否正确

### 论文获取失败

**检查项**：
1. 网络连接是否正常
2. HuggingFace API 是否可访问
3. 日期参数是否正确（默认获取昨天的论文）

### 报告内容为空

**可能原因**：
1. LLM 返回空内容
2. 论文数据获取失败
3. 所有论文分析都失败

**解决方案**：
- 检查 LLM API 配置
- 查看日志中的错误信息
- 尝试手动运行测试脚本

---

## 调试技巧

### 1. 启用详细日志

程序已经包含详细的日志输出，注意观察：
- 📧 连接 SMTP 服务器的步骤
- ✅ 每个步骤的成功/失败状态
- ❌ 错误信息和排查建议

### 2. 测试单个组件

```bash
# 测试论文获取
uv run python test_paper_fetcher.py

# 测试 LLM 分析（需要配置 API Key）
uv run python -c "from daily_paper.llm_analyzer import LLMAnalyzer; ..."

# 测试邮件发送（需要配置邮件信息）
```

### 3. 查看生成的报告

即使邮件发送失败，报告也会保存到 HTML 文件：
```bash
# 查看最新报告
ls -lt daily_paper_report_*.html | head -1

# 在浏览器中打开
open daily_paper_report_*.html  # macOS
xdg-open daily_paper_report_*.html  # Linux
```

---

## 获取帮助

如果问题仍然存在：
1. 检查 `.env` 配置文件
2. 查看程序输出的详细错误信息
3. 检查网络连接和防火墙设置
4. 查看生成的 HTML 报告文件确认内容是否正确
