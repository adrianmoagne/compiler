def explicitar(expression):
    caracteres = list(expression)
    print(caracteres)
    i=0
    while i<=(len(caracteres)-2):
        print('i: ',i)
        if caracteres[i].isalpha() and (caracteres[i+1].isalpha() or caracteres[i+1]=='\\'):
            caracteres.insert(i+1,'.')
            print('1')
        elif caracteres[i] == '\\':
            print('2')
            if i+2 == len(caracteres):
                pass
            elif caracteres[i+1] == '\\':
                caracteres.insert(i+2,'.')
            elif caracteres[i-1] == '\\':
                pass
        
        elif (caracteres[i-1]=='\\' and caracteres[i]!='\\' ):
            print('3')
            if len(caracteres) > i+2:
                if(caracteres[i+2] !='\\' and caracteres[i-2]!='\\'):
                    caracteres.insert(i+1,'.')
            else:
                caracteres.insert(i+1,'.')
                
            
        elif caracteres[i]==')' and caracteres[i+1]=='(':
            print('4')
            caracteres.insert(i+1,'.')
            
        elif caracteres[i].isalpha() and caracteres[i+1]=='(':
            print('5')
            caracteres.insert(i+1,'.')
            
        elif caracteres[i]==')' and caracteres[i+1].isalpha():
            print('6')
            caracteres.insert(i+1,'.')
        
        elif caracteres[i]=='*' and caracteres[i+1].isalpha():
            print('7')
            caracteres.insert(i+1,'.')
        
        elif caracteres[i].isascii() and caracteres[i] not in ['*','.','+']:
            print('8')
            caracteres.insert(i+1,'.')
            
        i+=1
        print(caracteres)
    return ''.join(caracteres)

x = explicitar(input())
print(repr(x))
print(x)