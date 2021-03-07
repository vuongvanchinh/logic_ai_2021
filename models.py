from functools import reduce
from copy import deepcopy

class Expression:
    
    def __init__(self, key='', value=True):
        self.key = key
        self.value = value
    
    def __str__(self):
        prefix = "" if self.value else '-'
        return f'{prefix + self.key}'#prefixf'({}'prefix + self.name

    def evaluate(self):
        return self.value
    
    def negate(self):
        return Expression(self.key, not self.value)


    def __eq__(self, o):
        if o.__class__ != Expression:
            return False
        return self.key == o.key and self.value == o.value

    def resolution(self, o):
        if o.__class__ == Expression and self.negate() == o:
            return Expression("NULL")

        if o.__class__ == Or:
            t = self.negate()
            if t in o.items:
                l = deepcopy(o.items)
                l.remove(t)
                
                if len(l) == 1:
                    return l[0]
                elif len(l) == 0:
                    return Expression("NULL")
                else:
                    return Or(*l)
        return None    
    def isStandard(self):
        return True

          
class ComplexExpression(Expression):
    def __init__(self, *args):
        self.items = args
    
    def standard(self):
        """ return a tuple of ..."""
        pass
    

class And(ComplexExpression):
    def __init__(self, *args):
        self.items = []
        for x in args:
            if x.__class__ == And:
                for k in x.items:
                    if k not in self.items:
                        self.items.append(k)        
            elif x not in self.items:
                self.items.append(x)

        if len(self.items) < 2:
            raise Exception("Or must have 2 or more unique arguments.")
        
    def evaluate(self):
        for x in self.items:
            if not x.evaluate():
                return False
        return True

    def negate(self):
        return Or(*list(map(lambda x: x.negate(), self.items)))
        
    def __str__(self):
        return '(' + ' and '.join(map(lambda x: x.__str__(), self.items)) + ')'
    
    def __eq__(self, o):
        if o.__class__ != And or len(self.items) != len(o.items):
            return False
        for x in self.items:
            if x not in o.items:
                return False
        return True
    
    def resolution(self, o):
        return None

    def isStandard(self):
        return False
    
    def standard(self):
        return tuple(self.items)
    
    
class Or(ComplexExpression):
    def __init__(self, *args):
        self.items = []
        for x in args:
            if x.__class__ == Or:
                for k in x.items:
                    if k not in self.items:
                        self.items.append(k)        
            elif x not in self.items:
                self.items.append(x)
        if len(self.items) < 2:
            raise Exception("Or must have 2 or more unique arguments.")

    def evaluate(self):
        for x in self.items:
            if x.evaluate():
                return True
        return False

    def negate(self):
        return And(*list(map(lambda x: x.negate(), self.items)))

    def __str__(self):
         return '('+' or '.join(map(lambda x: x.__str__(), self.items)) +')'
    
    def __eq__(self, o):
        if o.__class__ != Or or len(self.items) != len(o.items):
            return False
        for x in self.items:
            if x not in o.items:
                return False
        return True
    
    def isStandard(self):
            if len(self.items) == 1:
                return False

            for i in self.items:
                if not i.isStandard():
                    return False
            return True

    def standard(self):
        if len(self.items) == 1:
                return self.items[0]
        rs = []
        t = None
        for x in self.items:
            if not x.isStandard(): # chan chan say ra
                t = x
                self.items.remove(x)
                break

        st = t.standard()
        for x in st:
            try:
                o = Or(*self.items, x)
                rs.append(o)
            except:
                rs.append(x)
        self.items.append(t)
        return rs# chua triet de ngay
    
    def resolution(self, o):
        if o.__class__ == Expression:
            return o.resolution(self)

        elif o.__class__ == Or:
            
            l = deepcopy(self.items)
            s = deepcopy(o.items)
            for x in l:
                t = x.negate()
                if t in s:
                    l.remove(x)
                    s.remove(t)
                    k = len(l) + len(s)
                    if k == 1:
                        if len(s) == 1:
                            return s[0]
                        else: return l[0]
                    elif k == 0:
                        return Expression("NULL")
                    if(len(l) == len(s)== 1 and l[0].negate() == s[0]):
                        return None
                    return Or(*l, *s)                       
        return None

class  Deduce(ComplexExpression):
    """
    binary expression.
    """
    def __init__(self, *args):
        if len(args) != 2:
            raise Exception("Deduce only can have exactly two arguments.")
        self.items = args
        
    def evaluate(self):
        if self.items[0].evaluate() and not self.items[1].evaluate():
            return False
        return True
        
    def negate(self):
        #(a=>b) = -a or b = not (a => b) = a and -b
        return And(self.items[0], self.items[1].negate())

    def __str__(self):
        return f'({self.items[0]} => {self.items[1]})'
    
    def standard(self):# chi chuan hoa mot bac
        # a => b: -a or b
        #(a and b) or (c and d) = (c and d) or a, (c and d) or b 
        return (Or(self.items[0].negate(), self.items[1]),)
    
    def resolution(self, o):
        return None
    
    def __eq__(self, o):
        if o.__class__ != Deduce:
            return False
        return self.items[0] == o.items[0] and self.items[1] == o.items[1]
    
    def isStandard(self):
        return False


class Equivalent(ComplexExpression):

    """
    binary expression.
    """
    def __init__(self, *args):
        if len(args) != 2:
            raise Exception("Deduce only can have exactly two arguments.")
        self.items = args
        
    def evaluate(self):
        if self.items[0].evaluate() and not self.items[1].evaluate():
            return False
        if self.items[1].evaluate() and not self.items[0].evaluate():
            return False
        return True
        
    def negate(self):
        #a <=> b = a =>b and b => a
        #(a=>b) = -a or b => not (a => b) = a and -b
        #not (b => a) = b and -a 
        return (Or(And(self.items[0], self.items[1].negate()), And(self.items[1], self.items[0].negate())), )

    def __str__(self):
        return f'({self.items[0]} <=> {self.items[1]})'
    
    def standard(self):
        # a <=> b = (-a v b) and (-b v a) 
        return Or(self.items[0].negate(), self.items[1]), Or(self.items[1].negate(), self.items[0])
    
    def resolution(self, o):
        return None
    
    def __eq__(self, o):
        if o.__class__ != Equivalent:
            return False
        return self.items[0] == o.items[0] and self.items[1] == o.items[1]
    
    def isStandard(self):
        return False

