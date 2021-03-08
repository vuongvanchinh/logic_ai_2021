from models import Or, And, Deduce, Expression, Equivalent

NULL_EXPRESSION = Expression("NULL")

def resolutions_util(g):
    """
        
        tra ve ket qua phan giai va vi tri hai toans hang neu ton tai cap co the phan giai
        tra ve None neu khong phan giai duoc nua
    """
    l = len(g)
    for i in range(l - 1):
        for j in range(i+ 1, l):
            t = g[i].resolution(g[j])
            if t != None:
                return t, i, j
    return None # khong phan giai duoc nua

def standard(g = []):
    i = 0
    while i < len(g):
        if not g[i].isStandard():
            t = g[i].standard()
            g.remove(g[i])
            g.extend(t)
        else:
            i += 1
    return g
            
def show(g, text= ""):
    print(text, end = "")
    for x in g:
        print(x, end=" ")
    print(" ")
    

def ronbinson(g , h = None):
    """
    input: + g = cac cong thuc
           + h = ket luan
    output:
        True: neu tu g co the suy ra h
        False: neu tu g khong suy ra dc h
    """
    g.append(h.negate())
    t = None
    t2= None

    show(g, "G sau khi them phu h: ")
    g = standard(g)
    show(g, "G after standard: ")

    while len(g) != 0:
        t = resolutions_util(g)
        if t == None:# khong phan giai duoc nua
            print("Khong phan giai duoc nua")
            show(g, "G: sau khi khong phan giai duoc nua:")
            break
        
        show(t, "Ket qua phan giai: ")
        if t[0] == NULL_EXPRESSION:
            print("Phan giai ra cau NULL:")
            # print("Hai Expression do la:", g[t[1]], " va ", g[t[2]])
            # t2 = g[t[2]]
            # g.remove(g[t[1]])
            # g.remove(t2)
            # show(g, "G khi co null")
            #
            return True

        t2 = g[t[2]]
        g.remove(g[t[1]])
        g.remove(t2)
        g.append(t[0])
        show(g, "G sau khi them ket qua phan giai: ")
    
    show(g)

    return False

def factory(a, b, operator):
    if a == b: return a

    if operator == '+':
        return Or(b, a)
    elif operator == '*':
        return And(b ,a)
    elif operator == '>':
        return Deduce(b, a)
    elif operator == '_':
        return Equivalent(b, a)

def parse(s):
    """
    Tra ve 1 bieu thuc:
    '+' = or, '*' = and, '>' = =>, '_' = '<=>'
    """
    operator = []
    o = 0
    operand = []
    for i in range(len(s)):
        if s[i] == '(':
            o += 1
        elif s[i] == ')':
            if o == 0:
                raise Exception("Invalid syntax")
            o -= 1
            if len(operator) == 0:
                break
            t = operator.pop()
            if t == '-':
                operand.append(operand.pop().negate())
            else:
                operand.append(factory(operand.pop(), operand.pop(), t))
        elif s[i] in ('+', '-', '*', '>', '_'):
            operator.append(s[i])
        elif s[i] != ' ':# A, B, C
            operand.append(Expression(s[i]))
    
    if o != 0 or len(operand) != 1:
        raise Exception("Invalid Expession: ")
    return operand.pop()

