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
            self.client = OpenAI(api_key=Config.LLM_API_KEY,
                                 base_url=Config.LLM_BASE_URL)
        else:
            # 如果没有指定 base_url，使用默认的 OpenAI API
            self.client = OpenAI(api_key=Config.LLM_API_KEY)

    def summarize(self, paper: Any) -> str:
        """
        使用 LLM 生成论文摘要（HTML 格式）

        Args:
            paper: 论文对象（包含丰富的论文信息）

        Returns:
            HTML 格式的分析结果
        """
        # 构建结构化的上下文信息
        paper_info_parts = []

        # 基本信息
        paper_info_parts.append(f"标题: {paper.title}")
        paper_info_parts.append(f"摘要: {paper.summary}")

        # 作者信息
        if paper.authors:
            authors_str = ', '.join(paper.authors[:5])
            if len(paper.authors) > 5:
                authors_str += f" 等{len(paper.authors)}位作者"
            paper_info_parts.append(f"作者: {authors_str}")

        # 组织信息
        if paper.organization:
            paper_info_parts.append(f"组织: {paper.organization}")

        # AI 生成的摘要和关键词（如果可用，这些是 HuggingFace 的 AI 分析结果）
        if paper.ai_summary:
            paper_info_parts.append(f"\nAI 分析摘要: {paper.ai_summary}")

        if paper.ai_keywords:
            keywords_str = ', '.join(paper.ai_keywords[:15])
            paper_info_parts.append(f"AI 提取关键词: {keywords_str}")

        # GitHub 信息
        if paper.github_repo:
            paper_info_parts.append(f"GitHub 仓库: {paper.github_repo}")

        # 社区反馈指标
        metrics = []
        if paper.upvotes > 0:
            metrics.append(f"点赞 {paper.upvotes}")
        if paper.github_stars > 0:
            metrics.append(f"GitHub Stars {paper.github_stars}")
        if paper.num_comments > 0:
            metrics.append(f"评论 {paper.num_comments}")

        community_feedback = " | ".join(metrics) if metrics else "暂无社区反馈"
        paper_info_parts.append(f"\n社区反馈: {community_feedback}")

        paper_info = "\n".join(paper_info_parts)

        # 构建更专业的 system prompt
        system_prompt = """你是一位资深的 AI/ML 研究助理，擅长分析学术论文并生成精准的中文总结。
你的任务是基于论文的完整信息（包括摘要、AI分析、社区反馈等），生成结构化的中文总结。
请重点关注：
1. 论文的核心贡献和创新点
2. 技术亮点和实用价值
3. 与用户关注领域的相关性
4. 社区反馈反映的论文质量
5. 适用场景和潜在应用"""

        # 构建详细的 user prompt
        user_prompt = f"""请分析以下论文信息，并生成一份精准的中文总结。

论文信息：
{paper_info}

用户关注领域: {Config.KEYWORDS}

请用中文输出 HTML 代码片段（不要包含<html>或<body>标签），严格按照以下格式：

<h3><a href="{paper.link}">{paper.title}</a></h3>
<p><b>💡 核心 Idea:</b> [用一句话清晰概括论文的核心贡献，参考 AI 摘要但用自己的话表达]</p>
<p><b>🔬 技术亮点:</b> [2-3个关键技术点或创新点，要具体且有价值]</p>
<p><b>🎯 适用场景:</b> [1-2个实际应用场景或适用领域]</p>
<p><b>📊 社区反馈:</b> [基于点赞数、GitHub stars、评论数等，简要评价社区认可度]</p>
<p><b>⭐️ 推荐度:</b> [1-5星，综合考虑：1)与用户关注领域的相关性 2)技术创新性 3)社区反馈 4)实用价值。给出具体评分和简短理由]</p>
<hr>

要求：
- 所有内容用中文表达
- 核心 Idea 要简洁准确，不超过50字
- 技术亮点要具体，避免泛泛而谈
- 推荐度要客观，结合多个维度评估
- 如果社区反馈数据较少，在推荐度中说明
- 重点关注与用户关注领域（{Config.KEYWORDS}）的相关性"""

        try:
            print(f"    🔄 调用 LLM API（模型: {Config.MODEL_NAME}）...")
            # 注意：OpenAI SDK 的 timeout 需要在客户端初始化时设置
            # 这里使用默认超时，如果超时会抛出异常
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                ],
                temperature=0.3,
            )
            print(f"    ✅ LLM API 调用成功")

            # 处理响应：支持推理模式（deepseek-reasoner）和普通模式
            message = response.choices[0].message

            # 提取最终答案
            content = message.content
            if not content:
                print(f"    ⚠️ 警告: LLM 返回空内容")
                return f"<p>⚠️ 无法分析 {paper.title}：LLM 返回空内容</p>"

            # 检查是否有推理内容（reasoning mode）
            reasoning_content = None
            if hasattr(message,
                       'reasoning_content') and message.reasoning_content:
                reasoning_content = message.reasoning_content
                print(f"    💭 检测到推理过程（长度: {len(reasoning_content)} 字符）")

            # 如果配置了包含推理过程，且存在推理内容，则组合输出
            if Config.INCLUDE_REASONING and reasoning_content:
                # 在 HTML 中添加推理过程（可选，可以注释掉以仅显示最终答案）
                # 这里我们选择在最终答案前添加一个可折叠的推理过程
                result = f"""<details>
<summary><b>💭 推理过程</b> (点击展开)</summary>
<div style="background-color: #f5f5f5; padding: 10px; margin: 10px 0; border-left: 3px solid #4CAF50; font-size: 0.9em; color: #666;">
{reasoning_content}
</div>
</details>
{content}"""
                return result
            else:
                # 普通模式或不需要推理过程，直接返回最终答案
                return content

        except Exception as e:
            print(f"    ❌ LLM 调用异常: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return f"<p>Error analyzing {paper.title}: {e}</p>"
