#  A Quick Sort Algorithm
#  Created by Joshua Wen from HIT on 2023/05/03.
#  Copyright © 2023 Joshua Wen. All rights reserved.
#  Wen Jiazheng (Joshua Wen) HIT 22B903087
import copy
import random
import time
import sys
import matplotlib.pyplot as plt
import json

sys.setrecursionlimit(10000000)


def quicksort(A, p, r):
    if p < r:
        q = partion(A, p, r)
        quicksort(A, p, q - 1)
        quicksort(A, q + 1, r)


def partion(A, p, r):  # 每个元素都和最后一个元素比较，小的放前面，大的放后面
    i = random.randint(p, r)
    A[i], A[r] = A[r], A[i]
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:  #####这里是可以改进的地方，能节省很多时间
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1


# 三路快排
def quck(arr, l, r):
    # s = int(random.uniform(l, r) + 0.5)
    # arr[s],arr[l]=arr[l],arr[s]
    base = arr[l]
    lt = l + 1
    gt = r + 1
    i = l + 1
    # print(lt, i, gt)
    while i < gt:
        if arr[i] < base:
            arr[i], arr[lt] = arr[lt], arr[i]
            lt += 1
            i += 1
        elif arr[i] > base:
            gt -= 1
            arr[i], arr[gt] = arr[gt], arr[i]
        else:
            i += 1
    arr[l], arr[lt - 1] = arr[lt - 1], arr[l]
    # print(arr)
    return lt - 1, gt


def QuickSort3(arr, l, r):
    if l >= r:
        return
    mid, mid2 = quck(arr, l, r)
    # print(mid,arr[l:mid],arr[mid2:r+1])
    QuickSort3(arr, l, mid)
    QuickSort3(arr, mid2, r)
    # print(arr)
    return arr


if __name__ == '__main__':
    # print(len(a)-1)
    # print(quck(a,0,len(a)-1))
    # 小样例测试
    # A = [[2, 8, 7, 9, 1, 3, 5, 10, 6, 4]]

    # 生成11 个大小为10^6的整数数据集，第𝑖个子集中存在元素重复106 ×10 × i %,i = 0,1,2, ⋯ ,10
    N = 10000
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
    # with open('./lib/data.txt', 'r') as f:
    #     A = json.load(f)
    print("The datasets are created !")

    # print(A0)
    # print(A1)
    # print(A2)
    # print(A3)
    # print(A10)

    a = 0
    quicksort_runtime = []
    quicksort3_runtime = []
    for list0 in A:
        list00 = copy.deepcopy(list0)
        list01 = copy.deepcopy(list0)
        start = time.time()
        list1 = QuickSort3(list00, 0, len(list0) - 1)
        end = time.time()
        runtime = end - start
        # print('三路快排排好序的集合A' + str(a) + ':', list1)
        print('集合A' + str(a) + '三路快排的运行时间:{:1f}ms'.format(runtime * 1000))
        quicksort3_runtime.append((a * 0.1, runtime))
        start1 = time.time()
        quicksort(list01, 0, len(list0) - 1)
        end1 = time.time()
        runtime1 = end1 - start1
        # print('快速排序算法排好序的集合A' + str(a) + ':', list0)
        print('集合A' + str(a) + '快速排序算法的运行时间:{:1f}ms'.format(runtime1 * 1000))
        quicksort3_runtime.append((a * 0.1, runtime))
        quicksort_runtime.append((a * 0.1, runtime1))
        a = a + 1
    # list0 = A[2]
    # # list00 = copy.deepcopy(list0)
    # list01 = copy.deepcopy(list0)
    # start = time.time()
    # # list1 = QuickSort3(list00, 0, len(list0) - 1)
    # end = time.time()
    # runtime = end - start
    # # print('三路快排排好序的集合A' + str(a) + ':', list1)
    # print('集合A' + str(a) + '三路快排的运行时间:{:1f}ms'.format(runtime * 1000))
    # quicksort3_runtime.append((a * 0.1, runtime))
    # start1 = time.time()
    # quicksort(list01, 0, len(list0) - 1)
    # end1 = time.time()
    # runtime1 = end1 - start1
    # # print('快速排序算法排好序的集合A' + str(a) + ':', list0)
    # print('集合A' + str(a) + '快速排序算法的运行时间:{:1f}ms'.format(runtime1 * 1000))
    # quicksort3_runtime.append((a * 0.1, runtime))
    # quicksort_runtime.append((a * 0.1, runtime1))
    # a = a + 1

    plt.axis([-0.1, 1.2, -0.1, 10])
    plt.title("quicksort3's runtime ")
    plt.plot([point[0] for point in quicksort_runtime], [point[1] for point in quicksort_runtime], color='red',
             marker='s', label='quicksort_runtime')
    plt.plot([point[0] for point in quicksort3_runtime], [point[1] for point in quicksort3_runtime], color='blue',
             marker='o', label='sorted_runtime')

    plt.show()
