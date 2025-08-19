# Coze API 面试项目

这是一个将Coze智能体封装成自定义API的项目，包含终端测试和RESTful API服务。

## 📁 项目结构

```
test_cozeAPI/
├── coze_client.py          # Coze API 客户端封装
├── config.py               # 配置文件
├── simple_test.py          # 终端测试脚本
├── api_server.py           # Flask API服务器
├── test_api.py             # API测试客户端
├── requirements.txt        # 依赖包
└── README.md              # 说明文档
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置信息
在 `config.py` 中已经配置了你的 Coze API 信息：
- ACCESS_TOKEN: `pat_4ciNcRp1U4rTeSbvNWrDMuG5n29kNB7zECYKg0f2qgwUUFwyz6XU2FusAmdKMp1f`
- BOT_ID: `7539784189827104777`

## 🎮 使用方式

### 方式一：终端测试
```bash
python simple_test.py
```
- 在终端中直接与AI对话
- 输入 `quit` 或 `exit` 退出

### 方式二：API服务
1. **启动API服务器**
```bash
python api_server.py
```

2. **测试API接口**
```bash
python test_api.py
```

3. **API接口说明**
- `GET /api/health` - 健康检查
- `POST /api/chat` - 普通聊天
- `POST /api/interview/start` - 开始面试
- `POST /api/interview/{id}/answer` - 面试回答

## 📝 CozeClient 类

简化的 API 客户端类，只有一个方法：
- `chat(user_id, message)`: 发送聊天消息

## 📋 注意事项

1. 确保你的 Coze 智能体已发布为 API 服务
2. 检查网络连接，确保可以访问 `https://api.coze.cn`
3. 如果遇到认证问题，请检查 ACCESS_TOKEN 是否正确
