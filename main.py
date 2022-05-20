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
    # z*v*c*2*3*4*5*7*78*u*g*c*  -> bug sem estado final
    #expression = augmentedRE(pos)
    alphabet = get_alphabet(pos)
    positions = get_symbol_positions(pos)
    tree = syntax_tree(pos)
    #for node in tree:
    #    print(node.value, node.firstposz,node.lastposz)
    followpos(tree,followposz)
    print(followposz)
    print(alphabet)
    print(positions)
    visualization(DFA(followposz,tree,positions,alphabet))
 
   
