from langchain_openai import ChatOpenAI
from zhipuai import ZhipuAI

from env_utils import ZHIPU_API_KEY, OPENAI_API_KEY, DEEPSEEK_API_KEY

zhipuai_client = ZhipuAI(api_key=ZHIPU_API_KEY)

# 配置LLM - 和主项目使用相同配置
llm = ChatOpenAI(
    temperature=0,
    model="qwen3-8b",
    openai_api_key="EMPTY",
    openai_api_base="http://localhost:6006/v1",
    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)
