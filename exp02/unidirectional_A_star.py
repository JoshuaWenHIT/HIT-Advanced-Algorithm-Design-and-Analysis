#  A Unidirectional A* Algorithm for Solving Maze Problems
#  Created by Joshua Wen from HIT on 2023/05/02.
#  Copyright © 2023 Joshua Wen. All rights reserved.
#  Wen Jiazheng (Joshua Wen) HIT 22B903087


import math
import random
import copy
import time
import sys
import tkinter
import threading

# 地图
# 16 * 14
tm = [
    '................',
    '................',
    '................',
    '................',
    '................',
    '......#.........',
    '......#.........',
    '.......#........',
    '...S...#........',
    '.......##....T..',
    '........#.......',
    '........#.......',
    '................',
    '................',
]
# 40 * 20
# tm = [
#     '...#...#....#...........***********T****',
#     '.......#....#............*********%*****',
#     '######.####.#.............*******%******',
#     '........#...#.............******%****...',
#     '............#.............*******%**....',
#     '.......##...#..............******%%.....',
#     '..######....#..............******%%.....',
#     '..#..#.#....#................****%%%#...',
#     '.....#..........................%%%%....',
#     '.....#.#........................%%%.#...',
#     '..#.S#.##..........###......#...%%.%%...',
#     '..####..#..........###.........#%.%%....',
#     '...#....#...#......###...........%%.....',
#     '...#....##.##..................#%%%.....',
#     '...#....#...#...................%%%.....',
#     '...######...#...........##.....%%%......',
#     '...#........#...........##.....%%%......',
#     '.......#....#.................%%%.......',
#     '...#...#....#................%%%........',
#     '...#...#....#...............%%%.........',
# ]

# 存储搜索时的地图
test_map = []


# ----------- 开放列表和关闭列表的元素类型，parent用来在成功的时候回溯路径 -----------
class Node_Elem:

    def __init__(self, parent, x, y, dist):
        self.parent = parent  # 回溯父节点
        self.x = x  # x坐标
        self.y = y  # y坐标
        self.dist = dist  # 从起点到此位置的实际距离


# ----------- A*算法 -----------
class A_Star:

    def __init__(self, root, s_x, s_y, e_x, e_y, w=16, h=14):

        self.s_x = s_x  # 起点x
        self.s_y = s_y  # 起点y
        self.e_x = e_x  # 终点x
        self.e_y = e_y  # 终点y

        self.open = []  # open表
        self.close = []  # close表
        self.path = []  # path表

        # 创建画布
        self.root = root  # 画布根节点
        self.width = w  # 地图w，默认40
        self.height = h  # 地图h，默认20
        self.__r = 9  # 半径
        # tkinter.Canvas
        self.canvas = tkinter.Canvas(
            root,
            width=self.width * 20 + 100,
            height=self.height * 20 + 100,
            bg="#EBEBEB",  # 背景白色
            xscrollincrement=1,
            yscrollincrement=1
        )
        self.canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.title("A*寻路算法(e:开始搜索或退出)")
        self.__bindEvents()
        self.new()

    # 按键响应程序
    def __bindEvents(self):

        self.root.bind("e", self.quite)  # 退出程序

    # 退出程序
    def quite(self, evt):
        self.root.destroy()

    # 更改标题
    def title(self, s):
        self.root.title(s)

    # 初始化
    def new(self):

        node = self.canvas.create_rectangle(80 - self.__r,
                                            20 - self.__r, 80 + self.__r, 20 + self.__r,
                                            fill="#A6A6A6",
                                            outline="#ffffff",
                                            tags="node",
                                            )
        self.canvas.create_text(115, 20,
                                text=u'Barrier',
                                fill='black'
                                )
        node = self.canvas.create_rectangle(180 - self.__r,
                                            20 - self.__r, 180 + self.__r, 20 + self.__r,
                                            fill="#FFC125",
                                            outline="#ffffff",
                                            tags="node",
                                            )
        self.canvas.create_text(215, 20,
                                text=u'Desert',
                                fill='black'
                                )

        node = self.canvas.create_rectangle(280 - self.__r,
                                            20 - self.__r, 280 + self.__r, 20 + self.__r,
                                            fill="#1C86EE",
                                            outline="#ffffff",
                                            tags="node",
                                            )
        self.canvas.create_text(310, 20,
                                text=u'Lake',
                                fill='black'
                                )

        node = self.canvas.create_rectangle(380 - self.__r,
                                            20 - self.__r, 380 + self.__r, 20 + self.__r,
                                            fill="#000000",
                                            outline="#ffffff",
                                            tags="node",
                                            )
        self.canvas.create_text(410, 20,
                                text=u'Path',
                                fill='black'
                                )

        node = self.canvas.create_rectangle(480 - self.__r,
                                            20 - self.__r, 480 + self.__r, 20 + self.__r,
                                            fill="#7CCD7C",
                                            outline="#ffffff",
                                            tags="node",
                                            )
        self.canvas.create_text(520, 20,
                                text=u'Searched',
                                fill='black'
                                )

        for i in range(self.width):
            for j in range(self.height):

                # 生成可行节点
                if test_map[j][i] == '.':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#FFFFFF",  # 填充白色
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )

                # 生成障碍节点，半径为self.__r
                if test_map[j][i] == '#':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#A6A6A6",  # 填充灰色
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )

                # 生成沙漠节点
                if test_map[j][i] == '*':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#FFC125",  # 填充黄色
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )

                # 生成河流节点
                if test_map[j][i] == '%':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#1C86EE",  # 填充蓝色
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )

                # 显示起点
                if test_map[j][i] == 'S':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#00ff00",  # 填充绿色
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )
                    self.canvas.create_text(i * 20 + 50, j * 20 + 50 - 20,  # 使用create_text方法在坐标处绘制文字
                                            text=u'Start',  # 所绘制文字的内容
                                            fill='black'  # 所绘制文字的颜色为灰色
                                            )
                # 显示终点
                if test_map[j][i] == 'T':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#00ff00",  # 填充绿色
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )
                    self.canvas.create_text(i * 20 + 50, j * 20 + 50 - 20,  # 使用create_text方法在坐标处绘制文字
                                            text=u'End',  # 所绘制文字的内容
                                            fill='black'  # 所绘制文字的颜色为灰色
                                            )
                # 生成路径节点，半径为self.__r
                if test_map[j][i] == '@':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#000000",  # 填充黑色
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )
                # 显示搜索过的点
                if test_map[j][i] == ' ':
                    node = self.canvas.create_rectangle(i * 20 + 50 - self.__r,
                                                        j * 20 + 50 - self.__r, i * 20 + 50 + self.__r,
                                                        j * 20 + 50 + self.__r,
                                                        fill="#7CCD7C",  # 填充浅绿
                                                        outline="#ffffff",  # 轮廓白色
                                                        tags="node",
                                                        )

    # 查找路径的入口函数
    def find_path(self):
        # 构建开始节点
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
        while True:
            # 扩展节点
            self.extend_round(p)
            # 如果open表为空，则不存在路径，返回
            if not self.open:
                return
            # 取F值最小的节点
            idx, p, cost = self.get_best()
            # 到达终点，生成路径，返回
            if self.is_target(p):
                self.make_path(p)
                print('cost', cost)
                return
            # 把此节点加入close表，并从open表里删除
            self.close.append(p)
            del self.open[idx]

    # 生成路径
    def make_path(self, p):
        # 从结束点回溯到开始点，开始点的parent == None
        while p:
            self.path.append((p.x, p.y))
            p = p.parent

    # 判断是否为终点
    def is_target(self, i):
        return i.x == self.e_x and i.y == self.e_y

    # 取F值最小的节点
    def get_best(self):
        best = None
        bv = 10000000  # MAX值
        bi = -1
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)
            if value < bv:
                best = i
                bv = value
                bi = idx
                cost = value
        return bi, best, cost

    # 求距离
    def get_dist(self, i):
        # F = G + H
        # G 为当前路径长度(i.dist)，H为估计长度(该点到目标点的欧式距离)
        #
        return i.dist + math.sqrt((self.e_x - i.x) * (self.e_x - i.x) + (self.e_y - i.y) * (self.e_y - i.y))
        ##

    # 扩展节点
    def extend_round(self, p):
        # 八个方向移动
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1, -1, -1, 0, 0, 1, 1, 1)
        # 上下左右四个方向移动
        # xs = (0, -1, 1, 0)
        # ys = (-1, 0, 0, 1)
        for x, y in zip(xs, ys):
            new_x, new_y = x + p.x, y + p.y
            # 检查位置是否合法
            if not self.is_valid_coord(new_x, new_y):
                continue
            # 构造新的节点，计算距离
            node = Node_Elem(p, new_x, new_y, p.dist + self.get_cost(p.x, p.y, new_x, new_y))
            # 新节点在关闭列表，则忽略
            if self.node_in_close(node):
                continue
            i = self.node_in_open(node)
            # 新节点在open表
            if i != -1:
                # 当前路径距离更短
                if self.open[i].dist > node.dist:
                    # 更新距离
                    self.open[i].parent = p
                    self.open[i].dist = node.dist
                    # print(self.open[i].dist)
                continue
            # 否则加入open表
            self.open.append(node)
            # print(self.open[i].dist)

    # 移动距离，直走1.0，斜走1.4,沙漠代价4，河流代价2
    def get_cost(self, x1, y1, x2, y2):
        if test_map[y2][x2] == '*':
            if x1 == x2 or y1 == y2:
                return 1.0 + 4.0
            return 1.4142135623731 + 4.0
        if test_map[y2][x2] == '%':
            if x1 == x2 or y1 == y2:
                return 1.0 + 2.0
            return 1.4142135623731 + 2.0
        if x1 == x2 or y1 == y2:
            return 1.0
        return 1.4142135623731

    # 检查节点是否在close表
    def node_in_close(self, node):
        for i in self.close:
            if node.x == i.x and node.y == i.y:
                return True
        return False

    # 检查节点是否在open表，返回序号
    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

    # 判断位置是否合法，超出边界或者为阻碍
    def is_valid_coord(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return test_map[y][x] != '#'

    # 搜寻过的位置
    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.x, i.y))
        for i in self.close:
            l.append((i.x, i.y))
        return l


# 获取起点坐标
def get_start_XY():
    return get_symbol_XY('S')


# 获取终点坐标
def get_end_XY():
    return get_symbol_XY('T')


# 查找特定元素
def get_symbol_XY(s):
    for y, line in enumerate(test_map):
        try:
            x = line.index(s)
        except:
            continue
        else:
            break
    return x, y


# 标记路径位置
def mark_path(l):
    mark_symbol(l, '@')


# 标记已搜索过的位置
def mark_searched(l):
    mark_symbol(l, ' ')


# 标记函数
def mark_symbol(l, s):
    for x, y in l:
        test_map[y][x] = s


# 标记起点和终点
def mark_start_end(s_x, s_y, e_x, e_y):
    test_map[s_y][s_x] = 'S'
    test_map[e_y][e_x] = 'T'


# 将地图字符串转化为表
def tm_to_test_map():
    for line in tm:
        test_map.append(list(line))


# 寻找路径
def find_path():
    s_x, s_y = get_start_XY()
    e_x, e_y = get_end_XY()
    # A*算法
    a_star = A_Star(tkinter.Tk(), s_x, s_y, e_x, e_y)
    a_star.root.mainloop()
    a_star.find_path()
    searched = a_star.get_searched()
    path = a_star.path
    # 标记已搜索过的位置
    # mark_searched(searched)
    # 标记路径位置
    mark_path(path)
    # 标记起点和终点
    mark_start_end(s_x, s_y, e_x, e_y)

    print(u"路径长度:%d" % (len(path)))
    print(u"搜索过的区域:%d" % (len(searched)))

    a_star = A_Star(tkinter.Tk(), s_x, s_y, e_x, e_y)
    a_star.root.mainloop()


# ----------- 程序的入口处 -----------

if __name__ == '__main__':
    print()
    u""" 
    """
    # 载入地图
    tm_to_test_map()
    # 寻找路径
    find_path()
