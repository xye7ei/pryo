import pryo as po

k = po.KBMan()

# Add facts
+k.father['opa', 'pap']
+k.father['pap', 'a']
+k.mother['mum', 'a']
+k.father['pap', 'b']
+k.mother['mum', 'b']

# Schematic variables for First-Order rules
x, y, z, w = po.scm(list('xyzw'))

# Definite clause
k.sibling[x, y] <= (
    k.father[z, x],
    k.father[z, y],
    x != y,
)

# Alternative clauses
k.parent[x, y] <= k.father[x, y]
k.parent[x, y] <= k.mother[x, y]

# Recursive rules
k.ancester[x, y] <= k.father[x, y]
k.ancester[x, y] <= k.father[x, z] & k.ancester[z, y]

# Instant variable for queries
v = po.var
q = k.query

r = q.sibling(v.m, v.n)
print(list(r))
# [{$m: 'a', $n: 'b'}, {$m: 'b', $n: 'a'}]

r = q.parent(v.p, 'b')
print(list(r))
# [{$p: 'pap'}, {$p: 'mum'}]

r = q.ancester(v.x, 'b')
print(list(r))
# [{$x: 'pap'}, {$x: 'opa'}]


from pprint import pprint

import operator as op
from operator import ge, sub, mul

# Boundary case as fact to add
+k.factorial[0, 1]              # fatorial[0] == 1

# Recurive rule
k.factorial[x, y] <= (
    x >= 0,                     # x >= 0
    k.factorial[x - 1, z],      # z == factorial[x - 1]
    y == x * z                  # y == x * z
)

# Query results
r = q.factorial(4, v.w)
print(list(r))
# [{$w: 24}]
# assert 0

# FIXME: what is indeed Relation? Term? Predicate?
# CONFER: datomic 5-tuple
# [<$> <entity-id> <attr-key> <attr-value> <transaction-id>]
# SELFDESCRIPTION?
# 
# 
# FIXME: How to use namedtuple?
from pryo import TermCnpd
Cons = lambda car, cdr: TermCnpd('Cons', car, cdr)
NIL = None

# from pypro import unify
# u = unify(Cons(1, Cons(2, NIL)), Cons(var.x, var.y))
# print((u))
# u = unify([1, 2, 3], [var.x, var.y, var.z])
# print((u))
# assert 0

from pryo import scm

xs, ys, zs = scm('xs ys zs'.split())

# Is this a fact??
+k.append[NIL, y, y]

k.append[Cons(x, xs), y, Cons(x, zs)] <=\
    k.append[xs, y, zs]

# # Short for:
# k.append(Cons(scm.x, scm.xs), scm.y, scm.z) <=\
#     k.append(scm.xs, scm.y, scm.zs) &\
#     (scm.z == Cons(scm.x, scm.zs))

# pprint(k._kb)

from pryo import var
r = q.append(NIL, Cons(3, NIL), var.z)
pprint(list(r))
r = q.append(Cons(1, NIL), Cons(3, NIL), var.z)
pprint(list(r))
r = q.append(Cons(1, Cons(2, NIL)), Cons(3, Cons(4, NIL)), var.z)
pprint(list(r))


# Named compound term?


