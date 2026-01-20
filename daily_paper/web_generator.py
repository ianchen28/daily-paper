"""Interactive web page generator for daily paper reports."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class WebGenerator:
    """Generate interactive static web pages for paper reports."""

    def __init__(self, output_dir: str = "web_reports"):
        """Initialize web generator.

        Args:
            output_dir: Directory to save generated web pages
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_report_page(
        self,
        date: str,
        papers_data: List[Dict],
        report_html: str,
        keywords: Optional[str] = None
    ) -> str:
        """Generate interactive report page for a specific date.

        Args:
            date: Report date (YYYY-MM-DD)
            papers_data: List of paper dicts with metadata
            report_html: Analysis HTML content
            keywords: User's focus keywords

        Returns:
            Path to generated HTML file
        """
        # Prepare papers data for JavaScript
        papers_json = []
        for paper in papers_data:
            papers_json.append({
                "paper_id": paper.get("paper_id", ""),
                "title": paper.get("title", ""),
                "link": paper.get("link", ""),
                "summary": paper.get("summary", ""),
                "authors": paper.get("authors", []) if isinstance(paper.get("authors"), list)
                          else json.loads(paper.get("authors", "[]")),
                "organization": paper.get("organization", ""),
                "upvotes": paper.get("upvotes", 0),
                "github_repo": paper.get("github_repo", ""),
                "github_stars": paper.get("github_stars", 0),
                "num_comments": paper.get("num_comments", 0),
                "keywords": paper.get("keywords", []) if isinstance(paper.get("keywords"), list)
                           else json.loads(paper.get("keywords", "[]")),
                "published_at": paper.get("published_at", ""),
                "analysis_html": paper.get("analysis_html", "")
            })

        html_content = self._generate_html_template(
            date=date,
            papers_data=papers_json,
            report_html=report_html,
            keywords=keywords
        )

        # Save to file
        file_path = self.output_dir / f"report_{date}.html"
        file_path.write_text(html_content, encoding="utf-8")

        # Update index page
        self._update_index_page()

        return str(file_path)

    def _generate_html_template(
        self,
        date: str,
        papers_data: List[Dict],
        report_html: str,
        keywords: Optional[str]
    ) -> str:
        """Generate full HTML page with interactive features.

        Args:
            date: Report date
            papers_data: Papers metadata as JSON-serializable dicts
            report_html: Analysis HTML content
            keywords: Focus keywords

        Returns:
            Complete HTML string
        """
        papers_json_str = json.dumps(papers_data, ensure_ascii=False, indent=2)

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="HuggingFace Daily Papers - {date}">
    <title>Daily Papers - {date}</title>
    <style>
        :root {{
            --primary-color: #3498db;
            --secondary-color: #2c3e50;
            --background-color: #f5f7fa;
            --card-background: #ffffff;
            --text-color: #333333;
            --border-color: #e1e8ed;
            --hover-color: #ecf0f1;
            --success-color: #27ae60;
            --info-color: #3498db;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}

        header .meta {{
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .controls {{
            background: var(--card-background);
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .controls-row {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .search-box {{
            flex: 1;
            min-width: 250px;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 15px;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: var(--primary-color);
        }}

        .filter-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 0.95em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }}

        .btn-primary {{
            background-color: var(--primary-color);
            color: white;
        }}

        .btn-primary:hover {{
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}

        .btn-secondary {{
            background-color: var(--hover-color);
            color: var(--text-color);
        }}

        .btn-secondary:hover {{
            background-color: var(--border-color);
        }}

        .btn.active {{
            background-color: var(--success-color);
            color: white;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}

        .stat-item {{
            background: var(--background-color);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9em;
        }}

        .stat-item strong {{
            color: var(--primary-color);
            margin-right: 5px;
        }}

        .papers-grid {{
            display: grid;
            gap: 25px;
        }}

        .paper-card {{
            background: var(--card-background);
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s;
            border-left: 4px solid var(--primary-color);
        }}

        .paper-card:hover {{
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            transform: translateY(-3px);
        }}

        .paper-card.hidden {{
            display: none;
        }}

        .paper-header {{
            margin-bottom: 15px;
        }}

        .paper-title {{
            font-size: 1.4em;
            color: var(--secondary-color);
            margin-bottom: 10px;
            line-height: 1.3;
        }}

        .paper-title a {{
            color: var(--secondary-color);
            text-decoration: none;
            transition: color 0.3s;
        }}

        .paper-title a:hover {{
            color: var(--primary-color);
        }}

        .paper-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            font-size: 0.85em;
            color: #666;
            margin-bottom: 15px;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .meta-icon {{
            font-size: 1.1em;
        }}

        .paper-tags {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }}

        .tag {{
            padding: 4px 12px;
            background-color: var(--background-color);
            color: var(--text-color);
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
        }}

        .tag.highlight {{
            background-color: var(--primary-color);
            color: white;
        }}

        .paper-summary {{
            color: #555;
            line-height: 1.7;
            margin-bottom: 15px;
        }}

        .paper-analysis {{
            border-top: 2px dashed var(--border-color);
            padding-top: 15px;
            margin-top: 15px;
        }}

        .analysis-title {{
            font-size: 1.1em;
            color: var(--secondary-color);
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .paper-actions {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}

        .action-btn {{
            padding: 8px 15px;
            border: 1px solid var(--border-color);
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9em;
        }}

        .action-btn:hover {{
            background-color: var(--hover-color);
        }}

        .action-btn.bookmarked {{
            background-color: #fff3cd;
            border-color: #ffc107;
        }}

        footer {{
            text-align: center;
            padding: 30px 20px;
            color: #666;
            font-size: 0.9em;
            margin-top: 50px;
        }}

        footer a {{
            color: var(--primary-color);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.5em;
            }}

            .controls-row {{
                flex-direction: column;
            }}

            .paper-title {{
                font-size: 1.2em;
            }}

            .paper-meta {{
                flex-direction: column;
                gap: 8px;
            }}
        }}

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --background-color: #1a1a1a;
                --card-background: #2d2d2d;
                --text-color: #e0e0e0;
                --border-color: #444;
                --hover-color: #3a3a3a;
                --secondary-color: #b8c5d0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 HuggingFace Daily Papers</h1>
            <div class="meta">
                <div>日期: <strong>{date}</strong></div>
                {f'<div>关注领域: <strong>{keywords}</strong></div>' if keywords else ''}
            </div>
        </header>

        <div class="controls">
            <div class="controls-row">
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="🔍 搜索论文标题、关键词、作者...">
                </div>
                <div class="filter-group">
                    <button class="btn btn-secondary" onclick="sortPapers('upvotes')">按点赞排序</button>
                    <button class="btn btn-secondary" onclick="sortPapers('stars')">按 Stars 排序</button>
                    <button class="btn btn-secondary" onclick="sortPapers('default')">默认排序</button>
                    <button class="btn btn-primary" onclick="window.location.href='index.html'">查看历史</button>
                </div>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <strong id="totalPapers">{len(papers_data)}</strong> 篇论文
                </div>
                <div class="stat-item">
                    <strong id="visiblePapers">{len(papers_data)}</strong> 篇显示
                </div>
                <div class="stat-item">
                    <strong id="bookmarkedCount">0</strong> 篇已收藏
                </div>
            </div>
        </div>

        <div class="papers-grid" id="papersGrid">
            <!-- Papers will be rendered here by JavaScript -->
        </div>

        <footer>
            <p>由 Daily Paper Bot 自动生成 | <a href="https://github.com/huggingface/daily_papers" target="_blank">HuggingFace Daily Papers</a></p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>

    <script>
        // Papers data
        const papersData = {papers_json_str};

        // Local storage keys
        const BOOKMARKS_KEY = 'daily_papers_bookmarks';
        const NOTES_KEY = 'daily_papers_notes';

        // Load bookmarks and notes from localStorage
        let bookmarks = new Set(JSON.parse(localStorage.getItem(BOOKMARKS_KEY) || '[]'));
        let notes = JSON.parse(localStorage.getItem(NOTES_KEY) || '{{}}');

        // Render papers
        function renderPapers(papers) {{
            const grid = document.getElementById('papersGrid');
            grid.innerHTML = papers.map(paper => `
                <div class="paper-card" data-paper-id="${{paper.paper_id}}">
                    <div class="paper-header">
                        <h2 class="paper-title">
                            <a href="${{paper.link}}" target="_blank">${{paper.title}}</a>
                        </h2>
                        <div class="paper-meta">
                            <div class="meta-item">
                                <span class="meta-icon">👍</span>
                                <span>${{paper.upvotes}} 点赞</span>
                            </div>
                            ${{paper.github_stars > 0 ? `
                                <div class="meta-item">
                                    <span class="meta-icon">⭐</span>
                                    <span>${{paper.github_stars}} Stars</span>
                                </div>
                            ` : ''}}
                            <div class="meta-item">
                                <span class="meta-icon">💬</span>
                                <span>${{paper.num_comments}} 评论</span>
                            </div>
                            ${{paper.organization ? `
                                <div class="meta-item">
                                    <span class="meta-icon">🏢</span>
                                    <span>${{paper.organization}}</span>
                                </div>
                            ` : ''}}
                        </div>
                        <div class="paper-tags">
                            ${{paper.keywords.map(kw => `<span class="tag">${{kw}}</span>`).join('')}}
                        </div>
                    </div>
                    <div class="paper-summary">
                        ${{paper.summary || '暂无摘要'}}
                    </div>
                    ${{paper.analysis_html ? `
                        <div class="paper-analysis">
                            <div class="analysis-title">🤖 AI 分析</div>
                            ${{paper.analysis_html}}
                        </div>
                    ` : ''}}
                    <div class="paper-actions">
                        <button class="action-btn bookmark-btn ${{bookmarks.has(paper.paper_id) ? 'bookmarked' : ''}}"
                                onclick="toggleBookmark('${{paper.paper_id}}')">
                            ${{bookmarks.has(paper.paper_id) ? '⭐ 已收藏' : '☆ 收藏'}}
                        </button>
                        ${{paper.github_repo ? `
                            <button class="action-btn" onclick="window.open('${{paper.github_repo}}', '_blank')">
                                📦 查看代码
                            </button>
                        ` : ''}}
                    </div>
                </div>
            `).join('');

            updateStats();
        }}

        // Search functionality
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.paper-card');

            cards.forEach(card => {{
                const paperId = card.dataset.paperId;
                const paper = papersData.find(p => p.paper_id === paperId);

                if (!paper) {{
                    card.classList.add('hidden');
                    return;
                }}

                const searchText = [
                    paper.title,
                    paper.summary,
                    paper.authors.join(' '),
                    paper.keywords.join(' '),
                    paper.organization
                ].join(' ').toLowerCase();

                if (searchText.includes(query)) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            updateStats();
        }});

        // Sort functionality
        function sortPapers(sortBy) {{
            let sorted = [...papersData];

            if (sortBy === 'upvotes') {{
                sorted.sort((a, b) => b.upvotes - a.upvotes);
            }} else if (sortBy === 'stars') {{
                sorted.sort((a, b) => b.github_stars - a.github_stars);
            }}

            renderPapers(sorted);
        }}

        // Bookmark functionality
        function toggleBookmark(paperId) {{
            if (bookmarks.has(paperId)) {{
                bookmarks.delete(paperId);
            }} else {{
                bookmarks.add(paperId);
            }}

            localStorage.setItem(BOOKMARKS_KEY, JSON.stringify([...bookmarks]));
            renderPapers(papersData);
        }}

        // Update statistics
        function updateStats() {{
            const visibleCards = document.querySelectorAll('.paper-card:not(.hidden)');
            document.getElementById('visiblePapers').textContent = visibleCards.length;
            document.getElementById('bookmarkedCount').textContent = bookmarks.size;
        }}

        // Initial render
        renderPapers(papersData);
    </script>
</body>
</html>
"""

    def _update_index_page(self) -> None:
        """Update or create index page listing all reports."""
        # Get all report files
        report_files = sorted(
            self.output_dir.glob("report_*.html"),
            reverse=True
        )

        # Extract dates from filenames
        reports = []
        for file in report_files:
            date_str = file.stem.replace("report_", "")
            reports.append({
                "date": date_str,
                "file": file.name
            })

        index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Papers - 历史报告</title>
    <style>
        :root {{
            --primary-color: #3498db;
            --secondary-color: #2c3e50;
            --background-color: #f5f7fa;
            --card-background: #ffffff;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--background-color);
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .reports-list {{
            display: grid;
            gap: 15px;
        }}

        .report-item {{
            background: var(--card-background);
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s;
            border-left: 4px solid var(--primary-color);
        }}

        .report-item:hover {{
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            transform: translateX(5px);
        }}

        .report-item a {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-decoration: none;
            color: var(--secondary-color);
        }}

        .report-date {{
            font-size: 1.3em;
            font-weight: 600;
        }}

        .report-arrow {{
            font-size: 1.5em;
            color: var(--primary-color);
        }}

        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }}

        .empty-state p {{
            font-size: 1.2em;
            margin-bottom: 10px;
        }}

        footer {{
            text-align: center;
            padding: 30px 20px;
            color: #666;
            font-size: 0.9em;
            margin-top: 50px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Daily Papers 历史报告</h1>
            <p>查看往期的论文分析报告</p>
        </header>

        <div class="reports-list">
            {self._generate_report_list_html(reports)}
        </div>

        <footer>
            <p>由 Daily Paper Bot 自动生成 | 共 <strong>{len(reports)}</strong> 份报告</p>
        </footer>
    </div>
</body>
</html>
"""

        index_path = self.output_dir / "index.html"
        index_path.write_text(index_html, encoding="utf-8")

    def _generate_report_list_html(self, reports: List[Dict]) -> str:
        """Generate HTML for report list.

        Args:
            reports: List of report dicts with date and file

        Returns:
            HTML string
        """
        if not reports:
            return """
                <div class="empty-state">
                    <p>暂无报告</p>
                    <p style="font-size: 0.9em; color: #999;">报告将在首次运行后生成</p>
                </div>
            """

        return "\n".join([
            f'''
            <div class="report-item">
                <a href="{report['file']}">
                    <span class="report-date">📅 {report['date']}</span>
                    <span class="report-arrow">→</span>
                </a>
            </div>
            '''
            for report in reports
        ])

    def get_output_path(self, date: str) -> str:
        """Get output path for a specific date.

        Args:
            date: Report date (YYYY-MM-DD)

        Returns:
            Absolute path to HTML file
        """
        return str((self.output_dir / f"report_{date}.html").absolute())
