"""主程序入口"""
from .config import Config
from .paper_fetcher import get_papers
from .llm_analyzer import LLMAnalyzer
from .notifier import Notifier


def main() -> None:
    """主函数"""
    # 验证配置
    Config.validate()

    print(f"🚀 开始任务，使用模型: {Config.MODEL_NAME}")
    print(f"📡 RSS 源: {Config.FEED_URL}")

    # 初始化客户端和分析器
    analyzer = LLMAnalyzer()
    notifier = Notifier()

    # 获取论文
    print("\n📰 开始获取论文...")
    papers = get_papers()
    print(f"✅ 获取到 {len(papers)} 篇论文")

    if not papers:
        print("❌ 没有获取到论文，请检查 RSS 源是否可访问")
        return

    # 打印论文列表
    print("\n论文列表:")
    for i, paper in enumerate(papers, 1):
        print(f"  {i}. {paper.title}")
        print(f"     链接: {paper.link}")
        print(
            f"     摘要长度: {len(paper.summary) if hasattr(paper, 'summary') else 0} 字符"
        )

    # 生成 HTML 报告
    print("\n🤖 开始分析论文...")
    report_html = ""

    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] 正在分析: {paper.title}...")
        try:
            summary = analyzer.summarize(paper)
            print(f"  ✅ 分析完成，返回内容长度: {len(summary) if summary else 0} 字符")
            if summary:
                print(f"  内容预览: {summary[:100]}...")
                report_html += summary + "\n"
            else:
                print(f"  ⚠️ 返回内容为空")
        except Exception as e:
            print(f"  ❌ 分析出错: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n📊 报告统计:")
    print(f"  总论文数: {len(papers)}")
    print(f"  报告内容长度: {len(report_html)} 字符")

    # 发送邮件
    if report_html.strip():
        print("\n📧 开始发送邮件...")
        notifier.send_email(report_html)
        print("✅ 报告已发送！")
    else:
        print("\n⚠️ 没有生成报告内容")
        print("可能的原因:")
        print("  1. LLM API 调用失败")
        print("  2. LLM 返回空内容")
        print("  3. 论文数据获取失败")


if __name__ == "__main__":
    main()
