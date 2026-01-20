"""测试论文获取"""
import io
import sys

# 设置 UTF-8 编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from daily_paper.paper_fetcher import get_papers

# 测试几个日期
test_dates = ['2024-12-20', '2024-12-19', '2024-12-18']

for date in test_dates:
    print(f"\n测试日期: {date}")
    papers = get_papers(date)
    print(f"找到 {len(papers)} 篇论文")

    if papers:
        print("\n前3篇论文:")
        for i, paper in enumerate(papers[:3], 1):
            print(f"  {i}. {paper.title}")
            print(f"     👍 {paper.upvotes} | ⭐ {paper.github_stars} | 💬 {paper.num_comments}")
        break
