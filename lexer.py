import pickle

with open('dfa_data.pkl', 'rb') as inp:
    transition_function = pickle.load(inp)
    states = pickle.load(inp)
    states2 = pickle.load(inp)
    final_list = pickle.load(inp)
    tokens = pickle.load(inp)



def lexer(transition_function, tape, last_position):
    q = '->q0'
    p = None
    i = 0
    y = last_position
    while y < len(tape):
        x = tape[y]
        if x in transition_function[q]:
            q = transition_function[q][x]
            if '*' in q:
                p = q
                i = 0
            elif states[(states2.index(q))] == set():
                break
            else:
               i+=1
        else:
            break     
        y += 1
    if p != None:
        for token in range(len(final_list)):
                if p == final_list[token][0:final_list[token].index(' ')]:
                    return '<'+tokens[token]+'>', y-i
    
    return tape[y-i:y+1], y+1 
        

tape = input('Digite o código a ser analisado: ')
tokenized = [''] * len(tape)
last_position = 0
for token in range(len(tokenized)):
    try:
        tokenized[token], last_position = lexer(transition_function, tape, last_position)
        #print(tokenized[token])
        #print(last_position)
    except:
        continue

print(''.join(tokenized))

    
    

    





