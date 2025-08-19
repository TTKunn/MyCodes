"""
配置文件
存储Coze API相关配置信息
"""

# Coze API 配置
COZE_CONFIG = {
    # 你的个人访问令牌
    "ACCESS_TOKEN": "pat_4ciNcRp1U4rTeSbvNWrDMuG5n29kNB7zECYKg0f2qgwUUFwyz6XU2FusAmdKMp1f",
    
    # 你的智能体ID
    "BOT_ID": "7539784189827104777",
    
    # API基础URL
    "BASE_URL": "https://api.coze.cn",
    
    # 默认用户ID（用于测试）
    "DEFAULT_USER_ID": "test_user_123"
}

# 面试官相关配置
INTERVIEW_CONFIG = {
    # 面试类型
    "INTERVIEW_TYPES": [
        "技术面试",
        "行为面试", 
        "综合面试",
        "算法面试",
        "系统设计面试"
    ],
    
    # 技术栈选项
    "TECH_STACKS": [
        "Python",
        "Java",
        "JavaScript",
        "Go",
        "C++",
        "前端开发",
        "后端开发",
        "全栈开发",
        "数据科学",
        "机器学习"
    ]
}
