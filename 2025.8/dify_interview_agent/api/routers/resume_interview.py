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
from api.dify_client import dify_client, dify_knowledge_api
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
        # 使用Dify智能体直接分析简历并生成面试题
        prompt = f"""
        请分析以下简历内容并生成8道个性化面试题：

        简历内容：
        {request.resume_text}

        目标职位：{request.target_position or "未指定"}

        要求：
        1. 先分析简历的关键信息（教育背景、工作经历、技能、项目等）
        2. 基于分析结果生成针对性面试题
        3. 包含技术类、行为类、项目类问题
        4. 题目要有深度和针对性

        请以JSON格式返回，包含以下字段：
        {{
            "analysis": {{
                "education_background": ["教育背景1", "教育背景2"],
                "work_experience": ["工作经历1", "工作经历2"],
                "skills": ["技能1", "技能2"],
                "projects": ["项目1", "项目2"],
                "keywords": ["关键词1", "关键词2"]
            }},
            "questions": [
                {{
                    "question": "具体题目内容",
                    "difficulty": "初级/中级/高级",
                    "category": "技术类/行为类/项目类",
                    "knowledge_points": ["知识点1", "知识点2"]
                }}
            ]
        }}
        """

        # 调用Dify API
        response = await dify_client.chat_completion(
            query=prompt,
            user_id="resume_analysis_system",
            response_mode="blocking"
        )

        # 解析响应
        result = await _parse_resume_analysis_response(response)

        # 如果提供了user_id，将简历上传到知识库
        if request.user_id:
            try:
                dataset_id = await _get_or_create_user_dataset(request.user_id)
                text_content = request.resume_text.encode('utf-8')
                await dify_knowledge_api.upload_document(
                    dataset_id=dataset_id,
                    file_content=text_content,
                    filename=f"resume_analysis_{request.user_id}.txt"
                )
            except Exception as e:
                # 知识库上传失败不影响主要功能
                print(f"简历上传到知识库失败: {e}")

        return ResumeInterviewResponse(
            analysis=result["analysis"],
            questions=result["questions"],
            total_count=len(result["questions"])
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
    上传简历到Dify知识库

    使用Dify知识库API上传简历文件或文本到用户专属知识库。
    支持多种文件格式：pdf, docx, txt, md, csv, xlsx
    """
    try:
        if not files and not (resume_text and resume_text.strip()):
            raise HTTPException(status_code=400, detail="请提供简历文件或文本内容")

        # 1. 确保用户有专属知识库
        dataset_id = await _get_or_create_user_dataset(user_id)

        uploaded_files = []

        # 2. 处理文本内容
        if resume_text and resume_text.strip():
            # 将文本内容作为文件上传
            text_content = resume_text.strip().encode('utf-8')
            result = await dify_knowledge_api.upload_document(
                dataset_id=dataset_id,
                file_content=text_content,
                filename=f"resume_text_{user_id}.txt"
            )
            uploaded_files.append({
                "type": "text",
                "filename": f"resume_text_{user_id}.txt",
                "document_id": result.get("document", {}).get("id")
            })

        # 3. 处理上传的文件
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

                # 直接上传到Dify知识库
                result = await dify_knowledge_api.upload_document(
                    dataset_id=dataset_id,
                    file_content=content,
                    filename=file.filename
                )

                uploaded_files.append({
                    "type": "file",
                    "filename": file.filename,
                    "document_id": result.get("document", {}).get("id")
                })

        return {
            "message": "简历已上传到Dify知识库",
            "dataset_id": dataset_id,
            "uploaded_files": uploaded_files,
            "total_files": len(uploaded_files),
            "code": 200
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"简历上传失败: {str(e)}")

@router.post("/generate_resume_questions/")
async def generate_resume_questions(user_id: str = Form(...)):
    """
    基于Dify知识库中的简历生成面试题

    从用户的知识库中检索简历信息，生成个性化面试题。
    """
    try:
        # 构建提示词，让Dify智能体从知识库检索简历内容
        prompt = f"""
        请基于知识库中用户{user_id}的简历信息，生成8道个性化面试题。

        要求：
        1. 结合简历中的具体项目经历和工作背景
        2. 针对简历中提到的技能和技术栈
        3. 包含技术面试和行为面试问题
        4. 题目要有深度和针对性
        5. 避免过于宽泛的问题

        请以JSON格式返回，包含以下字段：
        {{
            "questions": [
                {{
                    "question": "具体题目内容",
                    "difficulty": "初级/中级/高级",
                    "category": "技术类/行为类/项目类",
                    "knowledge_points": ["相关知识点1", "知识点2"]
                }}
            ]
        }}
        """

        # 调用Dify API，智能体会自动从关联的知识库检索相关内容
        response = await dify_client.chat_completion(
            query=prompt,
            user_id=f"resume_questions_{user_id}",
            response_mode="blocking"
        )

        # 解析响应
        questions = await _parse_questions_from_response(response)

        return {
            "questions": questions,
            "user_id": user_id,
            "total_count": len(questions),
            "code": 200
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成简历面试题失败: {str(e)}")

async def _get_or_create_user_dataset(user_id: str) -> str:
    """获取或创建用户专属知识库"""
    try:
        # 尝试获取现有知识库列表
        datasets_response = await dify_knowledge_api.get_datasets()
        datasets = datasets_response.get("data", [])

        # 查找用户专属知识库
        dataset_name = f"resume_{user_id}"
        for dataset in datasets:
            if dataset.get("name") == dataset_name:
                return dataset.get("id")

        # 如果不存在，创建新的知识库
        create_response = await dify_knowledge_api.create_dataset(
            name=dataset_name,
            description=f"用户{user_id}的简历知识库"
        )

        return create_response.get("id")

    except Exception as e:
        raise Exception(f"获取或创建用户知识库失败: {str(e)}")

async def _parse_questions_from_response(response: dict) -> list:
    """解析Dify响应中的面试题"""
    try:
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
                    question = {
                        "question": q.get("question", ""),
                        "difficulty": q.get("difficulty", "中级"),
                        "category": q.get("category", "综合类"),
                        "knowledge_points": q.get("knowledge_points", [])
                    }
                    questions.append(question)

                return questions
            else:
                raise ValueError("无法解析JSON响应")

        except (json.JSONDecodeError, ValueError):
            # 如果JSON解析失败，生成默认题目
            return _generate_default_questions()

    except Exception as e:
        # 如果解析失败，返回默认题目
        return _generate_default_questions()

def _generate_default_questions() -> list:
    """生成默认面试题"""
    default_questions = [
        {
            "question": "请简单介绍一下你的工作经历和主要项目？",
            "difficulty": "初级",
            "category": "综合类",
            "knowledge_points": ["工作经历", "项目经验"]
        },
        {
            "question": "你在项目中遇到过什么技术难题？是如何解决的？",
            "difficulty": "中级",
            "category": "技术类",
            "knowledge_points": ["问题解决", "技术能力"]
        },
        {
            "question": "请描述一个你最有成就感的项目，以及你在其中的贡献？",
            "difficulty": "中级",
            "category": "项目类",
            "knowledge_points": ["项目管理", "个人贡献"]
        },
        {
            "question": "你的职业规划是什么？为什么选择我们公司？",
            "difficulty": "初级",
            "category": "行为类",
            "knowledge_points": ["职业规划", "求职动机"]
        },
        {
            "question": "请谈谈你在团队协作中的经验和心得？",
            "difficulty": "中级",
            "category": "行为类",
            "knowledge_points": ["团队协作", "沟通能力"]
        }
    ]

    return default_questions

async def _parse_resume_analysis_response(response: dict) -> dict:
    """解析简历分析响应"""
    try:
        answer = response.get("answer", "")

        # 尝试解析JSON响应
        try:
            json_start = answer.find('{')
            json_end = answer.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = answer[json_start:json_end]
                data = json.loads(json_str)

                # 解析分析结果
                analysis_data = data.get("analysis", {})
                analysis = ResumeAnalysis(
                    education_background=analysis_data.get("education_background", ["待分析"]),
                    work_experience=analysis_data.get("work_experience", ["待分析"]),
                    skills=analysis_data.get("skills", ["待分析"]),
                    projects=analysis_data.get("projects", ["待分析"]),
                    keywords=analysis_data.get("keywords", ["待分析"])
                )

                # 解析面试题
                questions = []
                for q in data.get("questions", []):
                    question = InterviewQuestion(
                        question=q.get("question", ""),
                        difficulty=q.get("difficulty", "中级"),
                        category=q.get("category", "综合类"),
                        knowledge_points=q.get("knowledge_points", [])
                    )
                    questions.append(question)

                return {
                    "analysis": analysis,
                    "questions": questions
                }
            else:
                raise ValueError("无法解析JSON响应")

        except (json.JSONDecodeError, ValueError):
            # 如果JSON解析失败，返回默认结果
            return _generate_default_resume_result()

    except Exception as e:
        # 如果解析失败，返回默认结果
        return _generate_default_resume_result()

def _generate_default_resume_result() -> dict:
    """生成默认简历分析结果"""
    analysis = ResumeAnalysis(
        education_background=["待分析"],
        work_experience=["待分析"],
        skills=["待分析"],
        projects=["待分析"],
        keywords=["待分析"]
    )

    questions = [
        InterviewQuestion(
            question="请简单介绍一下你的工作经历？",
            difficulty="初级",
            category="综合类",
            knowledge_points=["工作经历"]
        ),
        InterviewQuestion(
            question="你最有成就感的项目是什么？请详细介绍一下。",
            difficulty="中级",
            category="项目类",
            knowledge_points=["项目经验"]
        ),
        InterviewQuestion(
            question="在项目中遇到过什么技术难题？是如何解决的？",
            difficulty="中级",
            category="技术类",
            knowledge_points=["问题解决"]
        ),
        InterviewQuestion(
            question="你的职业规划是什么？",
            difficulty="初级",
            category="行为类",
            knowledge_points=["职业规划"]
        ),
        InterviewQuestion(
            question="为什么选择我们公司？",
            difficulty="初级",
            category="行为类",
            knowledge_points=["求职动机"]
        )
    ]

    return {
        "analysis": analysis,
        "questions": questions
    }
