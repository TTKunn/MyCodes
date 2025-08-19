"""
文件处理工具
"""
import os
import json
import aiofiles
from datetime import datetime
from typing import Dict, Any, List, Optional
from docx import Document
import PyPDF2
import pandas as pd
from config import settings

class FileHandler:
    """文件处理器"""
    
    @staticmethod
    async def save_json(file_path: str, data: Dict[str, Any]) -> None:
        """保存JSON文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))
    
    @staticmethod
    async def load_json(file_path: str) -> Dict[str, Any]:
        """加载JSON文件"""
        if not os.path.exists(file_path):
            return {}
        
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content) if content.strip() else {}
    
    @staticmethod
    async def extract_text_from_file(file_path: str, file_type: str) -> str:
        """从文件中提取文本"""
        try:
            if file_type.lower() == 'pdf':
                return await FileHandler._extract_from_pdf(file_path)
            elif file_type.lower() == 'docx':
                return await FileHandler._extract_from_docx(file_path)
            elif file_type.lower() in ['txt', 'md']:
                return await FileHandler._extract_from_text(file_path)
            elif file_type.lower() in ['csv', 'xlsx']:
                return await FileHandler._extract_from_excel(file_path, file_type)
            else:
                raise ValueError(f"不支持的文件类型: {file_type}")
        except Exception as e:
            raise Exception(f"文件解析失败: {str(e)}")
    
    @staticmethod
    async def _extract_from_pdf(file_path: str) -> str:
        """从PDF提取文本"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    async def _extract_from_docx(file_path: str) -> str:
        """从DOCX提取文本"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    @staticmethod
    async def _extract_from_text(file_path: str) -> str:
        """从文本文件提取内容"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    
    @staticmethod
    async def _extract_from_excel(file_path: str, file_type: str) -> str:
        """从Excel文件提取文本"""
        if file_type.lower() == 'csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # 将DataFrame转换为文本
        return df.to_string(index=False)

class DataManager:
    """数据管理器"""
    
    @staticmethod
    async def save_wrong_answer(user_id: str, wrong_answer: Dict[str, Any]) -> None:
        """保存错题"""
        file_path = os.path.join(settings.WRONG_ANSWERS_DIR, f"{user_id}.json")
        
        # 加载现有数据
        data = await FileHandler.load_json(file_path)
        if "wrong_answers" not in data:
            data["wrong_answers"] = []
        
        # 添加时间戳
        wrong_answer["created_at"] = datetime.now().isoformat()
        
        # 添加新的错题
        data["wrong_answers"].append(wrong_answer)
        
        # 保存数据
        await FileHandler.save_json(file_path, data)
    
    @staticmethod
    async def get_wrong_answers(user_id: str) -> List[Dict[str, Any]]:
        """获取用户错题"""
        file_path = os.path.join(settings.WRONG_ANSWERS_DIR, f"{user_id}.json")
        data = await FileHandler.load_json(file_path)
        return data.get("wrong_answers", [])
    
    @staticmethod
    async def save_user_profile(user_id: str, profile: Dict[str, Any]) -> None:
        """保存用户档案"""
        file_path = os.path.join(settings.USER_PROFILES_DIR, f"{user_id}.json")
        
        # 添加更新时间
        profile["updated_at"] = datetime.now().isoformat()
        
        await FileHandler.save_json(file_path, profile)
    
    @staticmethod
    async def get_user_profile(user_id: str) -> Dict[str, Any]:
        """获取用户档案"""
        file_path = os.path.join(settings.USER_PROFILES_DIR, f"{user_id}.json")
        return await FileHandler.load_json(file_path)
    
    @staticmethod
    async def save_knowledge_base(kb_name: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """保存知识库内容"""
        kb_dir = os.path.join(settings.VECTORS_DIR, kb_name)
        os.makedirs(kb_dir, exist_ok=True)
        
        # 保存内容
        content_file = os.path.join(kb_dir, "content.txt")
        async with aiofiles.open(content_file, 'w', encoding='utf-8') as f:
            await f.write(content)
        
        # 保存元数据
        if metadata:
            metadata_file = os.path.join(kb_dir, "metadata.json")
            await FileHandler.save_json(metadata_file, metadata)
    
    @staticmethod
    async def get_knowledge_base(kb_name: str) -> tuple[str, Dict[str, Any]]:
        """获取知识库内容"""
        kb_dir = os.path.join(settings.VECTORS_DIR, kb_name)
        
        # 读取内容
        content_file = os.path.join(kb_dir, "content.txt")
        content = ""
        if os.path.exists(content_file):
            async with aiofiles.open(content_file, 'r', encoding='utf-8') as f:
                content = await f.read()
        
        # 读取元数据
        metadata_file = os.path.join(kb_dir, "metadata.json")
        metadata = await FileHandler.load_json(metadata_file)
        
        return content, metadata
