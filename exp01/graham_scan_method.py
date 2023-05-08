#  A Convex Hull Solving Algorithm Based on Graham-Scan
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
        # x=random.randint(0, 100)
        # y=random.randint(0, 100)
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


def GrahamScanCH(data, show=True):
    start_time = time.time()
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
    data = sorted(data, key=lambda point: point.angle)
    stack = [p0, data[0], data[1]]
    for i in range(2, len(data)):
        while judge(stack[-2], stack[-1], data[i]):
            stack.pop(-1)
        stack.append(data[i])
    end_time = time.time()
    print("Graham-Scan method cost {:.1f}ms".format((end_time - start_time) * 1000))

    if show:
        plt.scatter(p0.x, p0.y, c='g', marker='.')
        for p in data:
            plt.scatter(p.x, p.y, c='g', marker='.')
        for i in range(len(stack) - 1):
            plt.scatter(stack[i].x, stack[i].y, c='r', marker='.')
            plt.plot([stack[i].x, stack[i + 1].x], [stack[i].y, stack[i + 1].y], color='r')
        plt.scatter(stack[-1].x, stack[-1].y, c='r', marker='.')
        plt.plot([stack[-1].x, p0.x], [stack[-1].y, p0.y], color='r')
        plt.show()


if __name__ == '__main__':
    size = 50
    data = generate_data(size)
    GrahamScanCH(data)
