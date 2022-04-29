from stack import Stack

stack = Stack()

def execute(input): 
    x = 0
    ignore = False
    while(x <= (len(input)-1)):
        
        char = input[x]
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
                    valor = operand2
                    stack.push(valor) 
                else: 
                    if(not stack.isEmpty()):
                        operand1 = stack.pop()
                        valor = operand1+operand2
                        stack.push(valor)      
                    else:
                        return print('expressão inválida')        
            else:
                return print('expressão inválida')
        x+=1
    operand1 = stack.pop()
    if(stack.isEmpty()):
        print('expressão válida')