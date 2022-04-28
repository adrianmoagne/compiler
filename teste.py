from stack import Stack




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
    
    
    for char in entrada:
        if char.isalpha():
            posfixa.append(char)
        elif char == '(':
            opStack.push(char)
        elif char == ')':
            topToken = opStack.pop()
            while topToken != '(':
                posfixa.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (topo_maior_precedencia(char)):
                  posfixa.append(opStack.pop())
            opStack.push(char)

    while not opStack.isEmpty():
        posfixa.append(opStack.pop())
    return " ".join(posfixa)

print(infixToPostfix("( A + B ) * C + D"))

