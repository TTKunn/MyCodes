from contextlib import asynccontextmanager

from langchain_mcp_adapters.client import MultiServerMCPClient

from McpServer.mcp_tools import mcp_server

mcp_server_config = {
    "url": "http://localhost:8000/sse",
    "transport": "sse"
}

@asynccontextmanager # 装饰器作用：快速创建异步的上下文管理器，使得异步资源的获取和释放可以和同步一样使用async with语法
async def make_graph():
# 定义并编译工作流
    async with MultiServerMCPClient({'lx_mcp':mcp_server_config}) as client;