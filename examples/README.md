# 示例和测试工具

本目录包含各种测试脚本和实用工具。

## 文件说明

### 测试脚本

1. **test_fetch.py** - 测试论文获取功能
   ```bash
   uv run python examples/test_fetch.py
   ```
   功能：测试从 HuggingFace API 获取不同日期的论文

2. **test_db_web.py** - 测试数据库和网页生成（不调用 LLM）
   ```bash
   uv run python examples/test_db_web.py
   ```
   功能：测试数据库存储和网页生成，跳过 LLM 分析

3. **test_full.py** - 完整流程测试
   ```bash
   uv run python examples/test_full.py
   ```
   功能：测试完整的论文获取、分析、存储、网页生成流程

### 实用工具

4. **query_db.py** - 数据库查询工具
   ```bash
   uv run python examples/query_db.py
   ```
   功能：
   - 查看数据库统计信息
   - 查询历史报告
   - 按日期查询论文
   - 关键词搜索

5. **run.bat** (Windows) - 启动脚本
   ```cmd
   examples\run.bat
   ```
   功能：自动设置 UTF-8 编码并运行主程序

## 使用场景

### 测试新功能
```bash
# 测试论文获取
uv run python examples/test_fetch.py

# 测试数据库和网页（快速测试，不调用 LLM）
uv run python examples/test_db_web.py
```

### 查询历史数据
```bash
# 查看数据库内容
uv run python examples/query_db.py
```

### Windows 用户快速启动
```cmd
# 双击运行，或在命令行执行
examples\run.bat
```

## 注意事项

- 所有测试脚本都需要先配置 `.env` 文件
- `test_db_web.py` 不需要 LLM API 密钥，适合快速测试
- `test_full.py` 和 `run.bat` 需要完整的配置（包括 LLM API）
- 测试脚本会使用 2024-12-20 的历史数据（有论文的日期）

## 开发建议

在开发新功能时，可以：
1. 先运行 `test_fetch.py` 确认论文获取正常
2. 再运行 `test_db_web.py` 测试数据库和网页
3. 最后运行 `test_full.py` 测试完整流程
