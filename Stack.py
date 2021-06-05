class Stack:
    def __init__(self):
        self.stack = []
    def peek(self):
        return self.stack[-1]
    def push(self, data):
        self.stack.append(data)
    def pop(self):
        return self.stack.pop()
    def isEmpty(self):
        return self.stack == []