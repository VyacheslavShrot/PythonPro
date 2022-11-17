class Node:
    def __init__(self, key, val):
        self.prev = None
        self.next = None
        self.val = val
        self.key = key

class DoublyLinkedList:
    def __init__(self,):
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.size = 0
        self.head.next = self.tail
        self.head.prev = self.head

    def append(self, key, val):
        node = Node(key, val)

        p = self.tail.prev
        p.next = node
        self.tail.prev = node
        node.prev = p
        node.next = self.tail

        self.size += 1
        return node

    def pop(self):
        return self.remove(self.head.next)

    def remove(self, node):
        if self.size > 0:
            node.prev.next = node.next
            node.next.prev = node.prev

class LFUCache:

    def __init__(self, capacity: int):
