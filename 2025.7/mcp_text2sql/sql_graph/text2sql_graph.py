from contextlib import asynccontextmanager
from typing import Literal

from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, create_react_agent

from sql_graph.my_llm import llm
from sql_graph.my_state import SQLState
from sql_graph.tools_node import generate_query_system_prompt, query_check_system, call_get_schema, get_schema_node

mcp_server_config = {
    "url": "http://localhost:8000/sse",
    "transport": "sse"
}


def should_continue(state: SQLState) -> Literal[END, "check_query"]:
    """条件路由的，动态边"""
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return END
    else:
        return "check_query"


@asynccontextmanager  # 作用：用于快速创建异步上下文管理器。它使得异步资源的获取和释放可以像同步代码一样通过 async with 语法优雅地管理。
async def make_graph():
    """定义，并且编译工作流"""
    # 修复：使用新版本 langchain-mcp-adapters 的API格式
    client = MultiServerMCPClient({'lx_mcp': mcp_server_config})
    try:
        tools = await client.get_tools()
        # 所有表名列表的工具
        list_tables_tool = next(tool for tool in tools if tool.name == "list_tables_tool")
        # 执行sql的工具
        db_query_tool = next(tool for tool in tools if tool.name == "db_query_tool")

        def call_list_tables(state: SQLState):
            """第一个节点 """
            tool_call = {
                "name": "list_tables_tool",
                "args": {},
                "id": "abc123",
                "type": "tool_call",
            }
            tool_call_message = AIMessage(content="", tool_calls=[tool_call])

            # tool_message = list_tables_tool.invoke(tool_call)  # 调用工具
            #
            # response = AIMessage(f"所有可用的表: {tool_message.content}")

            # return {"messages": [tool_call_message, tool_message, response]}
            return {"messages": [tool_call_message]}


        # 第二个节点
        list_tables_tool = ToolNode([list_tables_tool], name="list_tables_tool")

        def generate_query(state: SQLState):
            """第五个节点: 生成SQL语句"""
            system_message = {
                "role": "system",
                "content": generate_query_system_prompt,
            }
            # 这里不强制工具调用，允许模型在获得解决方案时自然响应
            llm_with_tools = llm.bind_tools([db_query_tool])
            resp = llm_with_tools.invoke([system_message] + state['messages'])
            return {'messages': [resp]}

        def check_query(state: SQLState):
            """第六个节点: 检查SQL语句"""
            system_message = {
                "role": "system",
                "content": query_check_system,
            }
            tool_call = state["messages"][-1].tool_calls[0]
            # 得到生成后的SQL
            user_message = {"role": "user", "content": tool_call["args"]["query"]}
            llm_with_tools = llm.bind_tools([db_query_tool], tool_choice='any')
            response = llm_with_tools.invoke([system_message, user_message])
            response.id = state["messages"][-1].id

            return {"messages": [response]}

        # 第 七个节点
        run_query_node = ToolNode([db_query_tool], name="run_query")

        workflow = StateGraph(SQLState)
        workflow.add_node(call_list_tables)
        workflow.add_node(list_tables_tool)
        workflow.add_node(call_get_schema)
        workflow.add_node(get_schema_node)
        workflow.add_node(generate_query)
        workflow.add_node(check_query)
        workflow.add_node(run_query_node)

        workflow.add_edge(START, "call_list_tables")
        workflow.add_edge("call_list_tables", "list_tables_tool")
        workflow.add_edge("list_tables_tool", "call_get_schema")
        workflow.add_edge("call_get_schema", "get_schema")
        workflow.add_edge("get_schema", "generate_query")
        workflow.add_conditional_edges('generate_query', should_continue)
        workflow.add_edge("check_query", "run_query")
        workflow.add_edge("run_query", "generate_query")

        graph = workflow.compile()
        yield graph
        
    finally:
        # 🧹 清理：关闭MCP客户端连接
        try:
            if hasattr(client, 'close'):
                await client.close()
        except Exception as e:
            print(f"Warning: 关闭MCP客户端时出现警告: {e}")
