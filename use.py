from pryo import KBMan, NotEq, scm, var, Assert, Func, Eq, TermCnpd
from pprint import pprint


k = KBMan()
q = k.query

k.father('opa', 'pap')
k.father('pap', 'a')
k.mother('mum', 'a')
k.father('pap', 'b')
k.mother('mum', 'b')

x, y, z, w = scm(4)

k.sibling(x, y) <= (
    k.father(z, x) &
    k.father(z, y) &
    NotEq(x, y)
)

k.ancester(x, y) <= k.father(x, y)
k.ancester(x, y) <= k.father(x, z) & k.ancester(z, y)

print(k._kb)

r = q.sibling(var.x, var.y)
print(list(r))

r = q.ancester(var.x, var.y)
print(list(r))

import operator as op
k.factorial(0, 1)
k.factorial(x, y) <= (
    Assert(Func(op.ge, x, 0)) &
    k.factorial(Func(op.sub, x, 1), z) &
    Eq(y, Func(op.mul, x, z))
)

r = q.factorial(4, var.w)
# r = q.factorial(4)
print(list(r))

# FIXME: what is indeed Relation? Term? Predicate?
# CONFER: datomic 5-tuple
# [<$> <entity-id> <attr-key> <attr-value> <transaction-id>]
# SELFDESCRIPTION?
# 
# 
# FIXME: How to use namedtuple?
Cons = lambda car, cdr: TermCnpd('Cons', car, cdr)
NIL = None

# from pypro import unify
# u = unify(Cons(1, Cons(2, NIL)), Cons(var.x, var.y))
# print((u))
# u = unify([1, 2, 3], [var.x, var.y, var.z])
# print((u))
# assert 0


# Is this a fact??
# k.append(NIL, scm.y, scm.y)
k.append(NIL, scm.y, scm.z) <= Eq(scm.y, scm.z)

# k.append(Cons(scm.x, scm.xs), scm.y, scm.z) <=\
#     k.append(scm.xs, scm.y, scm.zs) &\
#     Eq(scm.z, Cons(scm.x, scm.zs))

k.append(Cons(scm.x, scm.xs), scm.y, Cons(scm.x, scm.zs)) <=\
    k.append(scm.xs, scm.y, scm.zs)


r = q.append(NIL, Cons(3, NIL), var.z)
pprint(list(r))
r = q.append(Cons(1, NIL), Cons(3, NIL), var.z)
pprint(list(r))
r = q.append(Cons(1, Cons(2, NIL)), Cons(3, Cons(4, NIL)), var.z)
pprint(list(r))


# Named compound term?


