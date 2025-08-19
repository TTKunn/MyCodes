"""
API测试客户端
测试自定义的面试API接口
"""

import requests
import json


class InterviewAPIClient:
    """面试API客户端"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def health_check(self):
        """健康检查"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def chat(self, message, user_id=None):
        """普通聊天"""
        data = {"message": message}
        if user_id:
            data["user_id"] = user_id
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def start_interview(self, candidate_name=None, position=None):
        """开始面试"""
        data = {}
        if candidate_name:
            data["candidate_name"] = candidate_name
        if position:
            data["position"] = position
        
        try:
            response = requests.post(
                f"{self.base_url}/api/interview/start",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def interview_answer(self, interview_id, answer):
        """面试回答"""
        data = {"answer": answer}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/interview/{interview_id}/answer",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def test_health():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    client = InterviewAPIClient()
    result = client.health_check()
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    return result.get("status") == "ok"


def test_chat():
    """测试普通聊天"""
    print("\n=== 测试普通聊天 ===")
    client = InterviewAPIClient()
    
    message = "你好，请介绍一下你自己"
    print(f"发送消息: {message}")
    
    result = client.chat(message)
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    return result.get("success", False)


def test_interview():
    """测试面试流程"""
    print("\n=== 测试面试流程 ===")
    client = InterviewAPIClient()
    
    # 1. 开始面试
    print("1. 开始面试...")
    start_result = client.start_interview(
        candidate_name="张三",
        position="Python开发工程师"
    )
    print(f"开始面试结果: {json.dumps(start_result, ensure_ascii=False, indent=2)}")
    
    if not start_result.get("success"):
        print("开始面试失败")
        return False
    
    interview_id = start_result["data"]["interview_id"]
    print(f"面试ID: {interview_id}")
    print(f"欢迎消息: {start_result['data']['welcome_message']}")
    
    # 2. 回答问题
    answers = [
        "我有3年的Python开发经验，熟悉Django和Flask框架",
        "我参与过电商系统的开发，负责用户管理和订单处理模块",
        "我熟悉MySQL数据库，了解索引优化和查询优化"
    ]
    
    for i, answer in enumerate(answers, 2):
        print(f"\n{i}. 回答问题...")
        print(f"回答: {answer}")
        
        answer_result = client.interview_answer(interview_id, answer)
        print(f"面试官回复: {json.dumps(answer_result, ensure_ascii=False, indent=2)}")
        
        if not answer_result.get("success"):
            print("回答问题失败")
            return False
        
        print(f"下一个问题: {answer_result['data']['next_question']}")
    
    return True


def main():
    """主测试函数"""
    print("🧪 面试API测试工具")
    print("=" * 50)
    
    # 测试健康检查
    if not test_health():
        print("❌ 健康检查失败，请确保API服务已启动")
        return
    
    print("✅ 健康检查通过")
    
    # 选择测试模式
    print("\n请选择测试模式:")
    print("1. 普通聊天测试")
    print("2. 面试流程测试")
    print("3. 全部测试")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == "1":
        success = test_chat()
        print(f"\n{'✅ 普通聊天测试通过' if success else '❌ 普通聊天测试失败'}")
    elif choice == "2":
        success = test_interview()
        print(f"\n{'✅ 面试流程测试通过' if success else '❌ 面试流程测试失败'}")
    elif choice == "3":
        chat_success = test_chat()
        interview_success = test_interview()
        print(f"\n普通聊天: {'✅ 通过' if chat_success else '❌ 失败'}")
        print(f"面试流程: {'✅ 通过' if interview_success else '❌ 失败'}")
    else:
        print("无效选择")


if __name__ == "__main__":
    main()
