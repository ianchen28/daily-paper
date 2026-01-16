"""LLM 分析模块"""
from openai import OpenAI
from typing import Any, Optional
from .config import Config


class LLMAnalyzer:
    """LLM 分析器"""

    def __init__(self):
        """初始化 LLM 客户端"""
        # 如果指定了 base_url 则使用，否则使用默认（OpenAI 兼容）
        if Config.LLM_BASE_URL:
            self.client = OpenAI(api_key=Config.LLM_API_KEY, base_url=Config.LLM_BASE_URL)
        else:
            # 如果没有指定 base_url，使用默认的 OpenAI API
            self.client = OpenAI(api_key=Config.LLM_API_KEY)

    def summarize(self, paper: Any) -> str:
        """
        使用 LLM 生成论文摘要（HTML 格式）

        Args:
            paper: 论文对象（包含 title, link, summary 属性）

        Returns:
            HTML 格式的分析结果
        """
        prompt = f"""
请作为一名学术助理，阅读这篇论文摘要。

Title: {paper.title}
Abstract: {paper.summary}
User Interests: {Config.KEYWORDS}

请用中文输出一段简短的 HTML 代码片段（不要包含<html>或<body>标签），格式如下：
<h3><a href="{paper.link}">{paper.title}</a></h3>
<p><b>💡 核心 Idea:</b> [一句话解释]</p>
<p><b>✨ 亮点:</b> [1-2个关键点]</p>
<p><b>⭐️ 推荐度:</b> [1-5星]</p>
<hr>
"""

        try:
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            content = response.choices[0].message.content
            if not content:
                print(f"    ⚠️ 警告: LLM 返回空内容")
            return content
        except Exception as e:
            print(f"    ❌ LLM 调用异常: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return f"<p>Error analyzing {paper.title}: {e}</p>"
