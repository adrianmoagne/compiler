from functions import *
from dfa import *
from visualization_trasition_function import visualization
import pickle



final = [   
        list('/.\*.(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+y+x+z+ )*./.\*'), 
        list('for'), 
        list("print\((a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+y+x+z+ +')*\)")
        ]
tokens = ['comment', 'for', 'print']

'''
flag = True
final, tokens = [], []
while flag:
    token = input(colored('Token: ', 'magenta'))
    tokens.append(token)
    if token == '':
        flag = False
        continue
    inpt = input(colored('Expressão regular: ', 'magenta'))
    inpt = list(inpt)
    final.append(inpt)

tokens.pop()
'''

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
        #print(followposz)
        #print(alphabet)
        #print(positions)
        transition_function, aux, states, states2 = DFA(followposz,tree,positions,alphabet)
        finalstates = []
        for item in aux:
            if '#' in item:
                item = list(item.replace('#', '').replace(' ', ','))
                item.pop(-1)
                item = ''.join(item)
                finalstates.append(item)
        final_list = ['('+finalstates[i]+')'+' '+'=>'+' '+tokens[i] for i in range(len(tokens))]
        print(colored('Estados finais + tokens:', 'red'))
        print('\n'.join(final_list))          
        visualization(transition_function)

        with open('dfa_data.pkl', 'wb') as outp:
            pickle.dump(transition_function, outp, pickle.HIGHEST_PROTOCOL)
            pickle.dump(states, outp, pickle.HIGHEST_PROTOCOL)
            pickle.dump(states2, outp, pickle.HIGHEST_PROTOCOL)
            pickle.dump(final_list, outp, pickle.HIGHEST_PROTOCOL)
            pickle.dump(tokens, outp, pickle.HIGHEST_PROTOCOL)
            pickle.dump(final, outp, pickle.HIGHEST_PROTOCOL)

except:
    print(colored('Expressão inválida', 'red'))