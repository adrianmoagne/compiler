import pandas as pd
from rich_dataframe import prettify
from termcolor import colored

def visualization(table):
    transition_function = pd.DataFrame(table).T
    print('')
    print(colored('Tabela de transição:', 'cyan').center(155))
    transition_function = prettify(transition_function, clear_console=False)
    #print(transition_function)