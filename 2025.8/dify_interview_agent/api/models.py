"""
API数据模型定义
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum

class DifficultyLevel(str, Enum):
    """难度等级"""
    BEGINNER = "初级"
    INTERMEDIATE = "中级"
    ADVANCED = "高级"

class ResponseMode(str, Enum):
    """响应模式"""
    STREAMING = "streaming"
    BLOCKING = "blocking"

# ============ 公司题库面试模块 ============
class CompanyInterviewRequest(BaseModel):
    """公司面试题生成请求"""
    company_name: str = Field(..., description="公司名称")
    position: str = Field(..., description="职位名称")
    difficulty: DifficultyLevel = Field(DifficultyLevel.INTERMEDIATE, description="难度等级")
    question_count: int = Field(5, ge=1, le=20, description="题目数量")

class InterviewQuestion(BaseModel):
    """面试题"""
    question: str = Field(..., description="题目内容")
    difficulty: str = Field(..., description="难度等级")
    category: Optional[str] = Field(None, description="题目分类")
    knowledge_points: Optional[List[str]] = Field(None, description="知识点")

class CompanyInterviewResponse(BaseModel):
    """公司面试题响应"""
    questions: List[InterviewQuestion] = Field(..., description="面试题列表")
    company_name: str = Field(..., description="公司名称")
    position: str = Field(..., description="职位名称")
    total_count: int = Field(..., description="题目总数")

# ============ 自选知识点面试模块 ============
class SelfInterviewRequest(BaseModel):
    """自选知识点面试请求"""
    keywords: str = Field(..., description="技术知识点或技能关键词")
    difficulty: DifficultyLevel = Field(DifficultyLevel.INTERMEDIATE, description="难度等级")
    question_count: int = Field(5, ge=1, le=20, description="题目数量")

class SelfInterviewResponse(BaseModel):
    """自选知识点面试响应"""
    questions: List[InterviewQuestion] = Field(..., description="面试题列表")
    keywords: str = Field(..., description="关键词")
    total_count: int = Field(..., description="题目总数")

# ============ 薄弱知识点强化模块 ============
class SubmitAnswerRequest(BaseModel):
    """提交答题请求"""
    user_id: str = Field(..., description="用户ID")
    question: str = Field(..., description="题目内容")
    user_answer: str = Field(..., description="用户答案")
    knowledge_points: Optional[List[str]] = Field(None, description="知识点标签")

class EvaluationResult(BaseModel):
    """评估结果"""
    score: int = Field(..., ge=0, le=100, description="得分(0-100)")
    knowledge_points: List[str] = Field(..., description="涉及的知识点")
    weak_aspects: List[str] = Field(..., description="薄弱方面")
    detailed_feedback: Dict[str, Any] = Field(..., description="详细反馈")
    improvement_suggestions: List[str] = Field(..., description="改进建议")

class SubmitAnswerResponse(BaseModel):
    """提交答题响应"""
    score: int = Field(..., description="得分")
    knowledge_points: List[str] = Field(..., description="知识点")
    weak_aspects: List[str] = Field(..., description="薄弱方面")
    detailed_feedback: Dict[str, Any] = Field(..., description="详细反馈")
    improvement_suggestions: List[str] = Field(..., description="改进建议")

class SaveEvaluationRequest(BaseModel):
    """保存评估结果请求"""
    user_id: str = Field(..., description="用户ID")
    question: str = Field(..., description="题目内容")
    user_answer: str = Field(..., description="用户答案")
    evaluation_result: EvaluationResult = Field(..., description="评估结果")

class WrongAnswer(BaseModel):
    """错题记录"""
    question: str = Field(..., description="题目")
    user_answer: str = Field(..., description="用户答案")
    correct_answer: Optional[str] = Field(None, description="正确答案")
    evaluation_result: EvaluationResult = Field(..., description="评估结果")
    created_at: str = Field(..., description="创建时间")
    category: Optional[str] = Field(None, description="题目分类")

class WeaknessAnalysis(BaseModel):
    """薄弱点分析"""
    weak_knowledge_points: Dict[str, int] = Field(..., description="薄弱知识点统计")
    weak_aspects: Dict[str, int] = Field(..., description="薄弱方面统计")
    improvement_priority: List[str] = Field(..., description="改进优先级")
    suggested_practice: List[str] = Field(..., description="建议练习")

# ============ 简历定制面试模块 ============
class ResumeInterviewRequest(BaseModel):
    """简历面试请求"""
    resume_text: str = Field(..., description="简历内容")
    user_id: Optional[str] = Field(None, description="用户ID，可选")
    target_position: Optional[str] = Field(None, description="目标职位，可选")

class ResumeAnalysis(BaseModel):
    """简历分析结果"""
    education_background: List[str] = Field(..., description="教育背景")
    work_experience: List[str] = Field(..., description="工作经历")
    skills: List[str] = Field(..., description="技能")
    projects: List[str] = Field(..., description="项目经历")
    keywords: List[str] = Field(..., description="关键词")

class ResumeInterviewResponse(BaseModel):
    """简历面试响应"""
    analysis: ResumeAnalysis = Field(..., description="简历分析")
    questions: List[InterviewQuestion] = Field(..., description="面试题")
    total_count: int = Field(..., description="题目总数")

# ============ 知识库管理模块 ============
class KnowledgeUploadResponse(BaseModel):
    """知识库上传响应"""
    msg: str = Field(..., description="消息")
    segments: int = Field(..., description="分段数量")

class KnowledgeQueryRequest(BaseModel):
    """知识库查询请求"""
    query: str = Field(..., description="查询内容")
    kb_name: Optional[str] = Field(None, description="知识库名称")

class KnowledgeQueryResponse(BaseModel):
    """知识库查询响应"""
    answer: str = Field(..., description="答案")
    citations: List[Dict[str, Any]] = Field(..., description="引用来源")

# ============ 通用响应模型 ============
class BaseResponse(BaseModel):
    """基础响应模型"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="消息")
    data: Optional[Any] = Field(None, description="数据")

class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    detail: Optional[str] = Field(None, description="错误详情")
