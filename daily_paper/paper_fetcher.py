"""论文获取模块"""
from typing import List, Optional
from datetime import datetime, timedelta
from .config import Config


class Paper:
    """论文对象，统一接口"""

    def __init__(
        self,
        title: str,
        link: str,
        summary: str,
        paper_id: Optional[str] = None,
        upvotes: int = 0,
        ai_summary: Optional[str] = None,
        ai_keywords: Optional[List[str]] = None,
        authors: Optional[List[str]] = None,
        github_repo: Optional[str] = None,
        github_stars: int = 0,
        num_comments: int = 0,
        published_at: Optional[str] = None,
        organization: Optional[str] = None,
        raw_data: Optional[dict] = None,
    ):
        self.title = title
        self.link = link
        self.summary = summary
        self.paper_id = paper_id
        self.upvotes = upvotes
        self.ai_summary = ai_summary
        self.ai_keywords = ai_keywords or []
        self.authors = authors or []
        self.github_repo = github_repo
        self.github_stars = github_stars
        self.num_comments = num_comments
        self.published_at = published_at
        self.organization = organization
        # 保留原始数据，以便后续使用
        self.raw_data = raw_data or {}


def _fetch_paper_detail(paper_id: str) -> str:
    """获取论文详情（用于补充摘要）"""
    import requests

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://huggingface.co/papers',
    }

    try:
        detail_url = f"https://huggingface.co/api/papers/{paper_id}"
        response = requests.get(detail_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('summary', data.get('description', ''))
    except Exception:
        pass

    return ''


def _fetch_from_huggingface_api(
        target_date: Optional[str] = None) -> List[Paper]:
    """
    从 HuggingFace Daily Papers API 获取论文
    
    Args:
        target_date: 日期字符串，格式 'YYYY-MM-DD'。如果不传，默认是昨天。
    
    Returns:
        论文列表
    """
    import requests

    # 使用正确的 Daily Papers API 端点
    api_url = "https://huggingface.co/api/daily_papers"

    # 完善 Headers，伪装成浏览器以绕过 Cloudflare
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://huggingface.co/papers',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # 构建查询参数
    params = {}
    if target_date:
        params['date'] = target_date
        print(f"  📅 获取日期: {target_date}")
    else:
        # 默认获取昨天的论文
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        params['date'] = yesterday
        print(f"  📅 获取日期: {yesterday} (昨天)")

    try:
        print(f"  🔄 使用 HuggingFace Daily Papers API: {api_url}")
        print(f"  📊 配置的 MAX_PAPERS: {Config.MAX_PAPERS}")
        response = requests.get(api_url,
                                headers=headers,
                                params=params,
                                timeout=30)

        if response.status_code == 200:
            papers_data = response.json()
            print(f"  📥 API 返回的论文总数: {len(papers_data)}")
            papers = []

            # 适配 API 返回的数据结构
            # 接口返回的是一个列表，每一项包含 'paper' 字典（优先使用），外层也有 title/summary（备用）
            # 根据配置限制处理数量
            papers_to_process = papers_data[:Config.MAX_PAPERS]
            print(
                f"  🔢 将处理前 {len(papers_to_process)} 篇论文（MAX_PAPERS={Config.MAX_PAPERS}）"
            )
            for item in papers_to_process:
                # 优先使用 paper 字段中的数据（更完整），如果没有则使用外层数据
                paper_info = item.get('paper', {})

                # 获取标题：优先使用 paper 字段，其次使用外层
                title = paper_info.get('title', '') or item.get(
                    'title', 'Untitled')

                # 获取论文 ID 并构造链接
                paper_id = paper_info.get('id') or item.get('id')
                if paper_id:
                    link = f"https://huggingface.co/papers/{paper_id}"
                else:
                    link = paper_info.get('url', '') or item.get('url', '')

                # 获取摘要：优先使用 paper 字段，其次使用外层，最后尝试获取详情
                summary = paper_info.get('summary', '') or item.get(
                    'summary', '')
                if not summary:
                    # 尝试从 description 获取
                    summary = paper_info.get('description', '') or item.get(
                        'description', '')
                    # 如果还是没有，尝试获取详情
                    if not summary and paper_id:
                        print(f"    📥 获取论文详情: {paper_id}")
                        summary = _fetch_paper_detail(paper_id)
                    if not summary:
                        summary = 'No summary provided by API.'

                # 提取作者信息
                authors_list = []
                if paper_info.get('authors'):
                    authors_list = [
                        author.get('name', '')
                        for author in paper_info.get('authors', [])
                        if author.get('name')
                    ]

                # 提取组织信息
                org_name = None
                if paper_info.get('organization'):
                    org_name = paper_info.get('organization', {}).get('fullname') or \
                              paper_info.get('organization', {}).get('name')
                elif item.get('organization'):
                    org_name = item.get('organization', {}).get('fullname') or \
                              item.get('organization', {}).get('name')

                # 提取其他有用信息
                upvotes = paper_info.get('upvotes', 0) or item.get(
                    'upvotes', 0)
                ai_summary = paper_info.get('ai_summary',
                                            '') or item.get('ai_summary')
                ai_keywords = paper_info.get('ai_keywords', []) or item.get(
                    'ai_keywords', [])
                github_repo = paper_info.get('githubRepo',
                                             '') or item.get('githubRepo')
                github_stars = paper_info.get('githubStars', 0) or item.get(
                    'githubStars', 0)
                num_comments = item.get('numComments', 0)
                published_at = paper_info.get('publishedAt',
                                              '') or item.get('publishedAt')

                papers.append(
                    Paper(
                        title=title,
                        link=link,
                        summary=summary,
                        paper_id=paper_id,
                        upvotes=upvotes,
                        ai_summary=ai_summary,
                        ai_keywords=ai_keywords,
                        authors=authors_list,
                        github_repo=github_repo,
                        github_stars=github_stars,
                        num_comments=num_comments,
                        published_at=published_at,
                        organization=org_name,
                        raw_data=item,  # 保留完整原始数据
                    ))

            if papers:
                print(f"  ✅ 成功从 HuggingFace 获取 {len(papers)} 篇论文")
            else:
                print(f"  ⚠️ 该日期没有论文")
            return papers
        else:
            print(f"  ⚠️ API 请求失败，状态码: {response.status_code}")
            if response.status_code == 403:
                print("  🔒 被 Cloudflare 拦截，建议检查 User-Agent 或尝试本地运行")
            elif response.status_code == 404:
                print("  ⚠️ API 端点不存在，可能 HuggingFace 已更改接口")

    except Exception as e:
        print(f"  ⚠️ API 获取失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    return []


def get_papers(target_date: Optional[str] = None) -> List[Paper]:
    """
    获取 HuggingFace Daily Papers 列表
    
    Args:
        target_date: 日期字符串，格式 'YYYY-MM-DD'。如果不传，默认是昨天。
    
    Returns:
        论文条目列表
    """
    return _fetch_from_huggingface_api(target_date)
