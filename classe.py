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
        flag = False
        try:
            for char in self.input:            
                if ((char.isascii() and char not in ['+', '.', '*', '(', ')', '\\', ' ']) or flag): 
                    if flag:
                        flag = False
                        self.output.append('\\'+char)
                    else:    
                        self.output.append(char)
                elif (char == '\\'):
                    flag = True
                elif char == '(':
                    self.operatorsStack.push(char)
                elif char == ')':
                    top = self.operatorsStack.pop()
                    while top != '(':
                        self.output.append(top)
                        top = self.operatorsStack.pop()        
                else:
                    while (not self.operatorsStack.isEmpty()) and (self.greaterPrecedency(char)):
                        self.output.append(self.operatorsStack.pop())
                    self.operatorsStack.push(char)

            while not self.operatorsStack.isEmpty():
                self.output.append(self.operatorsStack.pop())

            self.output = list((''.join(self.output)).replace(' ', ''))
            print(self.output)

        except:
            self.output = []
            print('expressão inválida')

    def execute(self):
        if self.output == []:
            return print('expressão ainda não convertida') 
        stack = Stack()    
        x = 0
        while(x <= (len(self.output)-1)):         
            char = self.output[x]
            if(char.isascii() and char not in ['+', '.', '*', '(', ')']):
                if(char == '\\'):
                    stack.push(char+input[x+1])
                    x+=1
                else:
                    stack.push(char)
            else: 
                if(not stack.isEmpty()):
                    operand2 = stack.pop()
                    if(char == '*'):
                        value = operand2
                        stack.push(value) 
                    else: 
                        if(not stack.isEmpty()):
                            operand1 = stack.pop()
                            value = operand1+operand2
                            stack.push(value)      
                        else:
                            return print('expressão inválida')        
                else:
                    return print('expressão inválida')
            x+=1
        operand1 = stack.pop()

        if(stack.isEmpty()):
            print('expressão válida')
        else:
            print('expressão inválida')