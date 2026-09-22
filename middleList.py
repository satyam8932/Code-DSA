from __future__ import annotations

class Node:
    def __init__(self, data: int) -> None:
        self.data: int = data
        self.next: Node | None = None

    def insertNode(self, data: int) -> None:
        current: Node = self
        while current.next is not None:
            current = current.next
        current.next = Node(data)

    def middleNode(self) -> int:
        current: Node | None = self
        counter: int = 0

        while current is not None:
            current = current.next
            counter += 1

        mid: Node = self
        midCounter: int = 0
        while mid.next is not None:
            if midCounter == (counter/2):
                break
            mid = mid.next
            midCounter += 1

        return midCounter


head = Node(1)
head.insertNode(2)
head.insertNode(3)
head.insertNode(4)
head.insertNode(5)
head.insertNode(6)

print(head.middleNode())
