from zhipuai import ZhipuAI
import os

# 替换为你的智谱AI API Key
API_KEY = "332f9115b1a74d698b84f282bf809541.JGymaQNrJgaFHCvN"


def test_zhipu_api():
    try:
        # 初始化客户端
        client = ZhipuAI(api_key=API_KEY)

        # 调用一个简单的对话接口测试
        response = client.chat.completions.create(
            model="glm-4-air-250414",  # 使用智谱的GLM-4模型
            messages=[
                {"role": "user", "content": "你好，你是什么模型？"}
            ]
        )

        # 打印返回结果
        print("API调用成功！返回结果：")
        print(response.choices[0].message.content)
        return True

    except Exception as e:
        print(f"API调用失败：{str(e)}")
        return False


if __name__ == "__main__":
    test_zhipu_api()
