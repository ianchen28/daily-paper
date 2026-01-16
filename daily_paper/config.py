"""配置管理模块"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Config:
    """应用配置类"""

    # LLM 配置
    # 支持多种 LLM：
    # - DeepSeek: base_url=https://api.deepseek.com, model=deepseek-chat
    # - Gemini: base_url=https://generativelanguage.googleapis.com/v1beta/openai/, model=gemini-1.5-flash
    # - OpenAI: base_url=https://api.openai.com/v1, model=gpt-3.5-turbo
    LLM_API_KEY: str = os.environ.get("LLM_API_KEY", "")
    LLM_BASE_URL: Optional[str] = os.environ.get("LLM_BASE_URL")
    MODEL_NAME: str = os.environ.get("MODEL_NAME", "deepseek-chat")

    # 邮件配置
    SMTP_SERVER: str = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", "587"))
    EMAIL_SENDER: str = os.environ.get("EMAIL_SENDER", "")
    EMAIL_PASSWORD: str = os.environ.get("EMAIL_PASSWORD", "")
    EMAIL_RECEIVER: str = os.environ.get("EMAIL_RECEIVER", "")

    # 论文源配置
    FEED_URL: str = os.environ.get("FEED_URL",
                                   "https://huggingface.co/papers/feed")
    MAX_PAPERS: int = int(os.environ.get("MAX_PAPERS", "6"))

    # 关注关键词
    KEYWORDS: str = os.environ.get(
        "KEYWORDS", "RAG, Agent, Multimodal, Efficient Training")

    @classmethod
    def validate(cls) -> None:
        """验证必要的配置项"""
        if not cls.LLM_API_KEY:
            raise ValueError("LLM_API_KEY 环境变量未设置")
        if not cls.EMAIL_SENDER:
            raise ValueError("EMAIL_SENDER 环境变量未设置")
        if not cls.EMAIL_PASSWORD:
            raise ValueError("EMAIL_PASSWORD 环境变量未设置")
        if not cls.EMAIL_RECEIVER:
            raise ValueError("EMAIL_RECEIVER 环境变量未设置")
