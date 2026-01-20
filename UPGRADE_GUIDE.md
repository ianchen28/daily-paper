# Daily Paper 升级指南 (v0.1.0 → v0.2.0)

## 新功能概览

本次升级添加了三大核心功能：

1. **数据持久化** - 论文和分析结果自动保存到数据库
2. **交互式网页** - 每次推送后生成精美的可交互网页
3. **RAG-ready 架构** - 支持未来的语义搜索和 Agent 开发

---

## 新增功能详解

### 1. 数据持久化

#### 特性
- ✅ 自动保存论文元数据（标题、摘要、作者、关键词等）
- ✅ 存储 LLM 分析结果
- ✅ 记录每日报告生成历史
- ✅ 支持历史数据查询和统计
- ✅ **双数据库支持**：SQLite（默认）和 PostgreSQL

#### 数据库方案对比

| 特性 | SQLite (默认) | PostgreSQL (推荐) |
|------|-------------|------------------|
| 安装难度 | ⭐ 零配置，自动创建 | ⭐⭐ 需要安装 PostgreSQL |
| 适用场景 | 个人使用、小规模数据 | 生产环境、RAG Agent 开发 |
| 数据规模 | < 1万篇论文 | 1-100万篇论文 |
| 向量检索 | ⚠️ 需 numpy 模拟 | ✅ pgvector 原生支持 |
| 并发性能 | ⚠️ 写入串行 | ✅ 多用户并发 |
| 复杂查询 | ⚠️ 基础 SQL | ✅ 高级 SQL + JSONB |
| 全文搜索 | ✅ FTS5 | ✅ 更强大的 FTS |
| 备份方式 | 📁 单文件拷贝 | 💾 pg_dump |

#### 使用 SQLite（默认，推荐新手）

无需任何配置，运行程序即可自动创建 `daily_paper.db`：

```bash
uv run python main.py
```

数据文件位置：`./daily_paper.db`

#### 使用 PostgreSQL（推荐生产环境）

**步骤 1: 安装 PostgreSQL**

```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt install postgresql-15 postgresql-contrib-15
sudo systemctl start postgresql

# Windows
# 下载并安装: https://www.postgresql.org/download/windows/
```

**步骤 2: 创建数据库**

```bash
# 创建数据库
createdb daily_paper

# 或使用 psql
psql postgres
CREATE DATABASE daily_paper;
\q
```

**步骤 3: 安装 pgvector 扩展（可选，用于向量检索）**

```bash
# macOS
brew install pgvector

# Ubuntu/Debian
sudo apt install postgresql-15-pgvector

# 手动编译（如果包管理器没有）
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

**步骤 4: 安装 Python 依赖**

```bash
uv add psycopg2-binary
# 或
pip install psycopg2-binary
```

**步骤 5: 配置环境变量**

在 `.env` 文件中添加：

```env
DATABASE_URL=postgresql://username:password@localhost:5432/daily_paper
```

示例：
```env
# 本地开发
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/daily_paper

# 远程数据库
DATABASE_URL=postgresql://user:pass@db.example.com:5432/daily_paper

# Supabase
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:6543/postgres
```

**步骤 6: 首次运行会自动创建表和索引**

```bash
uv run python main.py
```

输出会显示：
```
📊 数据库类型: PostgreSQL
```

---

### 2. 交互式网页

#### 特性
- ✅ 精美的响应式设计（支持手机浏览）
- ✅ 实时搜索过滤（标题、关键词、作者）
- ✅ 多种排序方式（点赞数、GitHub Stars）
- ✅ 论文收藏功能（LocalStorage）
- ✅ 历史报告索引页
- ✅ 暗色模式支持

#### 生成的文件结构

```
web_reports/
├── index.html              # 历史报告索引页
├── report_2024-01-15.html  # 2024-01-15 的报告
├── report_2024-01-16.html  # 2024-01-16 的报告
└── ...
```

#### 使用方法

每次运行程序后，会自动生成网页：

```bash
uv run python main.py
```

输出：
```
🌐 生成交互式网页...
✅ 网页已生成: C:\path\to\web_reports\report_2024-01-15.html

🎉 完成！你可以访问以下网页查看报告:
  C:\path\to\web_reports\report_2024-01-15.html
  或访问索引页: C:\path\to\web_reports\index.html
```

直接在浏览器中打开 `web_reports/index.html` 即可查看所有历史报告。

#### 自定义网页输出目录

在 `.env` 中设置：

```env
WEB_OUTPUT_DIR=my_reports
```

---

### 3. RAG-ready 架构

虽然当前版本暂未启用向量检索，但数据库架构已为未来的 RAG Agent 做好准备：

#### 已实现
- ✅ PostgreSQL + pgvector 支持
- ✅ 向量字段预留（`embedding vector(1536)`）
- ✅ 向量索引优化（IVFFlat）
- ✅ 语义搜索 API（`db.semantic_search()`）
- ✅ 段落级存储表（`paper_chunks`）

#### 未来可扩展
- 📦 集成 Embedding 生成（OpenAI/Sentence Transformers）
- 📦 PDF 下载和解析
- 📦 图表识别和向量化
- 📦 多轮对话 Agent
- 📦 论文引用关系图谱

#### 快速尝试语义搜索（需 PostgreSQL + numpy）

```python
from daily_paper.database import Database

db = Database()

# 假设你有一个查询向量
query_vec = [0.1, 0.2, ...] * 1536  # 使用 OpenAI Embedding 生成

# 搜索相似论文
results = db.semantic_search(query_vec, limit=5, min_similarity=0.7)

for paper in results:
    print(f"{paper['title']} - 相似度: {paper['similarity']:.2f}")
```

---

## 数据库 Schema

### papers 表
存储论文基本信息

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL / INTEGER | 主键 |
| paper_id | TEXT | HuggingFace 论文 ID（唯一） |
| title | TEXT | 标题 |
| link | TEXT | 论文链接 |
| summary | TEXT | 摘要 |
| authors | JSONB / TEXT | 作者列表 |
| organization | TEXT | 机构 |
| published_at | TIMESTAMP / TEXT | 发布时间 |
| upvotes | INTEGER | 点赞数 |
| github_repo | TEXT | GitHub 仓库 |
| github_stars | INTEGER | Stars 数 |
| num_comments | INTEGER | 评论数 |
| keywords | JSONB / TEXT | 关键词列表 |
| raw_data | JSONB / TEXT | 原始数据 |
| created_at | TIMESTAMP | 创建时间 |

### analyses 表
存储 LLM 分析结果

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL / INTEGER | 主键 |
| paper_id | TEXT | 关联的论文 ID |
| analysis_html | TEXT | HTML 格式分析 |
| analysis_text | TEXT | 纯文本分析（用于 embedding） |
| model_name | TEXT | 使用的模型 |
| embedding | vector(1536) / BLOB | 文本向量（PostgreSQL 专用） |
| analyzed_at | TIMESTAMP | 分析时间 |

### reports 表
存储每日报告摘要

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL / INTEGER | 主键 |
| date | DATE / TEXT | 报告日期（唯一） |
| html_content | TEXT | 完整 HTML 报告 |
| paper_count | INTEGER | 论文数量 |
| web_page_path | TEXT | 生成的网页路径 |
| email_sent | BOOLEAN | 邮件是否发送成功 |
| created_at | TIMESTAMP | 创建时间 |
| metadata | JSONB / TEXT | 额外元数据 |

---

## API 使用示例

### 查询历史论文

```python
from daily_paper.database import Database

db = Database()

# 查询指定日期的论文
papers = db.get_papers_by_date_range("2024-01-15")
print(f"找到 {len(papers)} 篇论文")

for paper in papers:
    print(f"- {paper['title']}")
    print(f"  点赞: {paper['upvotes']}, Stars: {paper['github_stars']}")
```

### 搜索关键词

```python
# 搜索包含特定关键词的论文
results = db.search_papers("RAG", limit=10)

for paper in results:
    print(f"{paper['title']} - {paper['published_at']}")
```

### 获取统计信息

```python
stats = db.get_statistics()
print(f"总论文数: {stats['total_papers']}")
print(f"总报告数: {stats['total_reports']}")
print(f"已分析: {stats['analyzed_papers']}")
print(f"数据库类型: {stats['database_type']}")
```

---

## 迁移指南

### 从 v0.1.0 升级到 v0.2.0

**步骤 1: 更新代码**

```bash
git pull origin main
```

**步骤 2: 安装新依赖**

```bash
# 使用 SQLite（默认）
uv sync

# 或使用 PostgreSQL
uv sync --extra postgres
```

**步骤 3: 运行程序**

```bash
uv run python main.py
```

首次运行会自动：
- 创建数据库表
- 生成 `web_reports` 目录
- 保存当天的论文和分析结果

**步骤 4: 查看网页**

打开 `web_reports/index.html` 查看历史报告。

---

## 配置选项

### 新增环境变量

```env
# 数据库连接
DATABASE_URL=daily_paper.db              # SQLite (默认)
# DATABASE_URL=postgresql://...          # PostgreSQL

# 网页输出目录
WEB_OUTPUT_DIR=web_reports               # 默认值
```

---

## 常见问题

### Q: SQLite 和 PostgreSQL 如何选择？

**A:**
- **个人使用、初学者** → SQLite（零配置）
- **生产环境、团队协作、RAG Agent 开发** → PostgreSQL

### Q: 可以从 SQLite 迁移到 PostgreSQL 吗？

**A:** 可以，但需要手动导出导入数据。建议使用脚本：

```python
from daily_paper.database import Database

# 导出 SQLite 数据
sqlite_db = Database("daily_paper.db")
papers = sqlite_db.search_papers("", limit=10000)

# 导入到 PostgreSQL
pg_db = Database("postgresql://...")
for paper_data in papers:
    # 重构为 Paper 对象并保存
    pass
```

### Q: 向量检索功能如何启用？

**A:** 当前版本数据库架构已就绪，但向量生成功能待后续版本实现。你可以：

1. 使用 OpenAI Embedding API
2. 使用 Sentence Transformers（本地）
3. 等待官方集成（计划中）

### Q: 网页可以部署到服务器吗？

**A:** 可以！`web_reports` 目录下都是纯静态 HTML，可以直接部署到：
- GitHub Pages
- Vercel / Netlify
- Nginx / Apache
- 任何静态网站托管服务

### Q: 数据库文件在哪里？

**A:**
- SQLite: 项目根目录下的 `daily_paper.db`
- PostgreSQL: 取决于你的 PostgreSQL 配置

---

## 性能对比

### SQLite vs PostgreSQL

| 操作 | SQLite | PostgreSQL |
|------|--------|------------|
| 插入 1000 篇论文 | ~1s | ~0.5s |
| 关键词搜索 | ~50ms | ~10ms |
| 向量搜索（1万条） | ~2s (numpy) | ~50ms (pgvector) |
| 并发写入 | ⚠️ 锁等待 | ✅ 支持 |

---

## 下一步计划

- [ ] 自动生成 Embedding（OpenAI API）
- [ ] PDF 下载和解析
- [ ] 多模态内容提取（图表、公式）
- [ ] RAG Agent 示例
- [ ] Web UI 管理界面
- [ ] 论文推荐系统

---

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
