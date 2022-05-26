
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
        


  


def get_alphabet(input):
    alphabet = []
    while len(input)>0:
        char = Symbol(input).read()
        if char.value not in ['*','+','.','#'] and char.value not in alphabet:
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


def DFA(followposz, nodes,postions,alphabet):

    q0 = nodes[0].firstposz
    
    states, states_unmarked = [], []
    i = 0
    transition_function = {}
    states_unmarked.append(q0)
    exit = len(states_unmarked)
    new_trasition = []
    while(exit > 0):
        flag = False
        state = states_unmarked.pop(0)
        states.append(state)
        for symbol in alphabet:
            U = set()        
            for position in state:
                if postions[position] == '#':
                    flag = True
                if postions[position] == symbol:
                    U = U.union(followposz[position])
            if U not in states_unmarked and U not in states:
                states_unmarked.append(U)
            if flag:
                if state == q0:
                    if '->*q'+str(i) in transition_function:
                        transition_function['->*q'+str(i)].update({symbol:U})
                        new_trasition[i].transition.update({symbol:U})
                        new_trasition[i].final = True
                    else: 
                        transition_function['->*q'+str(i)] = {symbol:U}
                        new_trasition.append(State(i,state,{symbol:U}))
                        new_trasition[i].final = True
                        
                   
                else:
                    if '*q'+str(i) in transition_function:
                        transition_function['*q'+str(i)].update({symbol:U})
                        new_trasition[i].transition.update({symbol:U})
                        new_trasition[i].final = True
                        
                    else: 
                        transition_function['*q'+str(i)] = {symbol:U}
                        new_trasition.append(State(i,state,{symbol:U}))
                        new_trasition[i].final = True
                        
                
                   
            elif state == q0:
                if '->q'+str(i) in transition_function:
                    transition_function['->q'+str(i)].update({symbol:U})
                    new_trasition[i].transition.update({symbol:U})
                else: 
                    transition_function['->q'+str(i)] = {symbol:U}
                    new_trasition.append(State(i,state,{symbol:U}))
                 
            else:
                if 'q'+str(i) in transition_function:
                    transition_function['q'+str(i)].update({symbol:U})
                    new_trasition[i].transition.update({symbol:U})
                else: 
                    transition_function['q'+str(i)] = {symbol:U}
                    new_trasition.append(State(i,state,{symbol:U}))
             
        i+=1
        exit = len(states_unmarked)
    
   

    for i in range(len(new_trasition)):
        for key in new_trasition[i].transition:
            new_trasition[i].transition[key] = states.index(new_trasition[i].transition[key])
                

    for value in transition_function:
        for x in transition_function[value]:  
            transition_function[value][x]='q'+str(states.index(transition_function[value][x]))

  


    mini = minimization(alphabet,states,new_trasition)
  
    return transition_function,mini



def minimization(alphabet,Q,new_trasition):
    tabela = []
    for i in range(len(Q)):
        tabela.append([0]*(len(Q)))
    final = []
    flag = True
    while(flag):
        flag = False
        for i in range(len(Q)):
            for j in range(len(Q)):
                if i>j:
                    if new_trasition[i].final:
                        final.append(i)
                        if not (new_trasition[j].final):
                            
                            if tabela[i][j] != 1:
                                tabela[i][j] = 1
                                flag = True
                    else:
                        if new_trasition[j].final:
                            final.append(j)
                            if tabela[i][j] != 1:
                                tabela[i][j] = 1
                                flag = True
                                    
                if i>j:
                
                    if i not in final and j not in final and tabela[i][j]==0:
                        for symbol in alphabet:
                            a = new_trasition[i].transition[symbol]
                          
                            b = new_trasition[j].transition[symbol]
                            
                            if tabela[a][b] == 1  or tabela[b][a] and tabela[i][j]!=1:
                                tabela[i][j] = 1
                                flag = True

    equivalent = []
    #print(tabela)         
    for i in range(len(tabela)):
        for j in range(len(tabela)):
            if i>j:
                if tabela[i][j]==0:
                    #del transition_function[str(i)]
                    equivalent.append({i,j})
                    new_trasition[j].equivalent.append(i)
                    
                      
    if len(equivalent)>0:               #new_trasition.pop(i)   
        aux = equivalent[0]
        for i in range(len(equivalent)-1):
            for j in range(i,len(equivalent)):
                if not aux.isdisjoint(equivalent[j]):
                    aux= aux.union(equivalent[j])
        final_equivalent = [aux]
        for i in range(len(equivalent)):
            if not equivalent[i].issubset(aux):
                final_equivalent.append(equivalent[i])        
    
        return get_minimized_transition_function(new_trasition,final_equivalent)
    
    else:
        return make_table(new_trasition)
                    


     
                        
                                            
                            



# (if)+(for)+((f+o+r+i+f)(f+o+r+i+f)*)

    

def get_minimized_transition_function(new_transition,final_equivalent):
    table = {}
    
 
    
    
    for i in range(len(new_transition)):
        for value in new_transition[i].transition:
            for equivalent_set in final_equivalent:
                if new_transition[i].transition[value] in equivalent_set:
                    new_transition[i].transition[value] = min(equivalent_set)
                    
    for equivalent_set in final_equivalent:
        aux = list(equivalent_set)[1:]
        for index in sorted(aux, reverse=True):
            del new_transition[index]
                
    return make_table(new_transition)
    
    
    
def make_table(transition_function):
    table = {}
    for i in range(len(transition_function)):
        if i == 0:
            if transition_function[i].final:
                table['->*q0'] = transition_function[i].transition
            else:
                table['->q0'] = transition_function[i].transition
        else:
            if transition_function[i].final:
                table['*q'+str(i)] = transition_function[i].transition
            else:
                table['q'+str(i)] = transition_function[i].transition
                
    for key in table:
        for symbol in table[key]:
            table[key][symbol]='q'+str(table[key][symbol])
    
    return table