#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 随机抽样算法
import random


# 抽样，从n个中抽m个
def sampling(lists, m, n=None):
    selected = []
    if n is None:
        n = len(lists)
    remaining = n - 1
    for i in range(n):
        # random.random()返回 0 ~ 1的随机数
        if random.random() * remaining < m:
            selected.append(lists[i])
            m -= 1
        remaining -= 1
    return selected


# 不知道总数，随机取一个
def getRandLine(text):
    i = 1
    selected = ''
    for line in text.splitlines():
        if (random.random() < (1.0 / i)):
            selected = line
        i += 1
    return selected


if __name__ == '__main__':
    # 从n个中抽m个
    lists = [i for i in range(10)]
    print sampling(lists, 3)

    # 不知道总数，随机取一个
    text = """\
line1
line2
line3
line4
line5
line6
line7
line8
line9
line10
    """
    print getRandLine(text)
