import pickle
from visualization_trasition_function import visualization
import sys
sys.path.insert(1, './colorize')
from termcolor import colored

with open('dfa_data.pkl', 'rb') as inp:
    transition_function = pickle.load(inp)
    states = pickle.load(inp)
    states2 = pickle.load(inp)
    final_list = pickle.load(inp)
    tokens = pickle.load(inp)
    final = pickle.load(inp)

visualization(transition_function)
#print(states)
#print(states2)
print(colored('Estados finais + tokens:', 'red'))
print('\n'.join(final_list))
final = [''.join(final[i]) for i in range(len(final))]
final = [final[i].replace('#+', '').replace('+#', '').replace('#', '')+' => '+tokens[i] for i in range(len(final))]
final = '\n'.join(final)
print(colored('Expressões regulares:', 'magenta'))
print(final)