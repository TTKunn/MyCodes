# ====================================================================================
# MCP工具服务器 - 为AI模型提供数据库查询和网络搜索功能
# ====================================================================================

# 📦 导入必要的库
from langchain_community.utilities import SQLDatabase  # LangChain的SQL数据库工具类
from mcp.server import FastMCP                         # MCP快速服务器框架

# 导入智谱AI客户端（用于网络搜索功能）
from SqlGraph.my_llm import zhipuai_client

# ====================================================================================
# 🏗️ 服务器和数据库初始化
# ====================================================================================

# 创建MCP服务器实例
# 参数解释：
# - name: 服务器名称，用于标识这个MCP服务
# - instructions: 服务器描述信息
# - port: 服务器运行端口号，AI模型会连接到这个端口
mcp_server = FastMCP(
    name='lx-mcp', 
    instructions='我自己的MCP服务', 
    port=8000
)

# 连接到SQLite数据库
# URI格式解释：
# - sqlite:///  表示使用SQLite数据库
# - ../chinook.db  相对路径，上级目录的chinook.db文件
db = SQLDatabase.from_uri('sqlite:///../chinook.db')

# ====================================================================================
# 🔍 工具1：网络搜索工具
# ====================================================================================

# @装饰器语法说明：
# @mcp_server.tool() 是Python装饰器，用来"装饰"函数
# 作用：将普通函数注册成MCP工具，AI可以调用
# 参数：
# - 'my_search_tool': 工具名称（AI调用时使用这个名字）
# - description: 工具描述（告诉AI这个工具的用途）
@mcp_server.tool('my_search_tool', description='专门搜索互联网中的内容')
def my_search(query: str) -> str:
    """
    网络搜索功能函数
    
    函数签名解释：
    - query: str  参数名query，类型是字符串(str)
    - -> str      返回值类型是字符串(str)
    
    Args:
        query (str): 搜索关键词
        
    Returns:
        str: 搜索结果文本，多个结果用双换行分隔
    """
    
    # try-except语法：异常处理机制
    # try: 尝试执行可能出错的代码
    # except: 如果出错了，执行这里的代码
    try:
        # 调用智谱AI的网络搜索API
        # 方法链调用：zhipuai_client.web_search.web_search()
        response = zhipuai_client.web_search.web_search(
            search_engine="search-std",    # 搜索引擎类型
            search_query=query            # 搜索关键词
        )
        
        # 打印响应结果（用于调试）
        print(response)
        
        # if 条件判断：检查是否有搜索结果
        if response.search_result:
            # 列表推导式 + join方法：
            # [d.content for d in response.search_result] 提取每个结果的内容
            # "\n\n".join() 用双换行符连接所有内容
            return "\n\n".join([d.content for d in response.search_result])
            
    # Exception as e 语法：捕获任何异常，并将异常对象赋值给变量e
    except Exception as e:
        print(e)  # 打印错误信息
        return '没有搜索到任何内容！'  # 返回友好的错误提示

# ====================================================================================
# 📋 工具2：数据库表列表工具
# ====================================================================================

@mcp_server.tool('list_tables_tool', description='输入是一个空字符串, 返回数据库中的所有：以逗号分隔的表名字列表')
def list_tables_tool() -> str:
    """
    获取数据库中所有表的名称列表
    
    函数特点：
    - 无需输入参数（空参数列表）
    - 返回逗号分隔的表名字符串
    
    Returns:
        str: 逗号分隔的表名列表，如："Album, Artist, Customer, Employee"
    """
    
    # 方法链调用解释：
    # 1. db.get_usable_table_names() 获取所有可用表名，返回列表
    #    例如：['Album', 'Artist', 'Customer', 'Employee']
    # 2. ", ".join() 将列表用逗号和空格连接成字符串
    #    例如：'Album, Artist, Customer, Employee'
    return ", ".join(db.get_usable_table_names())

# ====================================================================================
# 💾 工具3：SQL查询执行工具
# ====================================================================================

@mcp_server.tool()
def db_query_tool(query: str) -> str:
    """
    执行SQL查询并返回结果
    
    这是整个系统的核心工具，负责执行AI生成的SQL语句
    
    安全特性：
    - 使用 run_no_throw 方法，即使SQL出错也不会让程序崩溃
    - 有完善的错误处理机制
    
    Args:
        query (str): 要执行的SQL查询语句
                    例如："SELECT * FROM Customer LIMIT 5"
        
    Returns:
        str: 查询结果或错误信息
             成功时返回查询结果的字符串表示
             失败时返回友好的错误提示
    """
    
    # 核心SQL执行语句
    # run_no_throw 方法说明：
    # - 执行SQL查询，但不抛出异常（no_throw = 不抛出）
    # - 如果查询成功，返回结果
    # - 如果查询失败，返回None或空字符串，而不是让程序崩溃
    result = db.run_no_throw(query)
    
    # 条件判断：检查查询是否成功
    # if not result: 意思是"如果result为空/None/False"
    if not result:
        return "错误: 查询失败。请修改查询语句后重试。"
    
    # 返回查询结果
    # result 可能是字符串格式的表格数据
    return result
