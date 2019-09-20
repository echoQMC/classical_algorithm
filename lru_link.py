#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 双向链表实现 LRU 算法


class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.pre = None


class Lru(object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.cacheDict = dict()
        self.head.next = self.tail
        self.tail.pre = self.head

    def set(self, key, value):
        if key not in self.cacheDict:
            if len(self.cacheDict) >= self.maxLength:
                self.popOldest()
            node = Node(key, value)
        else:
            node = self.cacheDict[key]
            node.value = value
            self._remove(node)

        self.cacheDict[key] = node
        self._insert(node)

        return True

    def get(self, key):
        if key in self.cacheDict:
            node = self.cacheDict[key]
            self._remove(node)
            self._insert(node)
            return node.value
        else:
            return None

    # 让节点排到前面
    def _insert(self, node):
        node.next = self.head.next
        node.pre = self.head
        self.head.next.pre = node
        self.head.next = node

    # 从链表中排除
    def _remove(self, node):
        node.pre.next = node.next
        node.next.pre = node.pre
        node.next = None
        node.pre = None

    # 删除最旧的节点
    def popOldest(self):
        oldestNode = self.tail.pre
        self._remove(oldestNode)
        del(self.cacheDict[oldestNode.key])
        return True

    # 打印 lru 队列
    def printQueue(self):
        node = self.head.next
        lt = []
        while node and node.key:
            lt.append(node.key)
            node = node.next
        print lt


if __name__ == '__main__':
    lru = Lru(4)

    for i in [1, 2, 3, 4, 5, 6]:
        lru.set(i, i)
        lru.printQueue()
    # [1]
    # [2, 1]
    # [3, 2, 1]
    # [4, 3, 2, 1]
    # [5, 4, 3, 2]
    # [6, 5, 4, 3]

    lru.set(4, 4)
    lru.printQueue()
    # [4, 6, 5, 3]

    lru.get(3)
    lru.printQueue()
    # [3, 4, 6, 5]

    lru.get(6)
    lru.printQueue()
    # [6, 3, 4, 5]
