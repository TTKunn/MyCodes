from fastapi import FastAPI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek    # 导入 DeepSeek 集成类
from langserve import add_routes
import os
import sys
import io

# 解决编码问题 - 仅添加了这部分编码设置
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 1. 配置代理（如果需要）
os.environ['http_proxy'] = '127.0.0.1:7890'
os.environ['https_proxy'] = '127.0.0.1:7890'

# 2. 配置 DeepSeek API 密钥（请替换为实际有效密钥）
os.environ["DEEPSEEK_API_KEY"] = "sk-a4d382212a5e41c9a236ab1c73c5cf79"

# 3. 初始化 DeepSeek 模型
model = ChatDeepSeek(model="deepseek-chat", timeout=30)  # 增加超时设置

# msg = [
#     SystemMessage(content='请将下面的文本内容翻译为英语：'),
#     HumanMessage(content='你好，请问你要去哪里')
# ]

parser = StrOutputParser()

# 提示词模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system','请将以下的内容翻译成{language}'),
    ('user',"{text}")
])

chain = prompt_template | model | parser

# 执行调用
print(chain.invoke({'language':'English','text':'我想学英语'}))

# 封装api
app = FastAPI(title = '我的langchain服务',version='1.0')

add_routes(
    app,
    chain,
    path="/chain_demo"
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='localhost', port=8000)