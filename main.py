from functions import *

x = explicit(input('Expressão regular: '))
print('Expressão explicita: ' + x)

y = infixToPostfix(x)
print('Experessão posfixa: ' + y)

x = execute(y)
