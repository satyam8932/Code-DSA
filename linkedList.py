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

    def searchNode(self, target: int) -> bool:
        current: Node | None = self
        while current is not None:
            if current.data == target:
                return True
            current = current.next
        return False

    def deleteNode(self, target: int) -> None:
        current: Node = self
        while current.next is not None:
            if current.next.data == target:
                current.next = current.next.next
                return
            current = current.next


head = Node(10)

head.insertNode(20)
head.insertNode(30)
head.insertNode(40)
head.insertNode(50)
head.insertNode(60)
head.insertNode(70)

print(head.searchNode(50))
head.deleteNode(60)

current: Node | None = head
while current is not None:
    print(current.data)
    current = current.next