"""
API测试脚本
"""
import requests
import json
import time

BASE_URL = "http://localhost:8010"

def test_company_interview():
    """测试公司题库面试"""
    print("=== 测试公司题库面试 ===")
    
    url = f"{BASE_URL}/interview/company/generate_company_questions/"
    data = {
        "company_name": "阿里巴巴",
        "position": "Java后端开发",
        "difficulty": "中级",
        "question_count": 3
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print()

def test_self_interview():
    """测试自选知识点面试"""
    print("=== 测试自选知识点面试 ===")
    
    url = f"{BASE_URL}/interview/self/generate_self_interview/"
    data = {
        "keywords": "Redis缓存优化",
        "difficulty": "高级",
        "question_count": 3
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print()

def test_weakness_interview():
    """测试薄弱知识点强化"""
    print("=== 测试薄弱知识点强化 ===")
    
    # 1. 提交答题评估
    url = f"{BASE_URL}/interview/weakness/submit_answer/"
    data = {
        "user_id": "test_user_123",
        "question": "请解释Redis的持久化机制",
        "user_answer": "Redis有RDB和AOF两种持久化方式，RDB是快照方式，AOF是日志方式。",
        "knowledge_points": ["Redis", "持久化", "RDB", "AOF"]
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"提交答题 - 状态码: {response.status_code}")
        result = response.json()
        print(f"评估结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # 2. 保存评估结果
        if response.status_code == 200:
            save_url = f"{BASE_URL}/interview/weakness/save_evaluation/"
            save_data = {
                "user_id": "test_user_123",
                "question": data["question"],
                "user_answer": data["user_answer"],
                "evaluation_result": {
                    "score": result.get("score", 0),
                    "knowledge_points": result.get("knowledge_points", []),
                    "weak_aspects": result.get("weak_aspects", []),
                    "detailed_feedback": result.get("detailed_feedback", {}),
                    "improvement_suggestions": result.get("improvement_suggestions", [])
                }
            }
            
            save_response = requests.post(save_url, json=save_data, timeout=30)
            print(f"保存评估 - 状态码: {save_response.status_code}")
            print(f"保存结果: {json.dumps(save_response.json(), ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"请求失败: {e}")
    
    print()

def test_resume_interview():
    """测试简历定制面试"""
    print("=== 测试简历定制面试 ===")
    
    url = f"{BASE_URL}/interview/resume/upload_resume/"
    data = {
        "resume_text": """
        张三
        Java后端开发工程师
        
        教育背景：
        2018-2022 北京大学 计算机科学与技术 本科
        
        工作经历：
        2022-至今 阿里巴巴 Java开发工程师
        - 负责电商平台后端开发
        - 使用Spring Boot、MySQL、Redis等技术
        - 参与微服务架构设计
        
        技能：
        Java、Spring、MySQL、Redis、Docker、Kubernetes
        """,
        "user_id": "test_user_123",
        "target_position": "高级Java开发工程师"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print()

def test_knowledge_management():
    """测试知识库管理"""
    print("=== 测试知识库管理 ===")
    
    # 1. 查询知识库
    query_url = f"{BASE_URL}/knowlage/query/"
    query_data = {
        "query": "什么是Redis？",
        "kb_name": "test_kb"
    }
    
    try:
        response = requests.post(query_url, json=query_data, timeout=30)
        print(f"知识库查询 - 状态码: {response.status_code}")
        print(f"查询结果: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"查询失败: {e}")
    
    # 2. 列出知识库
    list_url = f"{BASE_URL}/knowlage/list_knowledge_bases/"
    
    try:
        response = requests.get(list_url, timeout=30)
        print(f"知识库列表 - 状态码: {response.status_code}")
        print(f"知识库列表: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"获取列表失败: {e}")
    
    print()

def test_health_check():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"健康检查失败: {e}")
    
    print()

def main():
    """运行所有测试"""
    print("开始API测试...")
    print(f"测试地址: {BASE_URL}")
    print("=" * 50)
    
    # 健康检查
    test_health_check()
    
    # 各模块功能测试
    test_company_interview()
    test_self_interview()
    test_weakness_interview()
    test_resume_interview()
    test_knowledge_management()
    
    print("测试完成！")

if __name__ == "__main__":
    main()
