# import torch
# dev = torch.device("cuda")
# a = torch.tensor([1, 2, 3],
#                  dtype = torch.float32,
#                  device = dev)
# print(a)
#
#
# i = torch.tensor([[1, 2, 3],[0,1,2]])
# v = torch.tensor([1,2,3])
# a = torch.sparse_coo_tensor(i,v,(4,4),
#                             dtype = torch.float32,
#                             device = dev).to_dense()
#
# print(a)

import torch

# 创建两个张量
a = torch.tensor([1, 2, 3], dtype=torch.float32)
b = torch.tensor([4, 5, 6], dtype=torch.float32)

# 方法1：使用运算符
c = a + b
print("a + b           = ",c)

# 方法2：使用torch.add()函数
d = torch.add(a, b)
print("torch.add(a, b) = ", d)

# 与标量相加
e = a + 10
print("a + 10          = ", e)
f = torch.add(a, 10)
print("torch.add(a, 10) :", f)

# 方法3：使用a.add()或a.add_()
g = a.add(b)
print("原张量 a          :", a)    # 原张量 a 未被修改
print("a.add(b)计算结果  :", g)

h = a.add_(b)
print("张量 a            :", a)    # 原张量 a 被修改
print("a.add_(b)计算结果 :", h)
