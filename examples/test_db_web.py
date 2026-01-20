"""测试数据库和网页生成（不调用LLM）"""
import io
import sys

# 设置 UTF-8 编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from daily_paper.config import Config
from daily_paper.database import Database
from daily_paper.paper_fetcher import get_papers
from daily_paper.web_generator import WebGenerator

print("🔍 测试数据库和网页生成功能（不调用 LLM）\n")

# 初始化组件
db = Database()
web_gen = WebGenerator()

print(f"📊 数据库类型: {db.get_statistics()['database_type']}\n")

# 获取论文
test_date = '2024-12-20'
print(f"📰 获取论文（日期: {test_date}）...")
papers = get_papers(test_date)
print(f"✅ 获取到 {len(papers)} 篇论文\n")

if not papers:
    print("❌ 没有论文数据，无法继续测试")
    sys.exit(1)

# 打印论文列表
print("论文列表:")
for i, paper in enumerate(papers, 1):
    print(f"  {i}. {paper.title}")
    print(f"     👍 {paper.upvotes} | ⭐ {paper.github_stars} | 💬 {paper.num_comments}")

# 保存论文到数据库
print("\n💾 保存论文到数据库...")
for paper in papers:
    try:
        db.save_paper(paper)
    except Exception as e:
        print(f"  ⚠️ 保存失败: {e}")

print("✅ 论文已保存到数据库")

# 准备论文数据（不包含 LLM 分析）
papers_data = []
for paper in papers:
    papers_data.append({
        "paper_id": paper.paper_id,
        "title": paper.title,
        "link": paper.link,
        "summary": paper.summary,
        "authors": paper.authors,
        "organization": paper.organization,
        "upvotes": paper.upvotes,
        "github_repo": paper.github_repo,
        "github_stars": paper.github_stars,
        "num_comments": paper.num_comments,
        "keywords": paper.ai_keywords,
        "published_at": paper.published_at,
        "analysis_html": f"<p><strong>摘要:</strong> {paper.summary}</p>"  # 使用摘要代替 LLM 分析
    })

# 生成简单的 HTML 报告
report_html = ""
for paper in papers:
    report_html += f"""
<div style="margin-bottom: 30px; padding: 20px; border: 1px solid #e1e8ed; border-radius: 8px;">
    <h3><a href="{paper.link}" target="_blank">{paper.title}</a></h3>
    <p><strong>点赞:</strong> {paper.upvotes} | <strong>Stars:</strong> {paper.github_stars} | <strong>评论:</strong> {paper.num_comments}</p>
    <p><strong>摘要:</strong> {paper.summary}</p>
    {f'<p><strong>关键词:</strong> {", ".join(paper.ai_keywords)}</p>' if paper.ai_keywords else ''}
</div>
"""

# 生成交互式网页
today = test_date
print("\n🌐 生成交互式网页...")
try:
    web_page_path = web_gen.generate_report_page(
        date=today,
        papers_data=papers_data,
        report_html=report_html,
        keywords=Config.KEYWORDS
    )
    print(f"✅ 网页已生成: {web_page_path}")
except Exception as e:
    print(f"  ❌ 网页生成失败: {e}")
    import traceback
    traceback.print_exc()
    web_page_path = None

# 保存报告到数据库
print("\n💾 保存报告到数据库...")
try:
    db.save_report(
        date=today,
        html_content=report_html,
        paper_count=len(papers),
        web_page_path=web_page_path,
        email_sent=False
    )
    print("✅ 报告已保存到数据库")
except Exception as e:
    print(f"  ❌ 保存报告失败: {e}")

# 显示统计信息
print("\n📈 数据库统计:")
stats = db.get_statistics()
for key, value in stats.items():
    print(f"  {key}: {value}")

# 关闭数据库
db.close()

# 最终提示
if web_page_path:
    print("\n🎉 测试完成！你可以访问以下网页查看报告:")
    print(f"  {web_page_path}")
    index_path = web_gen.output_dir / 'index.html'
    print(f"  或访问索引页: {index_path}")
    print("\n💡 提示：在浏览器中打开这些文件即可查看")
