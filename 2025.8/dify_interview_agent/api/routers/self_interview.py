"""
自选知识点面试模块
"""
from fastapi import APIRouter, HTTPException
import json

from api.models import (
    SelfInterviewRequest,
    SelfInterviewResponse,
    InterviewQuestion
)
from api.dify_client import dify_manager

router = APIRouter()

@router.post("/generate_self_interview/", response_model=SelfInterviewResponse)
async def generate_self_interview(request: SelfInterviewRequest):
    """
    生成自选知识点面试题
    
    根据用户提供的技术知识点或技能关键词，生成相关的面试题，
    便于用户针对特定领域进行重点准备。
    """
    try:
        # 获取自选知识点面试专用的Dify客户端
        client = dify_manager.get_client("self")
        
        # 构建提示词
        prompt = f"""
        请根据以下技术知识点或技能关键词生成{request.question_count}道{request.difficulty}难度的面试题：

        关键词：{request.keywords}
        难度等级：{request.difficulty}
        题目数量：{request.question_count}

        要求：
        1. 题目要紧密围绕给定的关键词
        2. 涵盖理论基础、实践应用、问题解决等多个维度
        3. 难度要符合{request.difficulty}水平
        4. 题目要有深度和实用性
        5. 包含一些实际场景应用的问题

        请以JSON格式返回，包含以下字段：
        {{
            "questions": [
                {{
                    "question": "具体题目内容",
                    "difficulty": "难度等级",
                    "category": "题目分类（如基础理论、实践应用、架构设计等）",
                    "knowledge_points": ["相关知识点1", "相关知识点2"]
                }}
            ]
        }}
        """
        
        # 调用Dify API
        response = await client.chat_completion(
            query=prompt,
            user_id="self_interview_system",
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
                
                return SelfInterviewResponse(
                    questions=questions,
                    keywords=request.keywords,
                    total_count=len(questions)
                )
            else:
                raise ValueError("无法解析JSON响应")
                
        except (json.JSONDecodeError, ValueError) as e:
            # 如果JSON解析失败，尝试从文本中提取题目
            questions = _extract_questions_from_text(answer, request)
            
            return SelfInterviewResponse(
                questions=questions,
                keywords=request.keywords,
                total_count=len(questions)
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成面试题失败: {str(e)}")

def _extract_questions_from_text(text: str, request: SelfInterviewRequest) -> list[InterviewQuestion]:
    """从文本中提取面试题"""
    questions = []
    lines = text.split('\n')
    
    current_question = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是题目行
        if any(marker in line for marker in ['?', '？', '1.', '2.', '3.', '4.', '5.']) or \
           (line and (line[0].isdigit() or line.startswith('题目'))):
            
            if current_question:
                # 保存上一个题目
                question = InterviewQuestion(
                    question=current_question.strip(),
                    difficulty=request.difficulty,
                    category=_categorize_question(current_question, request.keywords),
                    knowledge_points=_extract_knowledge_points(current_question, request.keywords)
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
            category=_categorize_question(current_question, request.keywords),
            knowledge_points=_extract_knowledge_points(current_question, request.keywords)
        )
        questions.append(question)
    
    # 如果没有提取到足够的题目，生成默认题目
    if len(questions) < request.question_count:
        default_questions = _generate_default_questions(request)
        questions.extend(default_questions[:request.question_count - len(questions)])
    
    return questions[:request.question_count]

def _categorize_question(question: str, keywords: str) -> str:
    """根据题目内容和关键词分类"""
    question_lower = question.lower()
    keywords_lower = keywords.lower()
    
    if any(word in question_lower for word in ['原理', '概念', '定义', '什么是']):
        return "基础理论"
    elif any(word in question_lower for word in ['实现', '如何', '怎么', '步骤']):
        return "实践应用"
    elif any(word in question_lower for word in ['架构', '设计', '方案', '选择']):
        return "架构设计"
    elif any(word in question_lower for word in ['优化', '性能', '问题', '解决']):
        return "问题解决"
    elif any(word in question_lower for word in ['区别', '比较', '对比']):
        return "对比分析"
    else:
        return "综合应用"

def _extract_knowledge_points(question: str, keywords: str) -> list[str]:
    """从题目中提取知识点"""
    knowledge_points = []
    
    # 将关键词分割并添加到知识点中
    keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    knowledge_points.extend(keyword_list)
    
    # 根据题目内容添加额外的知识点
    question_lower = question.lower()
    
    # 技术相关知识点映射
    tech_mapping = {
        'redis': ['缓存', '数据结构', '持久化'],
        'mysql': ['数据库', 'SQL', '索引', '事务'],
        'java': ['面向对象', 'JVM', '多线程', '集合框架'],
        'python': ['数据结构', '装饰器', '生成器', 'GIL'],
        'spring': ['IOC', 'AOP', '依赖注入', 'MVC'],
        'docker': ['容器化', '镜像', '编排'],
        'kubernetes': ['容器编排', '微服务', '集群管理']
    }
    
    for tech, points in tech_mapping.items():
        if tech in question_lower:
            knowledge_points.extend(points)
    
    # 去重并返回
    return list(set(knowledge_points))

def _generate_default_questions(request: SelfInterviewRequest) -> list[InterviewQuestion]:
    """生成默认面试题"""
    keywords = request.keywords
    
    default_questions = [
        f"请详细解释{keywords}的核心概念和原理？",
        f"在实际项目中，你是如何使用{keywords}的？请举个具体例子。",
        f"{keywords}有哪些优缺点？在什么场景下会选择使用它？",
        f"请描述一个使用{keywords}解决技术难题的经历？",
        f"如何优化{keywords}的性能？有哪些最佳实践？"
    ]
    
    questions = []
    for i, q_text in enumerate(default_questions):
        question = InterviewQuestion(
            question=q_text,
            difficulty=request.difficulty,
            category=["基础理论", "实践应用", "对比分析", "问题解决", "性能优化"][i],
            knowledge_points=_extract_knowledge_points(q_text, keywords)
        )
        questions.append(question)
    
    return questions
