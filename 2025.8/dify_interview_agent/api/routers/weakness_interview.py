"""
薄弱知识点强化模块
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import json
from datetime import datetime

from api.models import (
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    SaveEvaluationRequest,
    EvaluationResult,
    WrongAnswer,
    WeaknessAnalysis
)
from api.dify_client import dify_client
from utils.file_handler import DataManager

router = APIRouter()

@router.post("/submit_answer/", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """
    提交答题（仅评估，不落盘）
    
    对用户的答案进行评估，分析薄弱点，但不保存到错题册。
    用于实时反馈和评估。
    """
    try:
        # 使用统一的Dify客户端
        
        # 构建评估提示词
        prompt = f"""
        请对以下面试题的用户答案进行详细评估：

        题目：{request.question}
        用户答案：{request.user_answer}
        知识点标签：{request.knowledge_points or []}

        请从以下维度进行评估：
        1. 答案正确性和完整性
        2. 技术深度和广度
        3. 逻辑思维和表达能力
        4. 实践经验体现

        请以JSON格式返回评估结果，包含以下字段：
        {{
            "score": 85,  // 得分(0-100)
            "knowledge_points": ["知识点1", "知识点2"],  // 涉及的知识点
            "weak_aspects": ["薄弱方面1", "薄弱方面2"],  // 薄弱的方面
            "detailed_feedback": {{
                "正确性": "具体反馈内容",
                "完整性": "具体反馈内容",
                "技术深度": "具体反馈内容",
                "表达能力": "具体反馈内容"
            }},
            "improvement_suggestions": [
                "改进建议1",
                "改进建议2",
                "改进建议3"
            ]
        }}
        """
        
        # 调用Dify API进行评估
        response = await dify_client.chat_completion(
            query=prompt,
            user_id=f"weakness_eval_{request.user_id}",
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
                evaluation_data = json.loads(json_str)
                
                return SubmitAnswerResponse(
                    score=evaluation_data.get("score", 0),
                    knowledge_points=evaluation_data.get("knowledge_points", request.knowledge_points or []),
                    weak_aspects=evaluation_data.get("weak_aspects", []),
                    detailed_feedback=evaluation_data.get("detailed_feedback", {}),
                    improvement_suggestions=evaluation_data.get("improvement_suggestions", [])
                )
            else:
                raise ValueError("无法解析JSON响应")
                
        except (json.JSONDecodeError, ValueError):
            # 如果JSON解析失败，返回基础评估
            return _generate_basic_evaluation(request, answer)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"答案评估失败: {str(e)}")

@router.post("/save_evaluation/")
async def save_evaluation(request: SaveEvaluationRequest):
    """
    保存评估结果（落盘到错题册）
    
    将评估结果保存到用户的错题册中，用于后续的薄弱点分析。
    """
    try:
        # 构建错题记录
        wrong_answer = {
            "question": request.question,
            "user_answer": request.user_answer,
            "evaluation_result": request.evaluation_result.dict(),
            "created_at": datetime.now().isoformat()
        }
        
        # 保存到错题册
        await DataManager.save_wrong_answer(request.user_id, wrong_answer)
        
        return {
            "code": 200,
            "message": "评估结果已保存到错题册",
            "data": {
                "user_id": request.user_id,
                "saved_at": wrong_answer["created_at"]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存评估结果失败: {str(e)}")

@router.get("/wrong_answers/{user_id}")
async def get_wrong_answers(user_id: str):
    """
    获取错题册
    
    返回用户的所有错题记录，按时间倒序排列。
    """
    try:
        wrong_answers = await DataManager.get_wrong_answers(user_id)
        
        # 按时间倒序排列
        wrong_answers.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return {
            "code": 200,
            "message": "获取错题册成功",
            "data": {
                "user_id": user_id,
                "wrong_answers": wrong_answers,
                "total_count": len(wrong_answers)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取错题册失败: {str(e)}")

@router.get("/weakness_analysis/{user_id}")
async def get_weakness_analysis(user_id: str):
    """
    获取薄弱点分析
    
    基于用户的错题记录，分析薄弱知识点和方面，提供改进建议。
    """
    try:
        wrong_answers = await DataManager.get_wrong_answers(user_id)
        
        if not wrong_answers:
            return {
                "code": 200,
                "message": "暂无错题数据",
                "data": {
                    "user_id": user_id,
                    "analysis": None
                }
            }
        
        # 分析薄弱点
        analysis = _analyze_weakness(wrong_answers)
        
        return {
            "code": 200,
            "message": "薄弱点分析完成",
            "data": {
                "user_id": user_id,
                "analysis": analysis,
                "total_wrong_answers": len(wrong_answers)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"薄弱点分析失败: {str(e)}")

def _generate_basic_evaluation(request: SubmitAnswerRequest, answer_text: str) -> SubmitAnswerResponse:
    """生成基础评估结果"""
    # 简单的文本分析来估算得分
    answer_length = len(request.user_answer)
    if answer_length < 50:
        score = 30
    elif answer_length < 200:
        score = 60
    else:
        score = 75
    
    return SubmitAnswerResponse(
        score=score,
        knowledge_points=request.knowledge_points or [],
        weak_aspects=["表达完整性", "技术深度"],
        detailed_feedback={
            "整体评价": answer_text[:200] + "..." if len(answer_text) > 200 else answer_text
        },
        improvement_suggestions=[
            "建议更详细地阐述技术细节",
            "可以结合实际项目经验进行说明",
            "注意逻辑结构的清晰性"
        ]
    )

def _analyze_weakness(wrong_answers: List[Dict[str, Any]]) -> WeaknessAnalysis:
    """分析薄弱点"""
    weak_knowledge_points = {}
    weak_aspects = {}
    all_suggestions = []
    
    for wrong_answer in wrong_answers:
        evaluation = wrong_answer.get("evaluation_result", {})
        
        # 统计薄弱知识点
        knowledge_points = evaluation.get("knowledge_points", [])
        for kp in knowledge_points:
            weak_knowledge_points[kp] = weak_knowledge_points.get(kp, 0) + 1
        
        # 统计薄弱方面
        weak_aspects_list = evaluation.get("weak_aspects", [])
        for wa in weak_aspects_list:
            weak_aspects[wa] = weak_aspects.get(wa, 0) + 1
        
        # 收集改进建议
        suggestions = evaluation.get("improvement_suggestions", [])
        all_suggestions.extend(suggestions)
    
    # 生成改进优先级（按出现频次排序）
    improvement_priority = sorted(weak_aspects.keys(), key=lambda x: weak_aspects[x], reverse=True)
    
    # 去重并选择最常见的建议
    unique_suggestions = list(set(all_suggestions))
    suggested_practice = unique_suggestions[:5]  # 取前5个建议
    
    return WeaknessAnalysis(
        weak_knowledge_points=weak_knowledge_points,
        weak_aspects=weak_aspects,
        improvement_priority=improvement_priority,
        suggested_practice=suggested_practice
    )
