# Quíntupla dos autômatos finitos deterministas
dfa_definition = ['Q', 'Σ', 'δ', 'q0', 'F']

# Resultados das funções de firstpos e lastpos para todos os nós e folhas da árvore
# São dicionários, da seguinte forma: "PosiçãoNóLista":"ConjuntoDeInteiros"
firstposz = {}
lastposz = {}

# Acha um elemento em uma lista de listas
def IsIn(element, place):
    for i in place:
        if isinstance(i, list):
            if IsIn(element, i):
                return True
        else:
            if element == i:
                return True
    return False

# Retorna a expressão regular expandida
def augmentedRE(rexpression):
    return rexpression+'#.'
    

# Abstração da árvore de sintaxe usando lista
def syntaxtree(rexpression): #  ab+*b.#.
    nodes = list(rexpression)
    positions = []
    alphabet = []
    for i in range(len(nodes)):  
        positions.append(i)
    for node in nodes:
        if node not in ['.', '+', '*', '#'] and node not in alphabet:
            alphabet.append(node)
    print(f'Nodes: {nodes}')
    print(f'Positions: {positions}')
    print(f'Alphabet: {alphabet}')
    return nodes, positions, alphabet


# Calcula a função nullable para um dado nó ou folha, levando em consideração seu(s) filho(s)
def nullable(node, i, nodes):
    if node == '&':
        return True
    elif node == '*':
        return True
    elif node == '+':
        if nodes[i-1] == '*':
            return nullable(nodes[i-3], i-3, nodes) or nullable(nodes[i-1], i-1, nodes)
        else:
            return nullable(nodes[i-2], i-2, nodes) or nullable(nodes[i-1], i-1, nodes)
    elif node  == '.':
        if nodes[i-1] == '*':
            return nullable(nodes[i-3], i-3, nodes) and nullable(nodes[i-1], i-1, nodes)
        else:
            return nullable(nodes[i-2], i-2, nodes) and nullable(nodes[i-1], i-1, nodes)
    return False


# Calcula a função firstpos
def firstpos(nodes, positions):
    # Para as folhas
    x = 0
    for position in positions:
        if nodes[x] == '&':
            firstposz.update({position:set()})
        else:
            firstposz.update({position:set([position])})
        x+=1
    # Para os nós
    for i in range(len(nodes)):
        if nodes[i] == '+':
            if nodes[i-1] == '*':
                 firstposz.update({i:firstposz[i-3].union(firstposz[i-1])})
            else:
                firstposz.update({i:firstposz[i-2].union(firstposz[i-1])})
        if nodes[i] == '*':
            firstposz.update({i:firstposz[i-1]})
        if nodes[i] == '.':
            if nodes[i-1] == '*':
                if nullable(nodes[i-3], i-3, nodes):
                    firstposz.update({i:firstposz[i-3].union(firstposz[i-1])})
                else:
                    firstposz.update({i:firstposz[i-3]})
            else:
                if nullable(nodes[i-2], i-2, nodes):
                    firstposz.update({i:firstposz[i-2].union(firstposz[i-1])})
                else:
                    firstposz.update({i:firstposz[i-2]})


# Calcula a função lastpos
def lastpos(nodes, positions):
    # Para as folhas
    i = 0
    for position in positions:
        if nodes[i] == '&':
            lastposz.update({position:set()})
        elif position not in ['*', '+', '.']:
            lastposz.update({position:set([position])})
        i+=1
    # Para os nós
    for i in range(len(nodes)):
        if nodes[i] == '+':
            if nodes[i-1] == '*':
                lastposz.update({i:lastposz[i-3].union(lastposz[i-1])})
            else:
                lastposz.update({i:lastposz[i-2].union(lastposz[i-1])})
        if nodes[i] == '*':
            lastposz.update({i:lastposz[i-1]})
        if nodes[i] == '.':
            if nodes[i-1] == '*':
                if nullable(nodes[i-1], i-1, nodes):
                    lastposz.update({i:lastposz[i-3].union(lastposz[i-1])})
                else:
                    lastposz.update({i:lastposz[i-1]})
            else:
                if nullable(nodes[i-1], i-1, nodes):
                    lastposz.update({i:lastposz[i-2].union(lastposz[i-1])})
                else:
                    lastposz.update({i:lastposz[i-1]})


# Calcula followpos para cada folha marcada com uma posição i 
def followpos(nodes, followposz):
    i = 0
    for node in nodes:
        if node == '.':
            if nodes[i-1] == '*':
                for position in lastposz[i-3]:
                    followposz[position] = followposz[position].union(firstposz[i-1])
            else:
                for position in lastposz[i-2]:
                    followposz[position] = followposz[position].union(firstposz[i-1])      
        elif node == '*':
            for position in lastposz[i]:
                followposz[position] = followposz[position].union(firstposz[i])
        i+=1 

    return followposz


def DFA(followposz, nodes, positions, alphabet):
    q0 = firstposz[positions[-1]]
    print(f'q0 =  {q0}')
    states, states_unmarked = [], []
    i = 0
    trasition_function = {}
    states_unmarked.append(q0)
    exit = len(states_unmarked)
    teste = {}
    while(exit > 0):
        flag = False
        state = states_unmarked.pop()
        states.append(state)
        for symbol in alphabet:
            U = set()        
            for position in state:
                if nodes[position] == '#':
                    flag = True
                if nodes[position] == symbol:
                    U = U.union(followposz[position])
            if U not in states_unmarked and U not in states:
                states_unmarked.append(U)
            if flag:
                if state == q0:
                    if '->*q'+str(i) in teste:
                        teste['->*q'+str(i)].update({symbol:U})
                    else: 
                        teste['->*q'+str(i)] = {symbol:U} 
                    trasition_function.update({'('+'->'+'*'+'q'+str(i)+','+symbol+')':U})
                else:
                    if '*q'+str(i) in teste:
                        teste['*q'+str(i)].update({symbol:U})
                    else: 
                        teste['*q'+str(i)] = {symbol:U} 
                
                    trasition_function.update({'('+'*'+'q'+str(i)+','+symbol+')':U})
            elif state == q0:
                if '->q'+str(i) in teste:
                    teste['->q'+str(i)].update({symbol:U})
                else: 
                    teste['->q'+str(i)] = {symbol:U}
                trasition_function.update({'('+'->'+'q'+str(i)+','+symbol+')':U})  
            else:
                if 'q'+str(i) in teste:
                    teste['q'+str(i)].update({symbol:U})
                else: 
                    teste['q'+str(i)] = {symbol:U}
                trasition_function.update({'('+'q'+str(i)+','+symbol+')':U})
        i+=1
        exit = len(states_unmarked)
    
    
    #print(f'Q = {Q}')
    #print(trasition_function)
    
   
    for value in trasition_function:
     
        if trasition_function[value] in states:
            trasition_function.update({value:'q'+str(states.index(trasition_function[value]))})
        else:
            trasition_function.update({value:'q'+str(states.index(trasition_function[value]))})

    for value in teste:
        for x in teste[value]:
            teste[value][x]='q'+str(states.index(teste[value][x]))
    
    for index in range(len(states)):
        states[index] = 'q'+str(index)

    #print(f'Q = {Q}')
   # print(δ)
   # print(teste)
    return teste

        




