# 工具
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from pandas.io.sql import get_schema

from SqlGraph.my_llm import llm

db = SQLDatabase.from_uri('sqlite:///../chinook.db')
toolkit = SQLDatabaseToolkit(db=db,llm=llm)

tools = toolkit.get_tools()

# 获取表结构的langchain内置工具
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")

print(get_schema_tool.invoke('employees'))
