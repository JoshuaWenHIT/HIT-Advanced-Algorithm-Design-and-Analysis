#  A Convex Hull Solving Algorithm Based on Enumeration Method
#  Created by Joshua Wen from HIT on 2023/05/02.
#  Copyright © 2023 Joshua Wen. All rights reserved.
#  Wen Jiazheng (Joshua Wen) HIT 22B903087


from lib.point import Point, Axis
import random
from enumeration_method import BruteForceCH
from graham_scan_method import GrahamScanCH
from divide_conquer_method import DivideCH


def generate_data(size, x_axis, y_axis):
    data = []
    for i in range(size):
        x = random.uniform(x_axis.min, x_axis.max)
        y = random.uniform(y_axis.min, y_axis.max)
        p = Point(x, y)
        data.append(p)
    return data


if __name__ == '__main__':
    x_axis = Axis(0, 100)
    y_axis = Axis(0, 100)
    size = 3000
    data = generate_data(size, x_axis, y_axis)
    data_o = []
    BruteForceCH(size, data_o, data)
    GrahamScanCH(data)
    DivideCH(data)
