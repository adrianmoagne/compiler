from stack import Stack


class posfix:
    def __init__(self, expression) -> None:
        self.precedency = {"*" : 3,"." : 2,"+" : 1}
        self.operatorsStack = Stack()
        self.output = []
        self.input = list(expression)

    def greaterPrecedency(self, i):
        try:
            a = self.precedency[i]
            b = self.precedency[self.operatorsStack.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    def convert(self):    
        for char in self.input:
            if char.isalpha():
               self.output.append(char)
            elif char == '(':
                self.operatorsStack.push(char)
            elif char == ')':
                topToken = self.operatorsStack.pop()
                while topToken != '(':
                    self.output.append(topToken)
                    topToken = self.operatorsStack.pop()
            else:
                while (not self.operatorsStack.isEmpty()) and \
                (self.greaterPrecedency(char)):
                    self.output.append(self.operatorsStack.pop())
                self.operatorsStack.push(char)

        while not self.operatorsStack.isEmpty():
            self.output.append(self.operatorsStack.pop())

        return " ".join(self.output)