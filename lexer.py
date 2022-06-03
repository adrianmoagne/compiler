import pickle

with open('dfa_data.pkl', 'rb') as inp:
    transition_function = pickle.load(inp)
    states = pickle.load(inp)
    states2 = pickle.load(inp)
    final_list = pickle.load(inp)
    tokens = pickle.load(inp)
    #final = pickle.load(inp)
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
                if '('+p+')' in final_list[token] or '('+p+',' in final_list[token] or ','+p+',' in final_list[token] or ','+p+')' in final_list[token]:
                    return '<'+tokens[token]+'>', y-i
    
    return tape[y-i:y+1], y+1 
        
with open('tape.txt') as tape:
    for line in tape:
        line = list(line)
        #tape = input('Digite o código a ser analisado: ')
        tokenized = [''] * len(line)
        i = 0
        
        while True:
            if i < len(line):
                if line[i] == '\\':
                    line[i+1] = '\\'+line[i+1]
                    line.pop(i)
            else:
                break
            i+=1
        
        last_position = 0
        for token in range(len(tokenized)):
            try:
                tokenized[token], last_position = lexer(transition_function, line, last_position)
                if last_position >= len(line):
                    break
                #print(tokenized[token])
                #print(last_position)
            except:
                continue
        tokenized = [''.join(tokenized[i]) for i in range(len(tokenized))]
        print(''.join(tokenized), end='')
# expressão regular bugada -> (/.\*.(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+y+x+z+ )*./.\*)
    
    
#DONE lexer não lê \Símbolo
    





