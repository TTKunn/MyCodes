"""
AI面试系统主入口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from api.routers import (
    company_interview,
    self_interview, 
    weakness_interview,
    resume_interview,
    knowledge_management
)

# 创建FastAPI应用
app = FastAPI(
    title="AI面试系统 API",
    description="基于Dify的AI面试系统API封装",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(company_interview.router, prefix="/interview/company", tags=["公司题库面试"])
app.include_router(self_interview.router, prefix="/interview/self", tags=["自选知识点面试"])
app.include_router(weakness_interview.router, prefix="/interview/weakness", tags=["薄弱知识点强化"])
app.include_router(resume_interview.router, prefix="/interview/resume", tags=["简历定制面试"])
app.include_router(knowledge_management.router, prefix="/knowlage", tags=["知识库管理"])

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI面试系统 API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"内部服务器错误: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
