"""查询数据库内容"""
import io
import sys

# 设置 UTF-8 编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from daily_paper.database import Database

db = Database()

print("=" * 60)
print("📊 数据库查询结果")
print("=" * 60)

# 1. 统计信息
print("\n1️⃣ 统计信息:")
stats = db.get_statistics()
for key, value in stats.items():
    print(f"   {key}: {value}")

# 2. 所有报告日期
print("\n2️⃣ 历史报告日期:")
dates = db.get_all_report_dates()
for date in dates:
    print(f"   📅 {date}")

# 3. 查询 2024-12-20 的论文
print("\n3️⃣ 2024-12-20 的论文:")
papers = db.get_papers_by_date_range("2024-12-20")
for i, paper in enumerate(papers, 1):
    print(f"\n   {i}. {paper['title']}")
    print(f"      Paper ID: {paper['paper_id']}")
    print(f"      点赞: {paper['upvotes']} | Stars: {paper['github_stars']}")
    if paper.get('analysis_html'):
        print(f"      有分析结果: ✅ ({len(paper['analysis_html'])} 字符)")

# 4. 查询报告信息
print("\n4️⃣ 报告信息:")
report = db.get_report("2024-12-20")
if report:
    print(f"   日期: {report['date']}")
    print(f"   论文数: {report['paper_count']}")
    print(f"   网页路径: {report['web_page_path']}")
    print(f"   邮件已发送: {report['email_sent']}")

# 5. 搜索关键词
print("\n5️⃣ 搜索 'Qwen' 关键词:")
results = db.search_papers("Qwen")
print(f"   找到 {len(results)} 篇相关论文")
for paper in results:
    print(f"   - {paper['title']}")

db.close()

print("\n" + "=" * 60)
print("✅ 查询完成！")
print("=" * 60)
