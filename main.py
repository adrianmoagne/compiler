from functions import *
from dfa import *
from visualization_trasition_function import visualization
import os
import sys
sys.path.insert(1, './colorize')
from termcolor import colored

exit = False

while(not exit):
    t = input(colored('Expressão regular: ', 'blue'))
    if t == '':
        continue
    exp = explicit(t)
    if t == 'clear':
        os.system('clear')
        continue
    if t == 'exit':
        exit = True
        continue

    try:
        pos = infixToPostfix(exp)
    except:
        print(colored('Expressão inválida', 'red'))
        continue

    exc = execute(pos)
    if exc:
        print('Expressão explicita: ' + exp)
        print('Experessão posfixa: ' + pos)

        expression = augmentedRE(pos)
        alphabet = get_alphabet(expression)
        positions = get_symbol_positions(expression)
        tree = syntax_tree(expression)
        followpos(tree,followposz)
        visualization(DFA(followposz,tree,positions,alphabet))
    