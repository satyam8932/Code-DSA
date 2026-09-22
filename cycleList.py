# Detect Cycle in Linked list

from __future__ import annotations

class Node:
    def __init__(self, data: int) -> None:
        self.data = data
        self.next: None | Node = None

    def insertNode(self, data: int) -> None:
        current: Node = self
        while current.next is not None:
            current = current.next
        current.next = Node(data)

    def detectCycle(self) -> bool:
        slow: None | Node = self
        fast: None | Node = self

        while slow is not None and fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False

head = Node(10)
for val in [20, 30, 40, 50, 60, 70, 80, 90, 100]:
    head.insertNode(val)

tail: Node = head
while tail.next is not None:
    tail = tail.next

tail.next = head


print(head.detectCycle())  # Output: True