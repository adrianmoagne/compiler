from functions import *
from dfa import *
from visualization_trasition_function import visualization



t = input('Expressão regular: ')
exp = explicit(t)


try:
    pos = infixToPostfix(exp)
except:
    print('Expressão inválida')

exc = execute(pos)
if exc:
    print('Expressão explicita: ' + exp)
    print('Experessão posfixa: ' + pos)
    # abcw+cw
    expression = augmentedRE(pos)
    alphabet = get_alphabet(expression)
    positions = get_symbol_positions(expression)
    tree = syntax_tree(expression)
    for node in tree:
        print(node.value, node.firstposz,node.lastposz)
    followpos(tree,followposz)
    print(followposz)
    print(alphabet)
    print(positions)
    dfa,mini= DFA(followposz,tree,positions,alphabet)
    visualization(dfa)
    visualization(mini)
    
 
   
