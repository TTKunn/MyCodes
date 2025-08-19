"""
Dify API客户端封装
"""
import httpx
import json
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from config import settings

class DifyAPIClient:
    """Dify API客户端"""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or settings.DIFY_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat_completion(
        self,
        query: str,
        user_id: str,
        inputs: Dict[str, Any] = None,
        conversation_id: str = None,
        response_mode: str = "blocking",
        files: list = None
    ) -> Dict[str, Any]:
        """
        发送聊天完成请求
        
        Args:
            query: 用户输入/问题内容
            user_id: 用户标识符
            inputs: 应用定义的各种变量值
            conversation_id: 会话ID，用于继续对话
            response_mode: 响应模式，streaming或blocking
            files: 文件列表（用于Vision模型）
        
        Returns:
            API响应结果
        """
        url = f"{self.base_url}/chat-messages"
        
        payload = {
            "query": query,
            "user": user_id,
            "inputs": inputs or {},
            "response_mode": response_mode,
            "auto_generate_name": True
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        if files:
            payload["files"] = files
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                if response_mode == "streaming":
                    # 处理流式响应
                    return await self._handle_streaming_response(response)
                else:
                    # 处理阻塞式响应
                    return response.json()
                    
            except httpx.HTTPStatusError as e:
                raise Exception(f"Dify API请求失败: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                raise Exception(f"Dify API请求异常: {str(e)}")
    
    async def _handle_streaming_response(self, response: httpx.Response) -> Dict[str, Any]:
        """处理流式响应"""
        full_answer = ""
        last_event_data = None
        
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                try:
                    data = json.loads(line[6:])  # 去掉 "data: " 前缀
                    
                    if data.get("event") == "message":
                        full_answer += data.get("answer", "")
                        last_event_data = data
                    elif data.get("event") == "message_end":
                        last_event_data = data
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        # 返回完整的响应数据
        if last_event_data:
            last_event_data["answer"] = full_answer
            return last_event_data
        else:
            return {"answer": full_answer, "event": "message"}
    
    async def stop_generation(self, task_id: str, user_id: str) -> Dict[str, Any]:
        """
        停止生成
        
        Args:
            task_id: 任务ID
            user_id: 用户ID
        
        Returns:
            停止结果
        """
        url = f"{self.base_url}/chat-messages/{task_id}/stop"
        
        payload = {
            "user": user_id
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                raise Exception(f"停止生成失败: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                raise Exception(f"停止生成异常: {str(e)}")

class DifyClientManager:
    """Dify客户端管理器"""
    
    def __init__(self):
        self._clients = {}
    
    def get_client(self, client_type: str) -> DifyAPIClient:
        """
        获取指定类型的客户端
        
        Args:
            client_type: 客户端类型 (company, self, weakness, resume, knowledge)
        
        Returns:
            DifyAPIClient实例
        """
        if client_type not in self._clients:
            api_key = self._get_api_key(client_type)
            if not api_key:
                raise ValueError(f"未配置{client_type}类型的API Key")
            
            self._clients[client_type] = DifyAPIClient(api_key)
        
        return self._clients[client_type]
    
    def _get_api_key(self, client_type: str) -> str:
        """根据客户端类型获取API Key"""
        key_mapping = {
            "company": settings.COMPANY_INTERVIEW_API_KEY,
            "self": settings.SELF_INTERVIEW_API_KEY,
            "weakness": settings.WEAKNESS_INTERVIEW_API_KEY,
            "resume": settings.RESUME_INTERVIEW_API_KEY,
            "knowledge": settings.KNOWLEDGE_CHAT_API_KEY
        }
        
        return key_mapping.get(client_type, settings.DIFY_API_KEY)

# 全局客户端管理器实例
dify_manager = DifyClientManager()
