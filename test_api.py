from models import Or, Expression, And, Deduce
from robinson import parse, ronbinson, show


def robinson_extend(gt, kl):
    gt = map(lambda x: x.strip(), gt.split(','))
    g = [parse(x) for x in gt]
    h = parse(kl)
    show(g, "G after parse: ")
    print("h after parse: ", h)
    return ronbinson(g, h)


if __name__ == "__main__":    
    g = "(A>B), (B>C), (A*D)"
    h = "(C*D)"
    rs = robinson_extend(g, h)
    print(rs)

# a = Expression('A')
# b = Expression('B')
# a_or_b = Or(a, b)
# c = Expression('C')
# ab = And(a, b)
# t = ab.standard() #t = A, B
# t = Or(ab, c) # t = (C or A), (C or B)

# print(a_or_b.resolution(Or(a.negate(),c)))# (B or C)
# print(ab.resolution(b.negate())) # None


# print(a.isStandard()) # True
# print(a_or_b.isStandard()) # True
# print(ab.isStandard())# False

# print(a) # A
# print(a.negate()) #-A
# a_or_b = Or(a, b)
# print(a_or_b)  #(A or B)
# print(a_or_b.negate()) #(-A and -B)

# notd = Expression("D", False)
# nota_or_b= Or(a.negate(), b)
# b_a = Deduce(b, a)
# #-a or b -b or a
