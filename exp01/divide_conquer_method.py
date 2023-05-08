#  A Convex Hull Solving Algorithm Based on Divide and Conquer
#  Created by Joshua Wen from HIT on 2023/05/02.
#  Copyright © 2023 Joshua Wen. All rights reserved.
#  Wen Jiazheng (Joshua Wen) HIT 22B903087


from lib.point import Point
import random
import matplotlib.pyplot as plt
import math
import time


def generate_data(size):
    data = []
    for i in range(size):
        # x=random.randint(0, 10)
        # y=random.randint(0, 10)
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        p = Point(x, y)
        data.append(p)
    return data


def judge(a, b, c):
    ans = (c.x - a.x) * (b.y - a.y) - (c.y - a.y) * (b.x - a.x)
    if ans >= 0:
        return True
    else:
        return False


def divide(data):
    maxn = -1
    minn = 101
    data1 = []
    data2 = []
    for p in data:
        if p.x < minn:
            minn = p.x
        if p.x > maxn:
            maxn = p.x
    minddle = (maxn + minn) / 2
    for p in data:
        if p.x <= minddle:
            data1.append(p)
        else:
            data2.append(p)
    return data1, data2


def conquer(data1, data2):
    if len(data1) == 0:
        return data2
    if len(data2) == 0:
        return data1
    # 求纵坐标最小的点
    if data1[0].y <= data2[0].y:
        p0 = data1[0]
        data1.remove(p0)
        flag = 1
    else:
        p0 = data2[0]
        data2.remove(p0)
        flag = 0
    # 计算每一个点相对于p0的极角
    p0.angle = 0
    for p in data1:
        if p.x == p0.x:
            p.angle = math.pi / 2
        elif p.x > p0.x:
            p.angle = math.atan((p.y - p0.y) / (p.x - p0.x))
        else:
            p.angle = math.atan((p0.x - p.x) / (p.y - p0.y)) + math.pi / 2
    for p in data2:
        if p.x == p0.x:
            p.angle = math.pi / 2
        elif p.x > p0.x:
            p.angle = math.atan((p.y - p0.y) / (p.x - p0.x))
        else:
            p.angle = math.atan((p0.x - p.x) / (p.y - p0.y)) + math.pi / 2
    # 利用data1和data2逆时针排序的特点，在线性时间内将所有点按极角大小排好序
    min1 = 10
    max1 = -1
    min2 = 10
    max2 = -1
    if flag == 0:
        minindex = -1
        maxindex = -1
        for i in range(len(data1)):
            if data1[i].angle > max1:
                max1 = data1[i].angle
                maxindex = i
            if data1[i].angle < min1:
                min1 = data1[i].angle
                minindex = i
        if minindex <= maxindex:
            data3 = data1[minindex:maxindex + 1]
            data4 = []
            if minindex != 0:
                data4 = data4 + data1[minindex - 1::-1]
            if maxindex != len(data1) - 1:
                data4 = data4 + data1[-1:maxindex:-1]
        else:
            data3 = data1[minindex:maxindex:-1]
            data4 = []
            data4 = data4 + data1[minindex + 1:]
            data4 = data4 + data1[0:maxindex + 1]
        data5 = []
        i = 0
        j = 0
        while i < len(data3) and j < len(data4):
            if data3[i].angle <= data4[j].angle:
                data5.append(data3[i])
                i = i + 1
            else:
                data5.append(data4[j])
                j = j + 1
        while i < len(data3):
            data5.append(data3[i])
            i = i + 1
        while j < len(data4):
            data5.append(data4[j])
            j = j + 1
        data6 = []
        i = 0
        j = 0
        while i < len(data2) and j < len(data5):
            if data2[i].angle <= data5[j].angle:
                data6.append(data2[i])
                i = i + 1
            else:
                data6.append(data5[j])
                j = j + 1
        while i < len(data2):
            data6.append(data2[i])
            i = i + 1
        while j < len(data5):
            data6.append(data5[j])
            j = j + 1
    else:
        maxindex = -1
        minindex = -1
        for i in range(len(data2)):
            if data2[i].angle > max2:
                max2 = data2[i].angle
                maxindex = i
            if data2[i].angle < min2:
                min2 = data2[i].angle
                minindex = i
        if minindex <= maxindex:
            data3 = data2[minindex:maxindex + 1]
            data4 = []
            if minindex != 0:
                data4 = data4 + data2[minindex - 1::-1]
            if maxindex != len(data2) - 1:
                data4 = data4 + data2[-1:maxindex:-1]
        else:
            data3 = data2[minindex:maxindex:-1]
            data4 = []
            data4 = data4 + data2[minindex + 1:]
            data4 = data4 + data2[0:maxindex + 1]
        data5 = []

        i = 0
        j = 0
        while i < len(data3) and j < len(data4):
            if data3[i].angle <= data4[j].angle:
                data5.append(data3[i])
                i = i + 1
            else:
                data5.append(data4[j])
                j = j + 1
        while i < len(data3):
            data5.append(data3[i])
            i = i + 1
        while j < len(data4):
            data5.append(data4[j])
            j = j + 1
        data6 = []
        i = 0
        j = 0
        while i < len(data1) and j < len(data5):
            if data1[i].angle <= data5[j].angle:
                data6.append(data1[i])
                i = i + 1
            else:
                data6.append(data5[j])
                j = j + 1
        while i < len(data1):
            data6.append(data1[i])
            i = i + 1
        while j < len(data5):
            data6.append(data5[j])
            j = j + 1
    # 洗牌，生成新的凸包
    if len(data6) <= 1:
        return [p0] + data6
    stack = [p0, data6[0], data6[1]]
    if len(data6) == 2:
        return stack
    for i in range(2, len(data6)):
        while judge(stack[-2], stack[-1], data6[i]):
            stack.pop(-1)
        stack.append(data6[i])
    return stack


def divide_and_conquer(data):
    if len(data) <= 1:
        return data
    if len(data) == 2:
        return sorted(data, key=lambda point: (point.y, point.x))
    elif len(data) == 3:
        p0 = Point(101, 101)
        for p in data:
            if p.y < p0.y:
                p0 = p
            elif p.y == p0.y and p.x < p0.x:
                p0 = p
        data.remove(p0)
        for p in data:
            if p.x == p0.x:
                p.angle = math.pi / 2
            elif p.x > p0.x:
                p.angle = math.atan((p.y - p0.y) / (p.x - p0.x))
            else:
                p.angle = math.atan((p0.x - p.x) / (p.y - p0.y)) + math.pi / 2
        res = [p0]
        if data[0].angle <= data[1].angle:
            res.append(data[0])
            res.append(data[1])
        else:
            res.append(data[1])
            res.append(data[0])
        return res
    data1, data2 = divide(data)
    data1 = divide_and_conquer(data1)
    data2 = divide_and_conquer(data2)
    data = conquer(data1, data2)
    return data


def DivideCH(data, show=True):
    start_time = time.time()
    stack = divide_and_conquer(data)
    end_time = time.time()
    print("divide and conquer method cost {:.1f}ms".format((end_time - start_time) * 1000))

    if show:
        for p in data:
            plt.scatter(p.x, p.y, c='g', marker='.')
        for i in range(len(stack) - 1):
            plt.scatter(stack[i].x, stack[i].y, c='r', marker='.')
            plt.plot([stack[i].x, stack[i + 1].x], [stack[i].y, stack[i + 1].y], color='r')
        plt.scatter(stack[-1].x, stack[-1].y, c='r', marker='.')
        plt.plot([stack[-1].x, stack[0].x], [stack[-1].y, stack[0].y], color='r')
        plt.show()


if __name__ == '__main__':
    size = 50
    data = generate_data(size)
    DivideCH(data)
