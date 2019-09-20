#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 双向链表实现 InnoDB LRU 算法
# 1. LUR 链表分为两个区域，young(热点)和old区域，如果读取young区域内的数据，会把数据提到头部
# 2. 如果要加入新数据，会把 tail 淘汰，然后数据插入到 old_lru 处
# 3. 读取一个 old 区的数据，如果数据处于 lru 链表中的时间小于 1 秒，则位置不变，否则提到 head 处

import time


class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.pre = None
        self.addtime = time.time()


class Lru(object):
    def __init__(self, size):
        self.size = size
        self.young_cache = dict()
        self.old_cache = dict()

        self.young_size = int(size * 0.37)  # 3/8
        self.old_size = size - self.young_size

        self.head = Node(None, None)
        self.old_head = Node(None, None)  # old_lru 的 head
        self.tail = Node(None, None)

        self.head.next = self.old_head
        self.old_head.next = self.tail
        self.old_head.pre = self.head
        self.tail.pre = self.old_head

    def set(self, key, value):
        if key in self.young_cache:
            node = self.young_cache[key]
            node.value = value
            self._remove(node)
            self._insertYoungLru(node)

        elif key in self.old_cache:
            node = self.old_cache[key]
            node.value = value

            # 如果存在 old 区超过一秒，就进入 young 区
            if self._canToYoung(node):
                self._remove(node)
                del self.old_cache[key]

                if len(self.young_cache) >= self.young_size:
                    self._youngLastToOldHead()

                self._insertYoungLru(node)
                self.young_cache[key] = node

        else:
            # 如果 old 区满了，淘汰最后一个
            if len(self.old_cache) >= self.old_size:
                last = self._popOldLast()
                del self.old_cache[last.key]

            node = Node(key, value)
            self.old_cache[key] = node
            self._insertOldLru(node)

        return True

    def get(self, key):
        if key in self.young_cache:
            node = self.young_cache[key]
            self._remove(node)
            self._insertYoungLru(node)

            return node.value

        elif key in self.old_cache:
            node = self.old_cache[key]

            # 如果存在 old 区超过一秒，就进入 young 区
            if self._canToYoung(node):
                self._remove(node)
                del self.old_cache[key]

                if len(self.young_cache) >= self.young_size:
                    self._youngLastToOldHead()

                self._insertYoungLru(node)
                self.young_cache[key] = node

            return node.value

        else:
            return None

    # 是否存在超过 1 秒
    def _canToYoung(self, node):
        if time.time() - node.addtime > 1:
            return True

        return False

    # young 区最后一个淘汰到 old 区
    def _youngLastToOldHead(self):
        # 删除 young 最后一个
        young_last = self._popYoungLast()
        # 在 old 前面插入
        self._insertOldLru(young_last)

    # 淘汰掉young链表最后一个
    def _popYoungLast(self):
        young_last = self.old_head.pre
        if young_last is self.head:
            return False
        self._remove(young_last)
        return young_last

    # 淘汰掉整个链表最后一个
    def _popOldLast(self):
        oldest = self.tail.pre
        if oldest is self.old_head:
            return False

        self._remove(oldest)
        return oldest

    # 让节点排到old区域前面
    def _insertOldLru(self, node):
        node.next = self.old_head.next
        node.pre = self.old_head
        self.old_head.next.pre = node
        self.old_head.next = node

    # 让节点排到young区域前面
    def _insertYoungLru(self, node):
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

    # 打印 lru 队列
    def printQueue(self):
        young = []
        node = self.head.next
        while node and node.key:
            young.append(node.key)
            node = node.next
        old = []
        node = self.old_head.next
        while node and node.key:
            old.append(node.key)
            node = node.next

        print young, old


if __name__ == '__main__':
    lru = Lru(9)

    # 新数据进入 old 队列
    for i in [1, 2, 3, 4, 5, 6, 7, 8]:
        lru.set(i, i)
        lru.printQueue()

    # [] [1]
    # [] [2, 1]
    # [] [3, 2, 1]
    # [] [4, 3, 2, 1]
    # [] [5, 4, 3, 2, 1]
    # [] [6, 5, 4, 3, 2, 1]
    # [] [7, 6, 5, 4, 3, 2]
    # [] [8, 7, 6, 5, 4, 3]
    # [] [8, 7, 6, 5, 4, 3]

    time.sleep(1.1)

    # 热点数据进入 young 队列
    lru.set(4, 4)
    lru.printQueue()
    # [4] [8, 7, 6, 5, 3]

    lru.get(3)
    lru.printQueue()
    # [3, 4] [8, 7, 6, 5]

    lru.get(6)
    lru.printQueue()
    # [6, 3, 4] [8, 7, 5]

    lru.get(4)
    lru.printQueue()
    # [4, 6, 3] [8, 7, 5]

    # 新数据进入 old 队列，观察到 old 队列删除最后的数据
    for i in [9, 10, 11, 12, 13]:
        lru.set(i, i)
        lru.printQueue()

    # [4, 6, 3] [9, 8, 7, 5]
    # [4, 6, 3] [10, 9, 8, 7, 5]
    # [4, 6, 3] [11, 10, 9, 8, 7, 5]
    # [4, 6, 3] [12, 11, 10, 9, 8, 7]
    # [4, 6, 3] [13, 12, 11, 10, 9, 8]

    time.sleep(1.1)

    # 热点数据替换
    lru.get(11)
    lru.printQueue()
    # [11, 4, 6] [3, 13, 12, 10, 9, 8]

    lru.get(12)
    lru.printQueue()
    # [12, 11, 4] [6, 3, 13, 10, 9, 8]
