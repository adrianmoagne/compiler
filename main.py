from functions import *
from dfa import *
from visualization_trasition_function import visualization

flag = True
final, tokens = [], []
while flag:
    token = input(colored('Token: ', 'magenta'))
    tokens.append(token)
    inpt = input(colored('Expressão regular: ', 'magenta'))
    if inpt == '':
        flag = False
        continue
    exp = explicit(inpt)
    inpt = list(inpt)
    final.append(inpt)

tokens.pop()


if final:    
    exp = finalize(final)
    print(exp)
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
        #print(followposz)
        #print(alphabet)
        #print(positions)
        transition_function, aux = DFA(followposz,tree,positions,alphabet)
        finalstates = []
        for item in aux:
            if '#' in item:
                item = item.replace('#', '')
                finalstates.append(item)
        final_list = [tokens[i]+' => '+finalstates[i] for i in range(len(tokens))]
        print('\n'.join(final_list))
                
        visualization(transition_function)
    
except:
    print(colored('Expressão inválida', 'red'))
   
