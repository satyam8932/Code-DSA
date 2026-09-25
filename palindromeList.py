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

    def palindrome(self) -> bool:
        fast: Node | None = self
        slow: Node | None = self

        # Find middle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Reverse Second Half
        # If Fast is none means the list was even and slow is on the first of next half
        # If fast is not none means the list was odd and slow is on the middle of list
        # So start the curr correctly to ensure we cover all elements in second half
        curr: Node | None = slow if fast is None else slow.next
        prev: Node | None = None

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp

        # Compare Both Halves
        left: Node | None = self
        right: Node | None = prev
        
        while left and right:
            if left.data != right.data: return False
            left = left.next
            right = right.next
        return True



        



head = Node(1)
head.insertNode(2)
head.insertNode(3)
head.insertNode(4)
head.insertNode(6)
head.insertNode(3)
head.insertNode(2)
head.insertNode(1)

# temp = head
# while temp:
#     print(temp.data)
#     temp = temp.next

# revList = head.reverseList()

# while revList:
#     print(revList.data)
#     revList = revList.next

print(head.palindrome())