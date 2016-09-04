import pryo as po

k = po.KBMan()
q = k.query

k.father('opa', 'pap')
k.father('pap', 'a')
k.mother('mum', 'a')
k.father('pap', 'b')
k.mother('mum', 'b')

# Schematic variables for First-Order rules
x, y, z, w = po.scm(4)

# Definite clause
k.sibling(x, y) <= (
    k.father(z, x) &
    k.father(z, y) &
    po.NotEq(x, y)
)

# Alternative clauses
k.parent(x, y) <= k.father(x, y)
k.parent(x, y) <= k.mother(x, y)

# Recursive rules
k.ancester(x, y) <= k.father(x, y)
k.ancester(x, y) <= k.father(x, z) & k.ancester(z, y)

v = po.var

r = q.sibling(v.m, v.n)
print(list(r))

r = q.parent(v.p, 'b')
print(list(r))

r = q.ancester(v.x, 'b')
print(list(r))

from pprint import pprint

import operator as op
from operator import ge, sub, mul

AF = po.AssertFunc
F = po.Func

k.factorial(0, 1)                      # fatorial(0) == 1
k.factorial(x, y) <= (
    AF(ge, x, 0) &                     # x > 0
    k.factorial(F(sub, x, 1), z) &     # z == factorial(x - 1)
    po.Eq(y, F(mul, x, z))             # y == x * z
)

r = q.factorial(4, v.w)
print(list(r))
# r = q.factorial(4)
assert 0

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


