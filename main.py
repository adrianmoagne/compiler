from functions import *
from dfa import *
from visualization_trasition_function import visualization



t = input('Expressão regular: ')
exp = explicit(t)


try:
    pos = infixToPostfix(exp)
    pos = augmentedRE(pos)
except:
    print('Expressão inválida')

exc = execute(pos)
if exc:
    print('Expressão explicita: ' + exp)
    print('Experessão posfixa: ' + pos)
    alphabet = get_alphabet(pos)
    positions = get_symbol_positions(pos)
    tree = syntax_tree(pos)
    followpos(tree,followposz)
    visualization(DFA(followposz,tree,positions,alphabet))
 
   
