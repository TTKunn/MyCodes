#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置测试脚本 - 验证智谱AI配置是否正确
"""

print("🔧 开始测试项目配置...")

# 测试1：检查环境变量
try:
    from sql_graph.env_utils import ZHIPU_API_KEY
    if ZHIPU_API_KEY:
        print("✅ 环境变量配置成功，ZHIPU_API_KEY已读取")
        print(f"   API Key前缀: {ZHIPU_API_KEY[:10]}...")
    else:
        print("❌ 未找到ZHIPU_API_KEY，请检查.env文件")
        exit(1)
except Exception as e:
    print(f"❌ 环境变量读取失败: {e}")
    exit(1)

# 测试2：检查LLM配置
try:
    from sql_graph.my_llm import llm
    print("✅ LLM配置成功")
    print(f"   模型: {llm.model_name}")
    print(f"   API地址: {llm.openai_api_base}")
except Exception as e:
    print(f"❌ LLM配置失败: {e}")
    exit(1)

# 测试3：测试LLM连接
try:
    print("🔍 测试智谱AI连接...")
    response = llm.invoke("你好，请简单回复一下")
    print(f"✅ 智谱AI连接成功!")
    print(f"   回复: {response.content}")
except Exception as e:
    print(f"❌ 智谱AI连接失败: {e}")
    print("   请检查:")
    print("   1. API Key是否正确")
    print("   2. 网络连接是否正常")
    print("   3. 智谱AI账户余额是否充足")

print("\n🎉 配置测试完成!")