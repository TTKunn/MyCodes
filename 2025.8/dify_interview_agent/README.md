# AI面试系统 API

基于Dify的AI面试系统API封装，提供完整的面试功能模块。

## 功能特性

- 🏢 **公司题库面试**: 基于公司名称生成定制化面试题
- 🎯 **自选知识点面试**: 根据技术关键词生成专项面试题
- 📊 **薄弱知识点强化**: 答题评估、错题册管理、薄弱点分析
- 📄 **简历定制面试**: 简历解析与个性化面试题生成
- 📚 **知识库管理**: 文件上传、向量化存储、智能检索

## 快速开始

### 环境要求

- Python 3.8+
- Dify API访问权限

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件：

```env
# Dify API配置
DIFY_API_BASE_URL=https://api.dify.ai/v1
DIFY_API_KEY=your_default_api_key

# 各模块专用API Key（可选，未配置时使用默认KEY）
COMPANY_INTERVIEW_API_KEY=your_company_interview_key
SELF_INTERVIEW_API_KEY=your_self_interview_key
WEAKNESS_INTERVIEW_API_KEY=your_weakness_interview_key
RESUME_INTERVIEW_API_KEY=your_resume_interview_key
KNOWLEDGE_CHAT_API_KEY=your_knowledge_chat_key
```

### 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8010` 启动。

## API文档

启动服务后，访问以下地址查看完整的API文档：

- Swagger UI: http://localhost:8010/docs
- ReDoc: http://localhost:8010/redoc

## 主要接口

### 公司题库面试

```http
POST /interview/company/generate_company_questions/
```

生成指定公司的定制化面试题。

### 自选知识点面试

```http
POST /interview/self/generate_self_interview/
```

根据技术关键词生成专项面试题。

### 薄弱知识点强化

```http
POST /interview/weakness/submit_answer/
POST /interview/weakness/save_evaluation/
GET /interview/weakness/wrong_answers/{user_id}
GET /interview/weakness/weakness_analysis/{user_id}
```

答题评估、错题册管理和薄弱点分析。

### 简历定制面试

```http
POST /interview/resume/upload_resume/
POST /interview/resume/upload_resume_to_kb/
```

简历分析和个性化面试题生成。

### 知识库管理

```http
POST /knowlage/upload_file/
POST /knowlage/query/
GET /knowlage/list_knowledge_bases/
```

文件上传、知识检索和知识库管理。

## 项目结构

```
dify_interview_agent/
├── main.py                 # 主入口文件
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── api/                   # API模块
│   ├── models.py         # 数据模型
│   ├── dify_client.py    # Dify客户端封装
│   └── routers/          # 路由模块
│       ├── company_interview.py
│       ├── self_interview.py
│       ├── weakness_interview.py
│       ├── resume_interview.py
│       └── knowledge_management.py
├── utils/                 # 工具模块
│   └── file_handler.py   # 文件处理工具
└── API/                   # 数据存储目录
    └── own_knle/
        ├── wrong_answers/ # 错题册
        ├── user_profiles/ # 用户档案
        └── vectors/       # 知识库向量
```

## 使用示例

### Python客户端示例

```python
import requests

# 生成公司面试题
response = requests.post("http://localhost:8010/interview/company/generate_company_questions/", 
    json={
        "company_name": "阿里巴巴",
        "position": "Java后端开发",
        "difficulty": "中级",
        "question_count": 5
    }
)
print(response.json())

# 提交答题评估
response = requests.post("http://localhost:8010/interview/weakness/submit_answer/",
    json={
        "user_id": "user123",
        "question": "请解释Redis的持久化机制",
        "user_answer": "Redis有RDB和AOF两种持久化方式...",
        "knowledge_points": ["Redis", "持久化"]
    }
)
print(response.json())
```

### curl示例

```bash
# 生成自选知识点面试题
curl -X POST "http://localhost:8010/interview/self/generate_self_interview/" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Redis缓存优化",
    "difficulty": "高级",
    "question_count": 6
  }'

# 上传文件到知识库
curl -X POST "http://localhost:8010/knowlage/upload_file/" \
  -F "file=@resume.pdf" \
  -F "kb_name=my_resume"
```

## 注意事项

1. **API Key配置**: 确保配置了有效的Dify API Key
2. **文件大小限制**: 上传文件不能超过50MB
3. **支持的文件格式**: PDF、DOCX、TXT、MD、CSV、XLSX
4. **数据存储**: 错题册和用户数据存储在本地JSON文件中
5. **并发限制**: 根据Dify API的限制调整并发请求

## 开发指南

### 添加新的面试模块

1. 在 `api/routers/` 下创建新的路由文件
2. 在 `api/models.py` 中定义相关数据模型
3. 在 `main.py` 中注册新的路由
4. 在 `config.py` 中添加相关配置

### 自定义Dify客户端

可以通过修改 `api/dify_client.py` 来自定义Dify API的调用逻辑。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
