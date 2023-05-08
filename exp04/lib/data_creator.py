import random
import json
# 生成11 个大小为10^6的整数数据集，第𝑖个子集中存在元素重复106 ×10 × i %,i = 0,1,2, ⋯ ,10
N = 100000
createVar = locals()
A = []
for i in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    m = N - int(N * i)  # 不重复的元素个数
    n = int(N * i)  # 重复元素个数
    A_m = []  # 不重复元素集合
    A_n = []  # 重复元素集合
    while len(A_m) < m:
        l = random.randint(0, N)
        if l not in A_m:
            A_m.append(l)
    k = random.randint(0, N)
    A_n = [k] * n
    A_mn = A_m + A_n
    random.shuffle(A_mn)
    j = int(i * 10)
    createVar['A' + str(j)] = A_mn
    A.append(createVar['A' + str(j)])
    # print(len(A))
    A_m = []
    A_n = []
with open('data.txt', 'w') as f:
    json.dump(A, f)
print("The datasets are created !")
with open('data.txt', 'r') as f:
    A = json.load(f)
print(A)
