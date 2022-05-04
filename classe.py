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

    def explicit(self):
        caracteres = self.input
        i=0
        while i<=(len(caracteres)-2):
            if caracteres[i].isalpha():
                if caracteres[i+1].isascii() and caracteres[i+1] not in ['*','.','+']:
                    caracteres.insert(i+1,'.')     

            elif caracteres[i] == '\\':
                if i+2 == len(caracteres):
                    pass
                elif caracteres[i+1] == '\\':
                    caracteres.insert(i+2,'.')
                elif caracteres[i-1] == '\\':
                    pass
            
            elif (caracteres[i-1]=='\\' and caracteres[i]!='\\' ):
                if len(caracteres) > i+2:
                    if(caracteres[i+2] !='\\' and caracteres[i-2]!='\\'):
                        caracteres.insert(i+1,'.')
                else:
                    caracteres.insert(i+1,'.')
                   
            elif caracteres[i]==')' and caracteres[i+1]=='(':
                caracteres.insert(i+1,'.')
                
            elif caracteres[i].isalpha() and caracteres[i+1]=='(':
                caracteres.insert(i+1,'.')
                
            elif caracteres[i]==')' and caracteres[i+1].isalpha():
                caracteres.insert(i+1,'.')
            
            elif caracteres[i]=='*' and caracteres[i+1].isalpha():
                caracteres.insert(i+1,'.')
            
            elif caracteres[i].isascii() and caracteres[i] not in ['*','.','+']:
                caracteres.insert(i+1,'.')          
            i+=1
        self.input = caracteres
        print('Expressão explícita: '+''.join(caracteres))

    def convert(self):
        flag = False
        try:
            for char in self.input:            
                if (((char.isascii() or char == 'ç') and char not in ['+', '.', '*', '(', ')', '\\', ' ']) or flag): 
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
            print('Expressão posfixa: '+''.join(self.output))

        except:
            self.output = []
            print('Expressão inválida')

    def execute(self):
        if self.output == []:
            return print('Expressão ainda não convertida') 
        stack = Stack()    
        x = 0
        while(x < len(self.output)):         
            char = self.output[x]
            if((char.isascii() or char == 'ç') and char not in ['+', '.', '*', '(', ')']):
                if(char == '\\'):
                    stack.push(char+self.output[x+1])
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
                            return print('Expressão inválida')        
                else:
                    return print('Expressão inválida')
            x+=1
        operand1 = stack.pop()

        if(stack.isEmpty()):
            print('Expressão válida')
        else:
            print('Expressão inválida')