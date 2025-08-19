"""
简历定制面试模块
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
import json
import os
import tempfile

from api.models import (
    ResumeInterviewRequest,
    ResumeInterviewResponse,
    ResumeAnalysis,
    InterviewQuestion
)
from api.dify_client import dify_manager
from utils.file_handler import FileHandler, DataManager
from config import settings

router = APIRouter()

@router.post("/upload_resume/", response_model=ResumeInterviewResponse)
async def upload_resume(request: ResumeInterviewRequest):
    """
    上传简历生成面试题
    
    分析简历内容，提取关键信息，生成个性化面试题。
    如果提供user_id，会自动将简历写入用户知识库。
    """
    try:
        # 分析简历
        analysis = await _analyze_resume(request.resume_text)
        
        # 如果提供了user_id，保存简历到知识库
        if request.user_id:
            kb_name = f"resume_{request.user_id}"
            metadata = {
                "user_id": request.user_id,
                "target_position": request.target_position,
                "created_at": "2024-01-01T00:00:00"  # 实际应用中使用当前时间
            }
            await DataManager.save_knowledge_base(kb_name, request.resume_text, metadata)
        
        # 生成面试题
        questions = await _generate_resume_questions(analysis, request.target_position)
        
        return ResumeInterviewResponse(
            analysis=analysis,
            questions=questions,
            total_count=len(questions)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"简历分析失败: {str(e)}")

@router.post("/upload_resume_to_kb/")
async def upload_resume_to_kb(
    user_id: str = Form(...),
    resume_text: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    上传简历（文件/文本）并入库到用户知识库
    
    支持多种文件格式：pdf, docx, txt, md, csv, xlsx
    可以同时上传文本和文件。
    """
    try:
        kb_name = f"resume_{user_id}"
        all_content = []
        
        # 处理文本内容
        if resume_text and resume_text.strip():
            all_content.append(resume_text.strip())
        
        # 处理上传的文件
        if files:
            for file in files:
                if not file.filename:
                    continue
                
                # 检查文件扩展名
                file_ext = file.filename.split('.')[-1].lower()
                if file_ext not in settings.ALLOWED_EXTENSIONS:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"不支持的文件类型: {file_ext}"
                    )
                
                # 检查文件大小
                content = await file.read()
                if len(content) > settings.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"文件 {file.filename} 超过大小限制"
                    )
                
                # 保存临时文件并解析
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp_file:
                    temp_file.write(content)
                    temp_file_path = temp_file.name
                
                try:
                    # 提取文件内容
                    file_content = await FileHandler.extract_text_from_file(temp_file_path, file_ext)
                    if file_content.strip():
                        all_content.append(f"=== {file.filename} ===\n{file_content}")
                finally:
                    # 清理临时文件
                    os.unlink(temp_file_path)
        
        if not all_content:
            raise HTTPException(status_code=400, detail="没有提供有效的简历内容")
        
        # 合并所有内容
        combined_content = "\n\n".join(all_content)
        
        # 保存到知识库
        metadata = {
            "user_id": user_id,
            "file_count": len(files) if files else 0,
            "has_text": bool(resume_text and resume_text.strip()),
            "created_at": "2024-01-01T00:00:00"  # 实际应用中使用当前时间
        }
        
        await DataManager.save_knowledge_base(kb_name, combined_content, metadata)
        
        return {
            "message": "简历已入库到用户知识库",
            "kb_name": kb_name,
            "code": 200
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"简历入库失败: {str(e)}")

async def _analyze_resume(resume_text: str) -> ResumeAnalysis:
    """分析简历内容"""
    try:
        # 获取简历分析专用的Dify客户端
        client = dify_manager.get_client("resume")
        
        # 构建分析提示词
        prompt = f"""
        请分析以下简历内容，提取关键信息：

        简历内容：
        {resume_text}

        请以JSON格式返回分析结果，包含以下字段：
        {{
            "education_background": ["教育背景1", "教育背景2"],
            "work_experience": ["工作经历1", "工作经历2"],
            "skills": ["技能1", "技能2", "技能3"],
            "projects": ["项目经历1", "项目经历2"],
            "keywords": ["关键词1", "关键词2", "关键词3"]
        }}

        要求：
        1. 教育背景：学校、专业、学历等
        2. 工作经历：公司、职位、主要职责
        3. 技能：技术技能、工具、框架等
        4. 项目经历：项目名称、技术栈、主要贡献
        5. 关键词：从简历中提取的技术关键词和技能点
        """
        
        # 调用Dify API
        response = await client.chat_completion(
            query=prompt,
            user_id="resume_analysis_system",
            response_mode="blocking"
        )
        
        # 解析响应
        answer = response.get("answer", "")
        
        # 尝试解析JSON响应
        try:
            json_start = answer.find('{')
            json_end = answer.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = answer[json_start:json_end]
                analysis_data = json.loads(json_str)
                
                return ResumeAnalysis(
                    education_background=analysis_data.get("education_background", []),
                    work_experience=analysis_data.get("work_experience", []),
                    skills=analysis_data.get("skills", []),
                    projects=analysis_data.get("projects", []),
                    keywords=analysis_data.get("keywords", [])
                )
            else:
                raise ValueError("无法解析JSON响应")
                
        except (json.JSONDecodeError, ValueError):
            # 如果JSON解析失败，使用简单的文本分析
            return _simple_resume_analysis(resume_text)
    
    except Exception as e:
        # 如果分析失败，返回基础分析
        return _simple_resume_analysis(resume_text)

async def _generate_resume_questions(analysis: ResumeAnalysis, target_position: Optional[str] = None) -> List[InterviewQuestion]:
    """基于简历分析生成面试题"""
    try:
        # 获取简历面试专用的Dify客户端
        client = dify_manager.get_client("resume")
        
        # 构建生成题目的提示词
        prompt = f"""
        基于以下简历分析结果，生成5-8道个性化面试题：

        教育背景：{analysis.education_background}
        工作经历：{analysis.work_experience}
        技能：{analysis.skills}
        项目经历：{analysis.projects}
        关键词：{analysis.keywords}
        目标职位：{target_position or "未指定"}

        请生成针对性的面试题，要求：
        1. 结合候选人的实际经历
        2. 针对简历中提到的技术和项目
        3. 包含行为面试和技术面试题目
        4. 题目要有深度和针对性

        请以JSON格式返回，包含以下字段：
        {{
            "questions": [
                {{
                    "question": "具体题目内容",
                    "difficulty": "中级",
                    "category": "题目分类",
                    "knowledge_points": ["相关知识点1", "相关知识点2"]
                }}
            ]
        }}
        """
        
        # 调用Dify API
        response = await client.chat_completion(
            query=prompt,
            user_id="resume_question_system",
            response_mode="blocking"
        )
        
        # 解析响应
        answer = response.get("answer", "")
        
        # 尝试解析JSON响应
        try:
            json_start = answer.find('{')
            json_end = answer.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = answer[json_start:json_end]
                questions_data = json.loads(json_str)
                
                questions = []
                for q in questions_data.get("questions", []):
                    question = InterviewQuestion(
                        question=q.get("question", ""),
                        difficulty=q.get("difficulty", "中级"),
                        category=q.get("category", "综合类"),
                        knowledge_points=q.get("knowledge_points", [])
                    )
                    questions.append(question)
                
                return questions
            else:
                raise ValueError("无法解析JSON响应")
                
        except (json.JSONDecodeError, ValueError):
            # 如果JSON解析失败，生成默认题目
            return _generate_default_resume_questions(analysis, target_position)
    
    except Exception as e:
        # 如果生成失败，返回默认题目
        return _generate_default_resume_questions(analysis, target_position)

def _simple_resume_analysis(resume_text: str) -> ResumeAnalysis:
    """简单的简历分析"""
    text_lower = resume_text.lower()
    
    # 简单的关键词提取
    tech_keywords = []
    common_techs = ['java', 'python', 'javascript', 'react', 'vue', 'spring', 'mysql', 'redis', 'docker', 'kubernetes']
    for tech in common_techs:
        if tech in text_lower:
            tech_keywords.append(tech.capitalize())
    
    return ResumeAnalysis(
        education_background=["待分析"],
        work_experience=["待分析"],
        skills=tech_keywords or ["待分析"],
        projects=["待分析"],
        keywords=tech_keywords or ["待分析"]
    )

def _generate_default_resume_questions(analysis: ResumeAnalysis, target_position: Optional[str] = None) -> List[InterviewQuestion]:
    """生成默认简历面试题"""
    questions = []
    
    # 基础问题
    base_questions = [
        "请简单介绍一下你的工作经历？",
        "你最有成就感的项目是什么？请详细介绍一下。",
        "在项目中遇到过什么技术难题？是如何解决的？",
        "你的职业规划是什么？",
        "为什么选择我们公司？"
    ]
    
    # 根据技能生成技术问题
    if analysis.skills:
        for skill in analysis.skills[:3]:  # 取前3个技能
            base_questions.append(f"请详细介绍一下你在{skill}方面的经验？")
    
    # 转换为InterviewQuestion对象
    for i, q_text in enumerate(base_questions[:6]):  # 限制为6个问题
        question = InterviewQuestion(
            question=q_text,
            difficulty="中级",
            category="综合类" if i < 2 else "技术类",
            knowledge_points=analysis.keywords[:3] if analysis.keywords else []
        )
        questions.append(question)
    
    return questions
