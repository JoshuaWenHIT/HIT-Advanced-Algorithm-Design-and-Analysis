#  An Approximation Algorithm Based on Greedy Strategy and an Approximation Algorithm Based on Linear Programming
#  Created by Joshua Wen from HIT on 2023/05/03.
#  Copyright © 2023 Joshua Wen. All rights reserved.
#  Wen Jiazheng (Joshua Wen) HIT 22B903087


import random
import sys
import time
import matplotlib.pyplot as plt
import pulp
from lib.logger import Logger


# 基于贪心策略的近似算法
def greedy(X, S, N):
    start = time.time()
    X1 = set(X)
    F = {}
    for i in range(1, N + 1):
        F['S' + str(i)] = set(S[i - 1])
    # print('F',F)
    final_Set = set()
    # 贪心算法首先要遍历子集，从中选择覆盖了最多的未覆盖元素的子集。
    while X1:
        best_set = None  # 覆盖了最多的未覆盖元素的子集
        sets_covered = set()
        for sets, point_for_set in F.items():
            covered = X1 & point_for_set  # 计算交集
            if len(covered) > len(sets_covered):
                best_set = sets
                sets_covered = covered
        X1 -= sets_covered
        final_Set.add(best_set)
    print('贪心算法final_Set', final_Set)
    end = time.time()
    greedy_runtime = end - start
    return greedy_runtime * 1000
    # print(list(final_Set))
    # 展示final_set中的子集具体包含哪些元素
    # for item in list(final_Set):
    #     print(F[item])


# 基于线性规划的近似算法————舍入法
def LP(X, S, N):
    start = time.time()
    # 随机生成每个集合的代价
    cost_S = []
    for i in range(N):
        a = random.random()
        cost_S.append(a)
    # 代价全为1
    # cost_S=[]
    # for i in range(N):
    #     cost_S.append(1)
    # 给每个集合引入一个变量xs
    x0 = []
    for i in range(1, N + 1):
        b = 'x' + str(i)
        x0.append(b)
    # print(x0)

    # W表示约束条件矩阵，是多个A拼接起来的矩阵
    W = []
    for s in X:
        A = []  # A是元素只有0或1的行向量，表示X中的每个元素是否在每一个S中
        for t in S:
            if s in t:
                r = 1
            else:
                r = 0
            A.append(r)
        W.append(A)
    # print(W)
    # for line in W:
    #     print(line)

    # 定义约束条件,生成N个字典，字典名为A1--AN
    createVar = locals()
    for i in range(1, N + 1):
        createVar['A' + str(i)] = {}
        for j in range(1, N + 1):
            createVar['A' + str(i)]['x' + str(j)] = W[i - 1][j - 1]
    # print(A1)
    # print(A50)
    # print(A100)
    # print(createVar['A' + str(100)])

    # 定义目标函数字典
    cost = {}
    for i in range(1, N + 1):
        cost['x' + str(i)] = cost_S[i - 1]
    # print(cost)

    # 创建问题实例，求最小极值
    prob = pulp.LpProblem("Set covering problem", pulp.LpMinimize)

    # 构建Lp变量字典，变量名以Ingr开头，如Ingr_CHICKEN，下界是0
    ingredient_vars = pulp.LpVariable.dicts("Ingr", x0, 0)

    # 添加目标方程
    prob += pulp.lpSum([cost[i] * ingredient_vars[i] for i in x0])

    # 添加前N个约束条件
    for i in range(1, N + 1):
        prob += pulp.lpSum([createVar['A' + str(i)][j] * ingredient_vars[j] for j in x0]) >= 1.0

    # 添加xs>=0的约束条件
    for i in x0:
        prob += ingredient_vars[i] >= 0.0

    # 求解
    prob.solve()
    # 查看解的状态
    # print("Status:", LpStatus[prob.status])
    # 目标函数的最小值
    # print('线性规划目标函数的最小值',value(prob.objective))

    # 打印求解结果
    # for i in prob.variables():
    #     print(i.varValue)

    # 求X中元素的最大频率f,求f时候的复杂度较高
    fre = []
    for item in X:
        i = 0
        for s in S:
            if item in s:
                i = i + 1
        fre.append(i)
    # print(fre)
    f = max(fre)

    # print(type(prob.variables))
    # 舍入法的第二步
    C = []
    C_detail = []
    j = 0
    for i in prob.variables():
        # print(str(i.varValue))
        l = str(i.varValue)
        if float(l) >= 1 / f:
            index = j
            C.append('S' + str(index))
            C_detail.append(S[index])
        j = j + 1
    print('基于线性规划的近似算法final_Set', C)
    # print(C_detail)
    end = time.time()
    LP_runtime = end - start
    return LP_runtime * 1000


def genXS(N):
    # N=100
    X = []
    for i in range(N):
        p = 'p' + str(i + 1)
        s = 'S' + str(i + 1)
        X.append(p)
    print('X', X)

    S0 = []
    while len(S0) < N / 5:
        a = random.randint(0, N - 1)
        if X[a] not in S0:
            S0.append(X[a])
    # print(S0)
    # print(len(S0))

    S_tem = S0
    i = 0
    S_detail = []  # 把S列表里的每一个子集展示出来
    while len(list(set(X) - set(S_tem))) >= (N / 5):
        #   X-S0=list(set(X)-set(S0))
        i = i + 1
        S_i = []
        S_j = []
        S_next = []
        n = random.randint(2, N / 5)  # S1集合的大小
        # print(n)
        b = random.randint(0, n - 1)
        while b == 0:
            b = random.randint(0, n - 1)
        # print('b正常')
        # 从X-S_tem中选b个点放入S_i中
        while len(S_i) < b:
            m = random.randint(0, b - 1)
            if list(set(X) - set(S_tem))[m] not in S_i:
                S_i.append(list(set(X) - set(S_tem))[m])
        # print('S_i正常')
        # 从S_tem中选n-b个点放入S_j中
        while len(S_j) < n - b:
            l = random.randint(0, n - b - 1)
            if S_tem[l] not in S_j:
                S_j.append(S_tem[l])
        # print('S_j正常')
        S_next = S_i + S_j
        S_detail.append(S_next)
        S_tem = S_tem + S_next
        # print('S'+str(i),S_next)
        # print('S_临时的 S',list(set(S_tem)))
        S_i = []
        S_j = []
        S_next = []

    # print('S_detail',S_detail)
    Sn = list(set(X) - set(S_tem))
    # print('Sn',Sn)

    S_detail1 = [S0] + S_detail + [Sn]
    # print('S_detail1',S_detail1)
    k = N - len(S_detail1)
    # print(k)
    S_next2 = []
    S_detail2 = []
    for i in range(k):
        q = random.randint(1, N / 5)  # 子集的长度
        while len(S_next2) < q:
            t = random.randint(0, N - 1)
            if X[t] not in S_next2:
                S_next2.append(X[t])
        S_detail2.append(S_next2)
        S_next2 = []

    # print(len(S_detail2))
    # print(len(S_detail1))

    S = []  # S是所有子集的集合
    createVar = locals()
    for i in range(1, N + 1):
        if i <= len(S_detail1):
            createVar['S' + str(i)] = S_detail1[i - 1]
        if i > len(S_detail1):
            createVar['S' + str(i)] = S_detail2[i - len(S_detail1) - 1]
        S.append(createVar['S' + str(i)])
    print('S', S)
    # print(S1)
    # print(S50)
    # print(S100)
    return X, S


if __name__ == '__main__':
    sys.stdout = Logger(stream=sys.stdout)
    # N_list = [100, 1000, 5000]
    N_list = [5000]
    greedy_runtime_list = []
    LP_runtime_list = []
    for N in N_list:
        X, S = genXS(N)
        greedy_runtime = greedy(X, S, N)
        LP_runtime = LP(X, S, N)
        greedy_runtime_list.append((N, greedy_runtime))
        LP_runtime_list.append((N, LP_runtime))
    print('greedy_runtime_list', greedy_runtime_list)
    print('LP_runtime_list', LP_runtime_list)
    plt.axis([-100, 5500, -100, 1200])
    plt.title("greedy & LP's runtime ")
    plt.plot([point[0] for point in greedy_runtime_list], [point[1] for point in greedy_runtime_list], color='red',
             marker='s', label='greedy_runtime_list')
    plt.plot([point[0] for point in LP_runtime_list], [point[1] for point in LP_runtime_list], color='blue', marker='o',
             label='LP_runtime_list')
    plt.show()
