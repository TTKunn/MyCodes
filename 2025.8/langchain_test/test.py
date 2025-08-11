from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.schema import OutputParserException

# 1. 定义响应模式
response_schemas = [
    ResponseSchema(
        name="answer",
        description="对问题的回答，用简洁明了的语言",
        type="string"
    ),
    ResponseSchema(
        name="source",
        description="回答的来源或依据，可以是书籍、文章或个人知识",
        type="string"
    ),
    ResponseSchema(
        name="confidence",
        description="对回答的信心程度，范围0-100的整数",
        type="integer"
    )
]

# 2. 创建结构化输出解析器
parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 3. 获取并打印格式化指令
format_instructions = parser.get_format_instructions()
print("--- 格式化指令 ---")
print(format_instructions)

# 4. 测试解析有效输出
valid_output = '''```json
{
    "answer": "LangChain是一个用于构建基于语言模型的应用程序的框架。",
    "source": "公开文档和官方网站",
    "confidence": 95
}
```'''

try:
    result_valid = parser.parse(valid_output)
    print("\n--- 有效输出解析结果 ---")
    print(f"类型: {type(result_valid)}")
    print(f"内容: {result_valid}")
    print(f"访问字段: 回答: {result_valid['answer']}, 信心度: {result_valid['confidence']}%")
except OutputParserException as e:
    print(f"\n有效输出解析错误: {e}")

# 5. 测试解析格式正确但内容不完整的输出（缺少'source'字段）
invalid_output_missing_field = '''```json
{
    "answer": "LangChain是一个Python框架。",
    "confidence": 90
}
```'''

try:
    print("\n--- 测试内容不完整的输出 ---")
    result_invalid = parser.parse(invalid_output_missing_field)
    print("解析结果:", result_invalid)
except OutputParserException as e:
    print(f"解析错误: {e}")