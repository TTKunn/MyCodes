"""
Coze API 客户端 - 支持完整对话
"""

import requests
import json
import time


class CozeClient:
    """Coze API 客户端"""

    def __init__(self, access_token: str, bot_id: str):
        self.access_token = access_token
        self.bot_id = bot_id
        self.base_url = "https://api.coze.cn"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def chat(self, user_id: str, message: str):
        """发送聊天消息并等待完整回复"""
        # 1. 发起对话
        chat_response = self._start_chat(user_id, message)
        if not chat_response or chat_response.get("code") != 0:
            return None

        # 2. 获取对话ID
        data = chat_response.get("data", {})
        conversation_id = data.get("conversation_id")
        chat_id = data.get("id")

        if not conversation_id or not chat_id:
            print("无法获取对话ID")
            return None

        # 3. 轮询等待对话完成
        return self._wait_for_completion(conversation_id, chat_id)

    def _start_chat(self, user_id: str, message: str):
        """发起对话"""
        url = f"{self.base_url}/v3/chat"

        data = {
            "bot_id": self.bot_id,
            "user_id": user_id,
            "stream": False,
            "auto_save_history": True,
            "additional_messages": [
                {
                    "role": "user",
                    "content": message,
                    "content_type": "text"
                }
            ]
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"发起对话失败: {e}")
            return None

    def _wait_for_completion(self, conversation_id: str, chat_id: str, max_wait_time: int = 30):
        """等待对话完成"""
        url = f"{self.base_url}/v3/chat/retrieve"

        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                # 查询对话状态
                params = {
                    "conversation_id": conversation_id,
                    "chat_id": chat_id
                }

                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                result = response.json()

                if result.get("code") != 0:
                    print(f"查询对话状态失败: {result}")
                    return None

                data = result.get("data", {})
                status = data.get("status", "")

                print(f"对话状态: {status}")

                if status == "completed":
                    # 对话完成，获取消息
                    return self._get_messages(conversation_id)
                elif status == "failed":
                    print("对话失败")
                    return None
                elif status in ["in_progress", "created"]:
                    # 继续等待
                    time.sleep(2)
                    continue
                else:
                    print(f"未知状态: {status}")
                    return None

            except Exception as e:
                print(f"查询对话状态出错: {e}")
                time.sleep(2)
                continue

        print("等待超时")
        return None

    def _get_messages(self, conversation_id: str):
        """获取对话消息"""
        url = f"{self.base_url}/v1/conversation/message/list"

        try:
            params = {"conversation_id": conversation_id}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            result = response.json()

            if result.get("code") != 0:
                print(f"获取消息失败: {result}")
                return None

            return result

        except Exception as e:
            print(f"获取消息出错: {e}")
            return None

