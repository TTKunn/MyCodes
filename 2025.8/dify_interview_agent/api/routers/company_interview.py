"""
公司题库面试模块
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json

from api.models import (
    CompanyInterviewRequest, 
    CompanyInterviewResponse,
    InterviewQuestion
)
from api.dify_client import dify_manager

router = APIRouter()

@router.post("/generate_company_questions/", response_model=CompanyInterviewResponse)
async def generate_company_questions(request: CompanyInterviewRequest):
    """
    生成公司面试题
    
    根据公司名称、职位和难度等级，生成定制化的面试题。
    这些面试题基于近几年的面经，结合公司最新动态和行业热门话题。
    """
    try:
        # 获取公司面试专用的Dify客户端
        client = dify_manager.get_client("company")
        
        # 构建提示词
        prompt = f"""
        请为{request.company_name}公司的{request.position}职位生成{request.question_count}道{request.difficulty}难度的面试题。

        要求：
        1. 题目要结合{request.company_name}公司的特点和文化
        2. 包含该公司常见的面试问题类型
        3. 结合行业最新动态和技术趋势
        4. 难度等级：{request.difficulty}
        5. 题目要有针对性和实用性

        请以JSON格式返回，包含以下字段：
        {{
            "questions": [
                {{
                    "question": "具体题目内容",
                    "difficulty": "难度等级",
                    "category": "题目分类（如技术类、行为类、业务类等）",
                    "knowledge_points": ["相关知识点1", "相关知识点2"]
                }}
            ]
        }}
        """
        
        # 调用Dify API
        response = await client.chat_completion(
            query=prompt,
            user_id="company_interview_system",
            response_mode="blocking"
        )
        
        # 解析响应
        answer = response.get("answer", "")
        
        # 尝试解析JSON响应
        try:
            # 提取JSON部分
            json_start = answer.find('{')
            json_end = answer.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = answer[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                # 转换为标准格式
                questions = []
                for q in parsed_data.get("questions", []):
                    question = InterviewQuestion(
                        question=q.get("question", ""),
                        difficulty=q.get("difficulty", request.difficulty),
                        category=q.get("category"),
                        knowledge_points=q.get("knowledge_points", [])
                    )
                    questions.append(question)
                
                return CompanyInterviewResponse(
                    questions=questions,
                    company_name=request.company_name,
                    position=request.position,
                    total_count=len(questions)
                )
            else:
                raise ValueError("无法解析JSON响应")
                
        except (json.JSONDecodeError, ValueError) as e:
            # 如果JSON解析失败，尝试从文本中提取题目
            questions = _extract_questions_from_text(answer, request)
            
            return CompanyInterviewResponse(
                questions=questions,
                company_name=request.company_name,
                position=request.position,
                total_count=len(questions)
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成面试题失败: {str(e)}")

def _extract_questions_from_text(text: str, request: CompanyInterviewRequest) -> list[InterviewQuestion]:
    """从文本中提取面试题"""
    questions = []
    lines = text.split('\n')
    
    current_question = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是题目行（通常以数字开头或包含问号）
        if any(marker in line for marker in ['?', '？', '1.', '2.', '3.', '4.', '5.']) or \
           (line and (line[0].isdigit() or line.startswith('题目'))):
            
            if current_question:
                # 保存上一个题目
                question = InterviewQuestion(
                    question=current_question.strip(),
                    difficulty=request.difficulty,
                    category="综合类",
                    knowledge_points=[]
                )
                questions.append(question)
            
            # 清理题目文本
            current_question = line
            # 移除序号
            for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.']:
                if current_question.startswith(prefix):
                    current_question = current_question[len(prefix):].strip()
                    break
        else:
            # 继续当前题目
            if current_question:
                current_question += " " + line
    
    # 添加最后一个题目
    if current_question:
        question = InterviewQuestion(
            question=current_question.strip(),
            difficulty=request.difficulty,
            category="综合类",
            knowledge_points=[]
        )
        questions.append(question)
    
    # 如果没有提取到足够的题目，生成默认题目
    if len(questions) < request.question_count:
        default_questions = _generate_default_questions(request)
        questions.extend(default_questions[:request.question_count - len(questions)])
    
    return questions[:request.question_count]

def _generate_default_questions(request: CompanyInterviewRequest) -> list[InterviewQuestion]:
    """生成默认面试题"""
    default_questions = [
        f"请介绍一下你对{request.company_name}公司的了解？",
        f"为什么选择{request.company_name}公司？",
        f"你认为{request.position}这个职位需要具备哪些核心能力？",
        f"请描述一个你在{request.position}相关工作中遇到的挑战及解决方案？",
        f"你如何看待{request.company_name}所在行业的发展趋势？"
    ]
    
    questions = []
    for q_text in default_questions:
        question = InterviewQuestion(
            question=q_text,
            difficulty=request.difficulty,
            category="综合类",
            knowledge_points=[]
        )
        questions.append(question)
    
    return questions
