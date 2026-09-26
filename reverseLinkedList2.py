class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def insertNode(self, data):
        current = self
        while current.next:
            current = current.next

        current.next = Node(data)

    def reverseList(self, left, right):
        prev = Node(0)
        prev.next = self

        for _ in range(left - 1):
            prev = prev.next

        curr = prev.next

        for _ in range(right - left):
            node_to_move = curr.next
            curr.next = node_to_move.next
            node_to_move.next = prev.next
            prev.next = node_to_move

head = Node(1)
head.insertNode(2)
head.insertNode(3)
head.insertNode(4)
head.insertNode(5)

head.reverseList(2, 4)
temp1 = head
while temp1:
    print(temp1.data, end=" ")
    temp1 = temp1.next

