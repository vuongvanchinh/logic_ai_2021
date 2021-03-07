from models import Expression, And, Or, Deduce, Equivalent
from robinson import ronbinson, parse
from collections import namedtuple

a = Expression("A")
b = Expression("B")
c = Expression("C")
d = Expression("D")
e = Expression("E")
p = Expression("P")
q = Expression("Q")
r = Expression("R")
s = Expression("S")
u = Expression("U")

notPorQ = Or(p.negate(), q) # -p or q
notQorR = Or(q.negate(), r) #-q or p
notRorS = Or(r.negate(), s) #-r or s
notUornotS = Or(u.negate(), s.negate()) #-u or - s

p_q = Deduce(p, q) # p => q
q_r = Deduce(q, r) # q => r
r_s = Deduce(r, s) # r => s
c_d = Deduce(c ,d)

pq = And(q, p) # q and q
bc = And(c, b) # c and b
cd = And(c, d) # c and d
de = And(d, e)
ab = And(a, b)
avcb = Or(cd, bc) # (c or d) and (c or d)
rvns = Or(r, s.negate())
a_e_b = Equivalent(a, b)
b_e_c = Equivalent(b, c)

Test = namedtuple("Test", "g,h")

#g = (-P or Q) (-Q or R) (-R or S) (-U or -S) ||| h = (-P or -U) expected = True
test1 = Test( [notPorQ, notQorR, notRorS, notUornotS], Or(p.negate(), u.negate()))

#g = (P => Q) (Q => R) (R => S) (Q and P)  ||| h = (S or U) expected: True
test2 = Test([p_q,q_r ,r_s, pq], Or(s, u))

#g = (P => Q), -(-R or -S), h = (S and -Q) expect: False
test3 = Test([p_q, rvns.negate()], And(s, q.negate())) 

# g = (a and b) => c, (b and c) => d, h= (a and d) => d, expect: True 
test4 = Test([Deduce(ab, c),Deduce(bc, d)], Deduce(ab, d))

# g = (A => B), (B => C), (C => D), C ||| h = D or (A and B) expect: True 
test5 = Test([Deduce(a, b), Deduce(b, c), Deduce(c, d), c], Or(d, ab))
#
# test6 = Test([a_e_b, b_e_c, b], And(a, c))
expression = "(A+B)>(C*D)"
expression = f'({expression})' # meansure expression is wrapped

if __name__ == "__main__":    
    rs = ronbinson(test4.g, test4.h)
    print(rs)
    express = parse(expression)
    print(express)


