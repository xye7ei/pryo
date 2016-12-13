from pryo import *
from pprint import pprint

k = KBMan()

# Parenthesis(__call__) means adding to KB.
k.father['John', 'Lucy']
k.father['John', 'Lucas']
k.mother['Sarah', 'Lucy']
k.mother['Sarah', 'Lucas']
k.father['Gregor', 'John']


# Schematic variables for First-Order rules
x, y, z, w = scm('xyzw')

# Declaring a rule
# - Use brackets at LHS, roughly meaning:
#   + "making a new index"
# - Use parenthesis at RHS, roughly meaning:
#   + "using the indexed"
#   + "calling for unification"
k.sibling[x, y] = (
    k.father(z, x) &
    k.father(z, y) &
    (x != y)
)

q = k.query

res = q.sibling(var.x, var.y)
pprint(next(res))
pprint(next(res))
try:
    pprint(next(res))
except StopIteration:
    pass


# Simple definition
k.parent[x, y] = k.father(x, y)
k.parent[x, y] = k.mother(x, y)

# Recursive rules
k.ancester[x, y] = k.father(x, y)
k.ancester[x, y] = k.father(x, z) & k.ancester(z, y)



# Instant variable for queries
from pryo import Var
v = var

r = q.sibling(v.m, v.n)
print(list(r))
# [{$n: 'Lucas', $m: 'Lucy'}, {$n: 'Lucy', $m: 'Lucas'}]

r = q.parent(Var("lucy's parent"), 'Lucy')
print(list(r))
# [{$lucy's parent: 'John'}, {$lucy's parent: 'Sarah'}]

res = q.ancester(var.ancester, var.decedant)
pprint(list(res))
# [{$ancester: 'John', $decedant: 'Lucy'},
#  {$ancester: 'John', $decedant: 'Lucas'},
#  {$ancester: 'Gregor', $decedant: 'John'},
#  {$ancester: 'Gregor', $decedant: 'Lucy'},
#  {$ancester: 'Gregor', $decedant: 'Lucas'}]


import operator as op
from operator import ge, sub, mul

# Boundary case as fact to add
k.factorial[0, 1]               # fatorial(0) == 1

# Recurive rule (can use list/tuple as RHS)
k.factorial[x, y] = [
    x >= 0,                     # x >= 0
    k.factorial(x - 1, z),      # z == factorial(x - 1)
    y == x * z                  # y == x * z
]

# Query results
r = q.factorial(4, v.w)
print(list(r))
# [{$w: 24}]


from pryo import TermCnpd

# Declare literal data type
Cons = lambda car, cdr: TermCnpd('Cons', car, cdr)
NIL = None

# from pypro import unify
# u = unify(Cons(1, Cons(2, NIL)), Cons(var.x, var.y))
# print((u))
# u = unify([1, 2, 3], [var.x, var.y, var.z])
# print((u))
# assert 0

from pryo import scm

# Declare predicate
xs, ys, zs = scm('xs ys zs'.split())
NIL = 'NIL'

k.append[NIL, ys, ys]
k.append[Cons(x, xs), ys, Cons(x, zs)] = k.append(xs, ys, zs)

# Short for:
# k.append(Cons(x, xs), ys, z) <= [
#     k.append(xs, ys, zs),
#     z == Cons(x, zs)
# ]

# pprint(k._kb)

vs = v.vs

r = q.append(NIL, Cons(3, NIL), vs)
pprint(list(r))
# [{$vs: Cons(3, 'NIL')}]

r = q.append(Cons(1, NIL), Cons(3, NIL), vs)
pprint(list(r))
# [{$vs: Cons(1, Cons(3, 'NIL'))}]

r = q.append(Cons(1, Cons(2, NIL)), Cons(3, Cons(4, NIL)), vs)
pprint(list(r))
# [{$vs: Cons(1, Cons(2, Cons(3, Cons(4, 'NIL'))))}]



