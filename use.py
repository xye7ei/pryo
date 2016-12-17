from pryo import KBMan, scm
from pprint import pprint

k = KBMan()

# Parenthesis(__call__) means adding to KB.
k.father['John', 'Lucy']
k.father['John', 'Lucas']
k.mother['Sarah', 'Lucy']
k.mother['Sarah', 'Lucas']
k.father['Gregor', 'John']

# Schematic variables for first-order qualification
x, y, z, w = scm('xyzw')

# Declaring a rule
# - Use brackets for the LHS predicate, roughly meaning:
#   + "making a new indexed predicate"
# - Use parenthesis for each RHS predicate, roughly meaning:
#   + "using the indexed predicate"
#   + "calling for unification"
k.sibling[x, y] = [
    k.father(z, x),
    k.father(z, y),
    x != y                      # overloaded operation on schematic variables
]

# Definition for alternatives
k.parent[x, y] = k.father(x, y)
k.parent[x, y] = k.mother(x, y)

# Recursive rules
k.ancester[x, y] = k.father(x, y)
k.ancester[x, y] = [k.father(x, z), k.ancester(z, y)]

# Can inspect the knowledge-base status
pprint(k.kb)
# [father/2['John', 'Lucy'],
#  father/2['John', 'Lucas'],
#  father/2['Gregor', 'John'],
#  mother/2['Sarah', 'Lucy'],
#  mother/2['Sarah', 'Lucas'],
#  (sibling/2[x, y] :- father/2[z, x] & father/2[z, y] & (x != y).),
#  (parent/2[x, y] :- father/2[x, y].),
#  (parent/2[x, y] :- mother/2[x, y].),
#  (ancester/2[x, y] :- father/2[x, y].),
#  (ancester/2[x, y] :- father/2[x, z] & ancester/2[z, y].)]

# The query proxy
q = k.query

# Variable for queries
from pryo import Var

# Do a query with q, with two variable arguments, each variable can be
# - explicitly constructed: Var('name')
# - a string starts with '$': '$name'
r = q.sibling(Var('who1'), '$who2')
print(next(r))
# {$who2: 'Lucas', $who1: 'Lucy'}
print(next(r))
# {$who2: 'Lucy', $who1: 'Lucas'}
try:
    print(next(r))
except StopIteration:
    print('Query exhausted.')

r = q.parent("$lucy's parent", 'Lucy')
print(list(r))
# [{$lucy's parent: 'John'}, {$lucy's parent: 'Sarah'}]


# Query a variable relevant to a constant 'Lucy'
res = q.ancester('$ancester', '$decedant')
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
    x >= 0,                     # let x >= 0, otherwise non-termination while exhausting
    k.factorial(x - 1, z),      # let z == factorial(x - 1)
    y == x * z                  # let y == x * z
]

# Query results
r = q.factorial(4, '$w')
print(list(r))
# [{$w: 24}]


from pryo import TermCnpd

# Declare compound data type
Cons = lambda car, cdr: TermCnpd('Cons', car, cdr)
NIL = None

xs, ys, zs = scm('xs ys zs'.split())

k.append[NIL, ys, ys]
k.append[Cons(x, xs), ys, Cons(x, zs)] = k.append(xs, ys, zs)
# This tricky equation above is short for:
# k.append[Cons(x, xs), ys, zs] <= [
#     k.append(xs, ys, zs),
#     zs == Cons(x, zs)
# ]


r = q.append(NIL, Cons(3, NIL), '$vs')
pprint(list(r))
# [{$vs: Cons(3, 'NIL')}]

r = q.append(Cons(1, NIL), Cons(3, NIL), '$vs')
pprint(list(r))
# [{$vs: Cons(1, Cons(3, 'NIL'))}]

r = q.append(Cons(1, Cons(2, NIL)), Cons(3, Cons(4, NIL)), '$vs')
pprint(list(r))
# [{$vs: Cons(1, Cons(2, Cons(3, Cons(4, 'NIL'))))}]
