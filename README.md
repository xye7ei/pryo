pryo
=====

This is a experimental core implementation for native *Prolog*
functionalities in *Python* environment. It aims to allow
experimenting Prolog-style knowledge-base within Python without any
dependencies.

The implementation is based on instructions in
book [AIMA](http://aima.cs.berkeley.edu/) with simplest
*backward-chaining* algorithm for querying. `dict` (hash table) is
used for naive indexing.

### First View

The knowledge base can be simply declared as the following. `KBMan` -
the knowledge base manager is the namespace and basic object. The
*facts* are declared through indexing several terms, while *rules*
(*definite clauses*) declared by `=` notations, where right-hand-side
is a list of clauses:

``` python
from pryo import *

k = KBMan()

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
k.sibling[x, y] = [
    k.father(z, x),
    k.father(z, y),
    x != y
]


# Simple definition
k.parent[x, y] = k.father(x, y)
k.parent[x, y] = k.mother(x, y)

# Recursive rules
k.ancester[x, y] = k.father(x, y)
k.ancester[x, y] = [k.father(x, z), k.ancester(z, y)]

```

Given facts and rules, queries can be fired by calling attributes from `query` attribute of `KBMan`:

``` python
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
```

Rules simulating *pattern matching* functions are supported:

``` python
# Boundary case as fact to add
k.factorial[0, 1]               # let fatorial(0) == 1

# Recurive rule (can use list/tuple as RHS)
k.factorial[x, y] = [
    x >= 0,                     # let x >= 0
    k.factorial(x - 1, z),      # let z == factorial(x - 1)
    y == x * z                  # let y == x * z
]

# Query results
r = q.factorial(4, v.w)
print(list(r))
# [{$w: 24}]
```

Some user-defined structures are also no problem, for example the `Cons` structure (an instance of compound term `TermCnpd`) and the `append` predicate over such structure:

``` python
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
```


though more tricks for simplification are yet to be explored.


### TODO

+ Confering ideas from project [datomic](http://www.datomic.com/) - a *Datalog* system in *Clojure*
+ Figuring out relations between data *Record* and *Relations*
+ Ordering of query subexpressions?
