# Dify智能体API调用Demo

这是一个简单的Demo，用于学习如何通过API调用Dify智能体，并传入不同的用户ID参数。

## 功能特点

- 支持传入不同的用户ID
- 支持持续对话（通过conversation_id）
- 简单的API封装，便于测试

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置Dify信息

编辑 `app.py` 文件，修改以下配置：

```python
DIFY_BASE_URL = 'https://api.dify.ai/v1'  # 你的Dify API地址
DIFY_API_KEY = 'your-dify-api-key'        # 你的API Key
```

### 3. 运行服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## API接口

### 1. 对话接口

**POST** `/api/chat`

#### 请求参数

```json
{
    "user_id": "user_001",           // 必需：用户ID
    "message": "你好，我想咨询一下",    // 必需：用户消息
    "conversation_id": ""            // 可选：对话ID，空字符串表示新对话
}
```

#### 响应示例

```json
{
    "success": true,
    "data": {
        "conversation_id": "conv_123456",
        "message_id": "msg_789012",
        "answer": "你好！我是智能助手，很高兴为您服务。请问有什么可以帮助您的吗？",
        "user_id": "user_001",
        "created_at": 1703123456
    },
    "timestamp": "2023-12-21T10:30:45.123456"
}
```

### 2. 健康检查接口

**GET** `/api/health`

#### 响应示例

```json
{
    "status": "healthy",
    "timestamp": "2023-12-21T10:30:45.123456",
    "service": "Dify Chat API Demo"
}
```

## 在Apifox中测试

### 1. 新建对话

- **方法**: POST
- **URL**: `http://localhost:5000/api/chat`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "user_id": "user_001",
    "message": "你好"
}
```

### 2. 继续对话

使用第一次对话返回的 `conversation_id`：

```json
{
    "user_id": "user_001",
    "message": "我想了解更多信息",
    "conversation_id": "conv_123456"
}
```

### 3. 不同用户对话

更换 `user_id` 来模拟不同用户：

```json
{
    "user_id": "user_002",
    "message": "你好，我是另一个用户"
}
```

## 注意事项

1. 请确保你的Dify应用已经正确配置并启用了API访问
2. 替换 `app.py` 中的 `DIFY_API_KEY` 为你的实际API密钥
3. 如果使用私有部署的Dify，请修改 `DIFY_BASE_URL`
4. 在Dify智能体中，你可以通过 `{{#inputs.user_id#}}` 来获取传入的用户ID参数

## 错误处理

API会返回标准的HTTP状态码：

- `200`: 成功
- `400`: 请求参数错误
- `500`: 服务器内部错误

错误响应格式：

```json
{
    "success": false,
    "error": "错误描述",
    "details": "详细错误信息"
}
```
