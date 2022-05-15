from functions import *
from dfa import *
from visualization_trasition_function import visualization
x = explicit(input('Expressão regular: '))
print('Expressão explicita: ' + x)

y = infixToPostfix(x)
print('Experessão posfixa: ' + y)

x = execute(y)

if x:
    expression = augmentedRE(y)
    nodes, positions, alphabet = syntaxtree(expression)
    followposz = dict.fromkeys(positions, set())
    firstpos(nodes, positions)
    lastpos(nodes, positions)
    followposz = followpos(nodes, followposz)
    print(f'Firstpos: {firstposz}')
    print(f'Lastpos: {lastposz}')
    print(f'Followpos: {followposz}')

    visualization(DFA(followposz, nodes, positions, alphabet))