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
    alphabet = get_alphabet(expression)
    positions = get_symbol_positions(expression)
    tree = syntax_tree(expression)
    followpos(tree,followposz)
    visualization(DFA(followposz,tree,positions, alphabet))