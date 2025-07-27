import torch

a = torch.Tensor([[1,2],[3,4]])
print(a)
print(a.type())
# 上面输出的类型是FloatTensor

a=torch.Tensor(2,3)
print(a)
print(a.type())
