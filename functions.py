from models import *





def explicit(input):

    current = Symbol(input).read()

    if len(current.value) == len(input):
        return current.value

    next = Symbol(input[len(current.value)]).read()

    if isinstance(current,Operand) :
        if isinstance(next,Operand) or next.value == '(':

            return ( (current.value + '.') + explicit(input[len(current.value):]) )

    if isinstance(current,Operator):
        if current.value == '*':
            if isinstance(next,Operand) or next.value == '(':
                return ( (current.value + '.') + explicit(input[len(current.value):]) )

    if isinstance(current, Parenthesis):
        if current.value == ')':
            if isinstance(next, Operand) or next.value =='(':
                return ( (current.value + '.') + explicit(input[len(current.value):]) )
    return ( (current.value) + explicit(input[len(current.value):]) )


def infixToPostfix(infixexpr):
    prec = {
        "*" : 3,
        "." : 2,
        "+" : 1
    }
    opStack = Stack()
    posfixa = []
    entrada = infixexpr.split()

    def topo_maior_precedencia(i):
        try:
            a = prec[i]
            b = prec[opStack.peek()]
            return True if a <= b else False
        except KeyError:
            return False
    
    
    while len(infixexpr)>0:
        char = Symbol(infixexpr).read()
        
        if isinstance(char,Operand):
            posfixa.append(char.value)
        elif isinstance(char,Parenthesis):
            if char.value ==  '(':
                opStack.push(char.value)
            else:
                topToken = opStack.pop()
                while topToken != '(':
                    posfixa.append(topToken)
                    topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (topo_maior_precedencia(char.value)):
                  posfixa.append(opStack.pop())
            opStack.push(char.value)
            
        infixexpr =  infixexpr[len(char.value):]

    while not opStack.isEmpty():
        posfixa.append(opStack.pop())
    return "".join(posfixa)


def execute(output):
    if len(output)==0:
        return print('Expressão ainda não convertida') 
    stack = Stack()    
    
    while( len(output) > 0):         
        char = Symbol(output).read()
        if isinstance(char,Operand):
            stack.push(char.value)
        else: 
            if(not stack.isEmpty()):
                operand2 = stack.pop()
                if(char.value == '*'):
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
        output =  output[len(char.value):]
    operand1 = stack.pop()

    if(stack.isEmpty()):
        print('Expressão válida')
    else:
        print('Expressão inválida')