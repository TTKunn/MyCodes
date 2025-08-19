from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# 简单配置 - 请替换为你的实际配置
DIFY_BASE_URL = 'https://api.dify.ai/v1'  # 或者你的私有部署地址
DIFY_API_KEY = 'your-dify-api-key'  # 替换为你的API Key

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    智能体对话接口 - 支持用户ID传参
    """
    try:
        data = request.get_json()

        # 验证必需参数
        if not data:
            return jsonify({'error': '请求体不能为空'}), 400

        user_id = data.get('user_id')
        message = data.get('message')
        conversation_id = data.get('conversation_id', '')  # 空字符串表示新对话

        if not user_id:
            return jsonify({'error': 'user_id参数是必需的'}), 400

        if not message:
            return jsonify({'error': 'message参数是必需的'}), 400

        # 调用Dify API
        url = f"{DIFY_BASE_URL}/chat-messages"
        headers = {
            'Authorization': f'Bearer {DIFY_API_KEY}',
            'Content-Type': 'application/json'
        }

        # 构建请求数据
        payload = {
            'inputs': {},  # 可以为空，因为我们使用sys.user_id
            'query': message,
            'response_mode': 'blocking',
            'conversation_id': conversation_id,
            'user': user_id,  # 这个会变成工作流中的sys.user_id
            'files': []
        }

        # 发送请求到Dify
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        # 构建响应
        return jsonify({
            'success': True,
            'data': {
                'conversation_id': result.get('conversation_id'),
                'message_id': result.get('id'),
                'answer': result.get('answer'),
                'user_id': user_id,
                'created_at': result.get('created_at')
            },
            'timestamp': datetime.now().isoformat()
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': 'Dify服务调用失败',
            'details': str(e)
        }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': '服务器内部错误',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    健康检查接口
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Dify Chat API Demo'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
