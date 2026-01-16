"""论文获取模块"""
import feedparser
from typing import List, Dict, Any
from .config import Config


class Paper:
    """论文对象，统一接口"""
    def __init__(self, title: str, link: str, summary: str):
        self.title = title
        self.link = link
        self.summary = summary


def _fetch_from_huggingface_api() -> List[Paper]:
    """从 HuggingFace API 获取论文"""
    import requests
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    # 尝试使用 HuggingFace Spaces API
    api_url = "https://huggingface.co/api/papers"
    try:
        print(f"  🔄 尝试使用 HuggingFace API: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=30)
        if response.status_code == 200:
            papers_data = response.json()
            papers = []
            for item in papers_data[:Config.MAX_PAPERS]:
                papers.append(Paper(
                    title=item.get('title', 'Untitled'),
                    link=item.get('url', ''),
                    summary=item.get('summary', '')
                ))
            return papers
    except Exception as e:
        print(f"  ⚠️ API 获取失败: {e}")
    
    return []


def _fetch_from_arxiv() -> List[Paper]:
    """从 arXiv RSS 获取论文（备选方案）"""
    import requests
    
    # arXiv 的 cs.AI 分类 RSS
    arxiv_url = "http://arxiv.org/rss/cs.AI"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        print(f"  🔄 尝试使用 arXiv RSS: {arxiv_url}")
        response = requests.get(arxiv_url, headers=headers, timeout=30)
        if response.status_code == 200:
            feed = feedparser.parse(response.text)
            papers = []
            for entry in feed.entries[:Config.MAX_PAPERS]:
                papers.append(Paper(
                    title=entry.get('title', 'Untitled'),
                    link=entry.get('link', ''),
                    summary=entry.get('summary', entry.get('description', ''))
                ))
            return papers
    except Exception as e:
        print(f"  ⚠️ arXiv 获取失败: {e}")
    
    return []


def get_papers() -> List[Paper]:
    """
    获取论文列表（支持多种来源）

    Returns:
        论文条目列表
    """
    import requests
    
    print(f"  🔗 正在访问: {Config.FEED_URL}")
    
    # 首先尝试从配置的 RSS URL 获取
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(Config.FEED_URL, headers=headers, timeout=30)
        
        # 检查是否是有效的 RSS/XML
        if response.status_code == 200 and ('xml' in response.headers.get('Content-Type', '') or 
                                            response.text.strip().startswith('<?xml') or
                                            response.text.strip().startswith('<rss')):
            feed = feedparser.parse(response.text)
            
            if feed.entries:
                papers = []
                for entry in feed.entries[:Config.MAX_PAPERS]:
                    papers.append(Paper(
                        title=entry.get('title', 'Untitled'),
                        link=entry.get('link', ''),
                        summary=entry.get('summary', entry.get('description', ''))
                    ))
                return papers
        else:
            print(f"  ⚠️ 返回的不是有效的 RSS feed，尝试备选方案...")
    except Exception as e:
        print(f"  ⚠️ RSS 获取失败: {e}，尝试备选方案...")
    
    # 如果 RSS 失败，尝试其他来源
    print(f"\n  🔄 尝试备选数据源...")
    
    # 尝试 HuggingFace API
    papers = _fetch_from_huggingface_api()
    if papers:
        return papers
    
    # 尝试 arXiv
    papers = _fetch_from_arxiv()
    if papers:
        return papers
    
    print(f"  ❌ 所有数据源都失败了")
    return []
