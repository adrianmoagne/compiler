from models import *

# Retorna a expressão regular expandida
def augmentedRE(rexpression):
    return rexpression+'#.'
    

def iterativePreorder(root):
    if root is None:
        return
    nodeStack = []
    nodeStack.append(root)
    output = []
    while(len(nodeStack) > 0):
        node = nodeStack.pop()
        output.append(node)
        if node.right is not None:
            nodeStack.append(node.right)
        if node.left is not None:
            nodeStack.append(node.left)      
    return output         

def nullable(node):
    if node.value == '&':
        return True
    elif node.value == '*':
        return True
    elif node.value == '+':
        return nullable(node.left) or nullable(node.right)

    elif node.value  == '.':
        return nullable(node.left) and nullable(node.right)
    
    return False


       
def syntax_tree(input):
    stack = Stack() 
    i = 0
    while len(input) > 0:
        char = Symbol(input).read()
        if isinstance(char,Operand):
            node_operand = Node(char.value)
            node_operand.firstposz = {i}
            node_operand.lastposz = {i}
            i+=1
            stack.push(node_operand)
        else: 
            if(not stack.isEmpty()):
                if(char.value == '*'):
                    node_operand = stack.pop()
                    next = Node(char.value)
                    next.left = node_operand
                    stack.push(next)
                    next.firstposz = node_operand.firstposz
                    next.lastposz = node_operand.lastposz
                else: 
                    if(not stack.isEmpty()):
                        
                        node_operand1 = stack.pop()
                        node_operand2 = stack.pop()
                        if not isinstance(node_operand1,Node):
                            node_operand1 = Node(node_operand1)
                            node_operand1.firstposz = {i}
                            node_operand1.lastposz = {i}
                            i+=1
                        if not isinstance(node_operand2,Node):   
                            node_operand2 = Node(node_operand2)
                            node_operand2.firstposz = {i}
                            node_operand2.lastposz = {i}
                            i+=1
                        next = Node(char.value)
                       
                        
                        next.right = node_operand1
                        next.left = node_operand2
                        if char.value == '+':
                            next.firstposz = next.right.firstposz.union(next.left.firstposz)
                            next.lastposz = next.right.lastposz.union(next.left.lastposz)
                        else:
                            if nullable(next.left):
                                next.firstposz = next.right.firstposz.union(next.left.firstposz)
                            else:
                                next.firstposz = next.left.firstposz
                                
                                
                            if nullable(next.right):
                                next.lastposz = next.right.lastposz.union(next.left.lastposz)
                            else:
                                next.lastposz = next.right.lastposz
                        stack.push(next)
                        
        input =  input[len(char.value):]
    
    x = stack.pop()
    x = iterativePreorder(x)
    return x
    
                     
# a*b*.#.                     
#  a*b*.**cd.w.+pa.a.+
#  a*b*.**cd.w.+pa.a.+                  
# ((a*b*)*)*+cdw+paa                                      
                    

# for node in tree:
#     print(node.value, node.firstposz,node.lastposz)
                  


followposz ={} 
# Calcula followpos para cada folha marcada com uma posição i 
def followpos(nodes, followposz):
    for node in nodes:
        if node.value == '.':
            for i in node.left.lastposz:
                if i not in followposz:
                    followposz[i] = node.right.firstposz
                else:
                    followposz[i] = followposz[i].union(node.right.firstposz)
                    
        if node.value == '*':
            for i in node.lastposz:
                if i not in followposz:
                    followposz[i] = node.firstposz
                else:
                    followposz[i] = followposz[i].union(node.firstposz)
        
        
        if node.value == '#':
            followposz[list(node.firstposz)[0]]=set()
        
    #print(followposz)

  


def get_alphabet(input):
    alphabet = []
    while len(input)>0:
        char = Symbol(input).read()
        if char.value not in ['*','+','.','#', '&'] and char.value not in alphabet:
            alphabet.append(char.value)
        input = input[len(char.value):]
            
    return alphabet


def get_symbol_positions(input):
    symbol_positions = []
    while len(input) > 0:
        char = Symbol(input).read()
        if char.value not in ['.', '+', '*']:
            symbol_positions.append(char.value)
        input = input[len(char.value):] 
    return symbol_positions
'''
def transition(transition_function, state, word, i):
    if '*' in state and i == len(word)-1:
        return state
    return transition(transition_function, transition_function[state][word[i]], word, i+1)'''

def DFA(followposz, nodes,postions,alphabet):
    q0 = nodes[0].firstposz
    aux = postions.copy()
    #print(f'q0 =  {q0}')
    states, states_unmarked = [], []
    i = 0
    transition_function = {}
    states_unmarked.append(q0)
    exit = len(states_unmarked)

    while(exit > 0):
        flag = False
        state = states_unmarked.pop(0)
        states.append(state)
        for symbol in alphabet:
            U = set()        
            for position in state:
                if postions[position] == '#':
                    pos = position
                    flag = True
                if postions[position] == symbol:
                    U = U.union(followposz[position])
            if U not in states_unmarked and U not in states:
                states_unmarked.append(U)
            if flag:
                
                if state == q0:
                    if '->*q'+str(i) in transition_function:
                        transition_function['->*q'+str(i)].update({symbol:U})
                        
                    else: 
                        transition_function['->*q'+str(i)] = {symbol:U} 
                        aux[pos] = '->*q'+str(i)+' '+aux[pos] 
                        
                   
                else:
                    if '*q'+str(i) in transition_function:
                        transition_function['*q'+str(i)].update({symbol:U})
                        
                    else: 
                        transition_function['*q'+str(i)] = {symbol:U} 
                        aux[pos] = '*q'+str(i)+' '+aux[pos]
                        
                
                   
            elif state == q0:
                if '->q'+str(i) in transition_function:
                    transition_function['->q'+str(i)].update({symbol:U})
                else: 
                    transition_function['->q'+str(i)] = {symbol:U}
                 
            else:
                if 'q'+str(i) in transition_function:
                    transition_function['q'+str(i)].update({symbol:U})
                else: 
                    transition_function['q'+str(i)] = {symbol:U}
             
        i+=1
        exit = len(states_unmarked)
    
   
    #print(transition_function)
 

    for value in transition_function:
        for x in transition_function[value]:  
            transition_function[value][x]='q'+str(states.index(transition_function[value][x]))

    for value in transition_function:
        for x in transition_function[value]:  
            for keys in transition_function.keys():
                if transition_function[value][x] in keys:
                    transition_function[value][x] = keys


    # for value in transition_function:
    #     for x in transition_function[value]:
    #         if transition_function[value][x] == value and '*' in value:
    #             if '>' in value:
    #                 transition_function[value][x]='->*q'+str(states.index(transition_function[value][x]))
    #             transition_function[value][x]='*q'+str(states.index(transition_function[value][x]))
    
    for index in range(len(states)):
        states[index] = 'q'+str(index)
        for value in transition_function.keys():
            if states[index] in value and '*' in value:
                states[index] = '*'+states[index]
    states[0] = '->q0'
    
    
    
    print(f'Q = {states}')
    print('')
    #print(transition_function)
 
    #minimization(alphabet,transition_function,states)
    return transition_function, aux


'''
def minimization(alphabet,transition_function,Q):
    tabela = {}
    flag = True
    for state in transition_function:
        for next in transition_function:
            if state != next and next+state not in tabela:
                if ('*' in state and '*' not in next) or ('*' in next and '*' not in state):
                    tabela.update({state+next:1})
                else:
                    tabela.update({state+next:0})
    
    while(flag):
        flag = False
        for letter in alphabet:
            for state in transition_function:
                for next in transition_function:          
                    if state != next and next+state not in tabela:
                        if transition_function[state][letter] != transition_function[next][letter] and transition_function[next][letter]+transition_function[state][letter] not in tabela:
                            if tabela[state+next] == 0 and tabela[transition_function[state][letter]+transition_function[next][letter]] == 1:
                                tabela.update({state+next:1})
                                flag = True
                            
        


    
    print(tabela)'''
    
