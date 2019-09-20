#!/usr/bin/env python
# -*- coding: utf-8 -*-
# OrderedDict 实现 LRU 算法

from collections import OrderedDict


class Lru(object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.cache = OrderedDict()

    def set(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
            self.cache[key] = value
        elif len(self.cache) >= self.maxLength:
            self.cache.popitem(last=False)
            self.cache[key] = value
        else:
            self.cache[key] = value

        return True

    def get(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return None

    def printQueue(self):
        print self.cache.keys()


if __name__ == '__main__':
    lru = Lru(4)

    for i in [1, 2, 3, 4, 5, 6]:
        lru.set(i, i)
        lru.printQueue()
    # [1]
    # [1, 2]
    # [1, 2, 3]
    # [1, 2, 3, 4]
    # [2, 3, 4, 5]
    # [3, 4, 5, 6]

    lru.set(4, 4)
    lru.printQueue()
    # [3, 5, 6, 4]

    lru.get(3)
    lru.printQueue()
    # [5, 6, 4, 3]

    lru.get(6)
    lru.printQueue()
    # [5, 4, 3, 6]
