import pandas as pd
import sys
sys.path.insert(1, './colorize')
from rich_dataframe import prettify
from termcolor import colored

def visualization(table):
    transition_function = pd.DataFrame(table).T
    print('')
    print(colored('Tabela de transição:', 'yellow').center(155))
    transition_function = prettify(transition_function, clear_console=False, row_limit=100000, col_limit=100000)
    #print(transition_function)