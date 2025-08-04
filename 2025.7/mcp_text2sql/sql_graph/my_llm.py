from langchain_openai import ChatOpenAI
from zhipuai import ZhipuAI

from sql_graph.env_utils import ZHIPU_API_KEY, OPENAI_API_KEY, DEEPSEEK_API_KEY

zhipuai_client = ZhipuAI(api_key=ZHIPU_API_KEY)  # 填写您自己的APIKey

#
# ✅ 当前激活：智谱AI GLM-4配置
llm = ChatOpenAI(  # zhipuai的
    temperature=0,
    model='glm-4-air-250414',
    api_key=ZHIPU_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/")


# llm = ChatOpenAI(  # openai的
#     temperature=0,
#     model='gpt-4o-mini',
#     api_key=OPENAI_API_KEY,
#     base_url="https://xiaoai.plus/v1")


# llm = ChatOpenAI(
#     temperature=0.5,
#     model='deepseek-chat',
#     api_key=DEEPSEEK_API_KEY,
#     base_url="https://api.deepseek.com")


# ❌ 本地Qwen3配置（已禁用）
# llm = ChatOpenAI(
#     temperature=0,
#     model="qwen3-8b",
#     openai_api_key="EMPTY",
#     openai_api_base="http://localhost:6006/v1",
#     extra_body={"chat_template_kwargs": {"enable_thinking": False}},
# )