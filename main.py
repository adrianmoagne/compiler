from functions import *
from dfa import *
from visualization_trasition_function import visualization

flag = True
final = []
while flag:
    inpt = input(colored('Expressão regular: ', 'magenta'))
    if inpt == '':
        flag = False
        continue
    exp = explicit(inpt)
    inpt = list(inpt)
    final.append(inpt)

if final:    
    exp = finalize(final)
    exp = explicit(exp)


try:
    pos = infixToPostfix(exp)
    exc = execute(pos)

    if exc:
        print(colored('Expressão explicita: ', 'blue') + exp)
        print(colored('Experessão posfixa: ', 'cyan') + pos)
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
except:
    print(colored('Expressão inválida', 'red'))
   
