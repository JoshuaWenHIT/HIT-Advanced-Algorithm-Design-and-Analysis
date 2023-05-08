#  A Convex Hull Solving Algorithm Based on Enumeration Method
#  Created by Joshua Wen from HIT on 2023/05/02.
#  Copyright © 2023 Joshua Wen. All rights reserved.
#  Wen Jiazheng (Joshua Wen) HIT 22B903087


from lib.point import Point
import random
import matplotlib.pyplot as plt
import time


# 判断p4是否在p1,p2,p3构成的三角形中
def istriangle(a, b, c, p):
    signOfTrig = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    signOfAB = (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x)
    signOfCA = (a.x - c.x) * (p.y - c.y) - (a.y - c.y) * (p.x - c.x)
    signOfBC = (c.x - b.x) * (p.y - b.y) - (c.y - b.y) * (p.x - b.x)

    d1 = (signOfAB * signOfTrig > 0)
    d2 = (signOfCA * signOfTrig > 0)
    d3 = (signOfBC * signOfTrig > 0)

    return d1 and d2 and d3


def generate_data(size):
    data = []
    data_o = []
    for i in range(size):
        # x=random.randint(0, 100)
        # y=random.randint(0, 100)
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        p = Point(x, y)
        data_o.append(p)
    return data, data_o


def d(A, B, P):
    ans = (B.x - A.x) * (P.y - A.y) - (B.y - A.y) * (P.x - A.x)
    return ans


def BruteForceCH(size, data, data_o, show=True):
    start_time = time.time()
    L = []
    R = []
    flag = [0 for x in range(size)]

    for i in range(size - 3):
        if flag[i] == 1:
            continue
        for j in range(i + 1, size - 2):
            if flag[j] == 1:
                continue
            for k in range(j + 1, size - 1):
                if flag[k] == 1:
                    continue
                for l in range(k + 1, size):
                    if flag[l] == 1:
                        continue
                    elif istriangle(data_o[i], data_o[j], data_o[k], data_o[l]):
                        flag[l] = 1
                        continue
                    elif istriangle(data_o[l], data_o[j], data_o[k], data_o[i]):
                        flag[i] = 1
                        continue
                    elif istriangle(data_o[i], data_o[l], data_o[k], data_o[j]):
                        flag[j] = 1
                        continue
                    elif istriangle(data_o[i], data_o[j], data_o[l], data_o[k]):
                        flag[k] = 1
    for i in range(size):
        if flag[i] == 0:
            data.append(data_o[i])
    data = sorted(data, key=lambda point: (point.x, point.y))

    A = data[0]
    B = data[-1]
    del data[0]
    del data[-1]
    for P in data:
        if d(A, B, P) > 0:
            L.append(P)
        elif d(A, B, P) < 0:
            R.append(P)
    Lr = L.reverse()
    end_time = time.time()
    print("enumeration method cost {:.1f}ms".format((end_time - start_time) * 1000))

    if show:
        for p in data_o:
            plt.scatter(p.x, p.y, c='g', marker='.')

        plt.scatter(A.x, A.y, c='r', marker='.')
        plt.plot([A.x, R[0].x], [A.y, R[0].y], color='r')
        for i in range(len(R) - 1):
            plt.scatter(R[i].x, R[i].y, c='r', marker='.')
            plt.plot([R[i].x, R[i + 1].x], [R[i].y, R[i + 1].y], color='r')
        plt.scatter(R[-1].x, R[-1].y, c='r', marker='.')
        plt.plot([R[-1].x, B.x], [R[-1].y, B.y], color='r')
        plt.scatter(B.x, B.y, c='r', marker='.')
        plt.plot([B.x, L[0].x], [B.y, L[0].y], color='r')
        for i in range(len(L) - 1):
            plt.scatter(L[i].x, L[i].y, c='r', marker='.')
            plt.plot([L[i].x, L[i + 1].x], [L[i].y, L[i + 1].y], color='r')
        plt.scatter(L[-1].x, L[-1].y, c='r', marker='.')
        plt.plot([L[-1].x, A.x], [L[-1].y, A.y], color='r')
        plt.show()


if __name__ == '__main__':
    size = 50
    data, data_o = generate_data(size)
    BruteForceCH(size, data, data_o)

