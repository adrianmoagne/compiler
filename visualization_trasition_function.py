import pandas as pd
#from rich_dataframe import prettify

def visualization(table):
    transition_function = pd.DataFrame(table).T
    #transition_function = prettify(transition_function)
    print(transition_function)