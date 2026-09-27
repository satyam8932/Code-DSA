class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0
    



st = Stack()
st.push(1)
st.push(2)
st.push(3)
st.push(4)
st.push(5)

print(st.peek())
