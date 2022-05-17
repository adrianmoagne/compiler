class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class Symbol:
    
    def __init__(self, input):
        if input[0] == '\\':
           self.value = input[0:2]
           
        else:
            self.value = input[0]
             
    
    def read(self):
        if self.value in ['.', '*', '+']: 
            return Operator(self.value)
        
        if self.value in ['(', ')']:
            return Parenthesis(self.value)
        
        return Operand(self.value)

class Operator(Symbol):
    def __init__(self, input):
        super().__init__(input)
        

class Operand(Symbol):
    def __init__(self, input):
        super().__init__(input)
        
        
class Parenthesis(Symbol):
    def __init__(self, input):
        super().__init__(input)
        
class Node:
    def __init__(self,value) -> None:
        self.value = value
        self.left = None
        self.right = None
    