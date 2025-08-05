from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from SqlGraph.my_llm import llm

if __name__ == '__main__':
    # db = SQLDatabase.from_uri('sqlite:///../chinook.db')
    # toolkit = SQLDatabaseToolkit(db=db,llm=llm)

    # tools = toolkit.get_tools()
    # for tool in tools:
    #     print("工具名：",tool.name,"工具描述：",tool.description)

    # list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")

    # response = list_tables_tool.invoke("")
    # print("response内容：",response)
    pass