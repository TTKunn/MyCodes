"""
知识库管理模块
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
import os
import tempfile

from api.models import (
    KnowledgeUploadResponse,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse
)
from api.dify_client import dify_client
from utils.file_handler import FileHandler, DataManager
from config import settings

router = APIRouter()

@router.post("/upload_file/", response_model=KnowledgeUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    kb_name: Optional[str] = Form(None)
):
    """
    上传文件并解析为向量
    
    支持多种文件格式：PDF、TXT、DOCX、CSV、XLSX等
    文件内容会被解析并存储到知识库中。
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名不能为空")
        
        # 检查文件扩展名
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件类型: {file_ext}。支持的格式: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # 检查文件大小
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小超过限制 ({settings.MAX_FILE_SIZE / 1024 / 1024:.1f}MB)"
            )
        
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # 提取文件内容
            file_content = await FileHandler.extract_text_from_file(temp_file_path, file_ext)
            
            if not file_content.strip():
                raise HTTPException(status_code=400, detail="文件内容为空或无法解析")
            
            # 使用文件名作为知识库名称（如果未指定）
            if not kb_name:
                kb_name = f"kb_{file.filename.rsplit('.', 1)[0]}"
            
            # 保存到知识库
            metadata = {
                "filename": file.filename,
                "file_type": file_ext,
                "file_size": len(content),
                "created_at": "2024-01-01T00:00:00"  # 实际应用中使用当前时间
            }
            
            await DataManager.save_knowledge_base(kb_name, file_content, metadata)
            
            # 简单的分段计算（按段落分）
            segments = len([p for p in file_content.split('\n\n') if p.strip()])
            
            return KnowledgeUploadResponse(
                msg="文件已成功解析并入库",
                segments=segments
            )
        
        finally:
            # 清理临时文件
            os.unlink(temp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@router.post("/query/", response_model=KnowledgeQueryResponse)
async def query_knowledge(request: KnowledgeQueryRequest):
    """
    知识库检索/问答
    
    在指定的知识库中搜索相关信息，并生成答案。
    如果未指定知识库名称，将在默认知识库中搜索。
    """
    try:
        # 使用统一的Dify客户端
        
        # 如果指定了知识库名称，先获取知识库内容作为上下文
        context = ""
        if request.kb_name:
            try:
                content, metadata = await DataManager.get_knowledge_base(request.kb_name)
                if content:
                    # 截取部分内容作为上下文（避免超过token限制）
                    context = content[:2000] + "..." if len(content) > 2000 else content
            except Exception as e:
                # 如果获取知识库失败，继续使用普通查询
                pass
        
        # 构建查询提示词
        if context:
            prompt = f"""
            基于以下知识库内容回答问题：

            知识库内容：
            {context}

            问题：{request.query}

            请基于知识库内容给出准确、详细的答案。如果知识库中没有相关信息，请明确说明。
            """
        else:
            prompt = request.query
        
        # 调用Dify API
        response = await dify_client.chat_completion(
            query=prompt,
            user_id="knowledge_query_system",
            response_mode="blocking"
        )
        
        # 解析响应
        answer = response.get("answer", "")
        
        # 构建引用信息
        citations = []
        if request.kb_name and context:
            citations.append({
                "source": request.kb_name,
                "content": context[:200] + "..." if len(context) > 200 else context,
                "relevance": "high"
            })
        
        return KnowledgeQueryResponse(
            answer=answer,
            citations=citations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识库查询失败: {str(e)}")

@router.post("/knowlage_chat/")
async def knowledge_chat(
    query: str = Form(...),
    kb_name: Optional[str] = Form(None),
    user_id: Optional[str] = Form("default_user")
):
    """
    知识库聊天接口
    
    与指定知识库进行对话，支持上下文记忆。
    兼容原API文档中的接口名称。
    """
    try:
        request = KnowledgeQueryRequest(query=query, kb_name=kb_name)
        response = await query_knowledge(request)
        
        return {
            "code": 200,
            "message": "查询成功",
            "data": {
                "answer": response.answer,
                "citations": response.citations,
                "kb_name": kb_name,
                "user_id": user_id
            }
        }
    
    except HTTPException as e:
        return {
            "code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"聊天失败: {str(e)}",
            "data": None
        }

@router.get("/list_knowledge_bases/")
async def list_knowledge_bases():
    """
    列出所有知识库
    
    返回系统中所有可用的知识库列表。
    """
    try:
        kb_list = []
        vectors_dir = settings.VECTORS_DIR
        
        if os.path.exists(vectors_dir):
            for kb_name in os.listdir(vectors_dir):
                kb_path = os.path.join(vectors_dir, kb_name)
                if os.path.isdir(kb_path):
                    # 获取知识库元数据
                    try:
                        _, metadata = await DataManager.get_knowledge_base(kb_name)
                        kb_info = {
                            "name": kb_name,
                            "created_at": metadata.get("created_at", "未知"),
                            "file_count": metadata.get("file_count", 0),
                            "description": metadata.get("description", "")
                        }
                        kb_list.append(kb_info)
                    except:
                        # 如果无法获取元数据，添加基本信息
                        kb_list.append({
                            "name": kb_name,
                            "created_at": "未知",
                            "file_count": 0,
                            "description": ""
                        })
        
        return {
            "code": 200,
            "message": "获取知识库列表成功",
            "data": {
                "knowledge_bases": kb_list,
                "total_count": len(kb_list)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识库列表失败: {str(e)}")

@router.delete("/delete_knowledge_base/{kb_name}")
async def delete_knowledge_base(kb_name: str):
    """
    删除知识库
    
    删除指定的知识库及其所有数据。
    """
    try:
        kb_path = os.path.join(settings.VECTORS_DIR, kb_name)
        
        if not os.path.exists(kb_path):
            raise HTTPException(status_code=404, detail=f"知识库 {kb_name} 不存在")
        
        # 删除知识库目录
        import shutil
        shutil.rmtree(kb_path)
        
        return {
            "code": 200,
            "message": f"知识库 {kb_name} 已删除",
            "data": {
                "kb_name": kb_name,
                "deleted_at": "2024-01-01T00:00:00"  # 实际应用中使用当前时间
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除知识库失败: {str(e)}")
