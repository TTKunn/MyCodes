import torch
import numpy as np
a = torch.Tensor([[1,2],[3,4]])
print(a)
print(a.type())
# 上面输出的类型是FloatTensor

# a=torch.Tensor(2,3)
# print(a)
# print(a.type())
#
# a = torch.ones(2,2)
# print(a)
# print(a.type())
# # 全1 Tensor
#
# a = torch.zeros(2,2)
# print(a)
# print(a.type())
# # 全0 Tenseor
#
# a = torch.eye(2,2)
# print(a)
# print(a.type())
#
# b = torch.Tensor([[1,2],[3,4],[5,6]])
# a = torch.zeros_like(b)
# print(a)
#
# a = torch.rand(2,2)
# print(a)
# print(a.type())
# # 随机生成tensor
#
# a = torch.normal(mean=0.0,std=torch.rand(5))
# # 生成一个包含5个随机数的一维张量a。这些随机数从不同正态分布中采样得到，
# # 每个随机数的标准差是随机生成的，均值固定为0
# print("一维正态分布张量：",a)
#
# a = torch.normal(mean=0.0, std=0.5, size=(3, 3))
# # 生成一个固定均值为0，标准差为0.5，3x3的二维张量。
# print("二维正态分布张量：",a)
#
# a = torch.normal(mean=torch.rand(5),std=torch.rand(5))
# print(a)
#
#
# data = np.array([1, 2, 3])
#
# Tensor = torch.Tensor(data)
# tensor = torch.tensor(data)
# from_numpy = torch.from_numpy(data)
# as_tensor = torch.as_tensor(data)
# print('输出的结果：')
# print(Tensor)
# print(tensor)
# print(from_numpy)
# print(as_tensor)
#
# print('输出的类型：')
# print(Tensor.dtype)
# print(tensor.dtype)
# print(from_numpy.dtype)
# print(as_tensor.dtype)


dev = torch.device('cpu')
dev = torch.device('cuda:0')
a = torch.tensor([[1,2],[3,4]],device=dev)
print (a)
print(a.type())

torch.sparse_coo_tensor()