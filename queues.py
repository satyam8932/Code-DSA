class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        return self.queue.pop(0)

    def front(self):
        return self.queue[0]

    def rear(self):
        return self.queue[-1]

    def is_emtpy(self):
        return len(self.queue) == 0

# qu = Queue()
# qu.enqueue(1)
# qu.enqueue(2)
# qu.enqueue(3)
# qu.enqueue(4)
# qu.enqueue(5)

# print(qu.front())
# print(qu.rear())
# print(qu.is_emtpy())
# print(qu.dequeue())

# qu.enqueue(6)


class CircularQueue:
    def __init__(self, capacity):
        self.cqueue = [None] * capacity
        self.capacity = capacity
        self.first = 0
        self.last = 0
        self.size = 0

    def enqueue(self, data):
        if not self.is_full():
            self.cqueue[self.last] = data
            self.last = (self.last + 1) % self.capacity
            self.size += 1
        else:
            print("tis ain't yer mundane queue lad")

    def dequeue(self):
        if not self.is_empty():
            dequeued_val = self.cqueue[self.first]
            self.cqueue[self.first] = None
            self.size -= 1
            self.first = (self.first + 1) % self.capacity

            return dequeued_val
        else:
            print('are ye high lad?')

    def printCQueue(self):
        for i in self.cqueue:
            print(i, end = " ")
        print()

    def is_full(self):
        return self.capacity == self.size

    def is_empty(self):
        return self.size == 0

    def front(self):
        return self.cqueue[self.first]

    def rear(self):
        return self.cqueue[(self.last - 1) % self.capacity]



cq = CircularQueue(5)

cq.enqueue(1)
cq.enqueue(3)
cq.enqueue(4)
cq.enqueue(5)
cq.enqueue(6)
cq.dequeue()
cq.dequeue()
cq.enqueue(7)
cq.printCQueue()
print(cq.rear())
print(cq.last)