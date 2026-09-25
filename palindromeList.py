from __future__ import annotations

class Node:
    def __init__(self, data: int) -> None:
        self.data = data
        self.next: Node | None = None

    def insertNode(self, data: int) -> None:
        current = self

        while current.next is not None:
            current = current.next

        current.next = Node(data)

    def reverseList(self) -> Node | None:
        prev: Node | None = None
        curr: Node | None = self

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp

        return prev

head = Node(1)
head.insertNode(2)
head.insertNode(3)
head.insertNode(4)
head.insertNode(5)

temp = head
while temp:
    print(temp.data)
    temp = temp.next

revList = head.reverseList()

while revList:
    print(revList.data)
    revList = revList.next