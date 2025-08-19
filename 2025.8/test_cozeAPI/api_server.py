"""
简单的面试API服务器
将Coze智能体封装成RESTful API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from coze_client import CozeClient
from config import COZE_CONFIG
import uuid
import time

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化Coze客户端
coze_client = CozeClient(
    access_token=COZE_CONFIG["ACCESS_TOKEN"],
    bot_id=COZE_CONFIG["BOT_ID"]
)


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "message": "面试API服务正常运行",
        "timestamp": int(time.time())
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    聊天接口
    POST /api/chat
    {
        "message": "用户消息",
        "user_id": "用户ID（可选）"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数: message"
            }), 400
        
        message = data['message']
        user_id = data.get('user_id', f"user_{int(time.time())}")
        
        print(f"收到消息: {message} (用户: {user_id})")
        
        # 调用Coze API
        response = coze_client.chat(user_id, message)
        
        if response and response.get("code") == 0:
            # 解析AI回复
            messages = response.get("data", [])
            ai_reply = ""
            
            for msg in messages:
                if msg.get("role") == "assistant" and msg.get("type") == "answer":
                    ai_reply = msg.get("content", "").strip()
                    break
            
            if not ai_reply:
                ai_reply = "抱歉，我现在无法回复，请稍后再试。"
            
            return jsonify({
                "success": True,
                "data": {
                    "reply": ai_reply,
                    "user_id": user_id
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "AI服务暂时不可用"
            }), 500
            
    except Exception as e:
        print(f"API错误: {e}")
        return jsonify({
            "success": False,
            "error": "服务器内部错误"
        }), 500


@app.route('/api/interview/start', methods=['POST'])
def start_interview():
    """
    开始面试接口
    POST /api/interview/start
    {
        "candidate_name": "候选人姓名（可选）",
        "position": "应聘职位（可选）"
    }
    """
    try:
        data = request.get_json() or {}
        
        candidate_name = data.get('candidate_name', '候选人')
        position = data.get('position', '技术岗位')
        user_id = f"interview_{int(time.time())}"
        
        # 构建面试开始消息
        start_message = f"你好，我是{candidate_name}，我想应聘{position}，请开始面试。"
        
        print(f"开始面试: {start_message} (用户: {user_id})")
        
        # 调用Coze API
        response = coze_client.chat(user_id, start_message)
        
        if response and response.get("code") == 0:
            # 解析AI回复
            messages = response.get("data", [])
            welcome_message = ""
            
            for msg in messages:
                if msg.get("role") == "assistant" and msg.get("type") == "answer":
                    welcome_message = msg.get("content", "").strip()
                    break
            
            if not welcome_message:
                welcome_message = "欢迎参加面试，让我们开始吧！"
            
            return jsonify({
                "success": True,
                "data": {
                    "interview_id": user_id,
                    "welcome_message": welcome_message,
                    "candidate_name": candidate_name,
                    "position": position
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "面试初始化失败"
            }), 500
            
    except Exception as e:
        print(f"开始面试错误: {e}")
        return jsonify({
            "success": False,
            "error": "服务器内部错误"
        }), 500


@app.route('/api/interview/<interview_id>/answer', methods=['POST'])
def interview_answer(interview_id):
    """
    面试回答接口
    POST /api/interview/{interview_id}/answer
    {
        "answer": "候选人的回答"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'answer' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数: answer"
            }), 400
        
        answer = data['answer']
        
        print(f"面试回答: {answer} (面试ID: {interview_id})")
        
        # 调用Coze API
        response = coze_client.chat(interview_id, answer)
        
        if response and response.get("code") == 0:
            # 解析AI回复
            messages = response.get("data", [])
            next_question = ""
            
            for msg in messages:
                if msg.get("role") == "assistant" and msg.get("type") == "answer":
                    next_question = msg.get("content", "").strip()
                    break
            
            if not next_question:
                next_question = "谢谢你的回答，请继续。"
            
            return jsonify({
                "success": True,
                "data": {
                    "next_question": next_question,
                    "interview_id": interview_id
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "获取下一个问题失败"
            }), 500
            
    except Exception as e:
        print(f"面试回答错误: {e}")
        return jsonify({
            "success": False,
            "error": "服务器内部错误"
        }), 500


if __name__ == '__main__':
    print("🚀 启动面试API服务器...")
    print("📚 可用接口:")
    print("  GET  /api/health                     - 健康检查")
    print("  POST /api/chat                       - 普通聊天")
    print("  POST /api/interview/start            - 开始面试")
    print("  POST /api/interview/{id}/answer      - 面试回答")
    print("\n🌐 服务地址: http://localhost:5000")
    print("💡 使用 Ctrl+C 停止服务")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
