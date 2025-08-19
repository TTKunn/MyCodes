"""
简单的Coze API测试
"""

from coze_client import CozeClient
from config import COZE_CONFIG


def main():
    print("🤖 Coze API 简单测试")
    print("=" * 40)
    
    # 初始化客户端
    client = CozeClient(
        access_token=COZE_CONFIG["ACCESS_TOKEN"],
        bot_id=COZE_CONFIG["BOT_ID"]
    )
    
    print(f"🔑 Token: {COZE_CONFIG['ACCESS_TOKEN'][:20]}...")
    print(f"🤖 Bot ID: {COZE_CONFIG['BOT_ID']}")
    print()
    
    # 测试对话
    user_id = "test_user_123"
    
    while True:
        # 获取用户输入
        message = input("你: ").strip()
        
        if message.lower() in ['quit', 'exit', '退出']:
            print("再见！")
            break
            
        if not message:
            continue
        
        print("正在请求...")

        # 发送消息并等待回复
        response = client.chat(user_id, message)

        if response:
            print(f"📡 响应状态: {response.get('code', 'N/A')}")

            if response.get("code") == 0:
                # 解析消息列表
                data = response.get("data", [])
                found_reply = False

                # 查找AI的回复
                for msg in data:
                    if msg.get("role") == "assistant" and msg.get("type") == "answer":
                        content = msg.get("content", "").strip()
                        if content:
                            print(f"🤖 AI: {content}")
                            found_reply = True
                            break

                if not found_reply:
                    print("🤖 AI: [没有找到回复内容，可能还在处理中]")
                    # 显示原始响应用于调试
                    print(f"📋 原始响应: {response}")

            else:
                print(f"❌ 请求失败: {response.get('msg', '未知错误')}")
                print(f"📋 详细信息: {response}")
        else:
            print("❌ 请求失败或超时")
        
        print("-" * 40)


if __name__ == "__main__":
    main()
