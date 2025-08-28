"""
配置文件
"""
import os
from typing import Optional

class Settings:
    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8010
    DEBUG: bool = True
    
    # Dify API 配置 - 只使用一个智能体
    DIFY_API_BASE_URL: str = os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1")
    DIFY_API_KEY: str = os.getenv("DIFY_API_KEY", "")

    # Dify知识库API配置
    DIFY_KNOWLEDGE_API_KEY: str = os.getenv("DIFY_KNOWLEDGE_API_KEY", "")
    
    # 数据存储路径
    DATA_DIR: str = "API/own_knle"
    WRONG_ANSWERS_DIR: str = f"{DATA_DIR}/wrong_answers"
    USER_PROFILES_DIR: str = f"{DATA_DIR}/user_profiles"
    VECTORS_DIR: str = f"{DATA_DIR}/vectors"
    
    # 文件上传配置
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set = {
        "pdf", "docx", "txt", "md", "csv", "xlsx",
        "png", "jpg", "jpeg", "webp", "gif"
    }
    
    # API限制
    MAX_QUESTION_COUNT: int = 20
    DEFAULT_QUESTION_COUNT: int = 5

settings = Settings()

# 确保数据目录存在
os.makedirs(settings.WRONG_ANSWERS_DIR, exist_ok=True)
os.makedirs(settings.USER_PROFILES_DIR, exist_ok=True)
os.makedirs(settings.VECTORS_DIR, exist_ok=True)
