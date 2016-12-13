pryo
=====

This is a experimental core implementation for native *Prolog*
functionalities in *Python* environment. It aims to allow
experimenting Prolog-style *knowledge base* utilities within native
Python.

The implementation is based on instructions in
book [AIMA](http://aima.cs.berkeley.edu/) with the most simple
*backward-chaining* query algorithm.

### First View

The knowledge base can be simply declared as the following. `KBMan` -
the knowledge base manager is the namespace and basic object for
simplicity of usage.

Any predicate is declared through accessing attribute (whose name is
exact the name of the predicate) of `KBMan` object, with several
*Term*s as indexing arguments.

More specifically, *Facts* are declared through indexing several terms
(calling overriden `__getitem__`). *Rules* (*definite clauses*) are
declared by `[]=` operation (calling overriden `__setitem__`), where
*left-hand-side* is a first-order conclusion predicate and
*right-hand-side* is a list of premise clauses.


``` python
from pryo import KBMan, scm

k = KBMan()

# Facts
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
    x != y                      # overloaded operation on schematic vars 
]


# Definition for alternatives
k.parent[x, y] = k.father(x, y)
k.parent[x, y] = k.mother(x, y)

# Recursive rules
k.ancester[x, y] = k.father(x, y)
k.ancester[x, y] = [k.father(x, z), k.ancester(z, y)]

```

Given facts and rules, queries can be fired by calling attributes from `query` attribute of `KBMan`:

``` python
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

# Query a variable relevant to a constant 'Lucy'
r = q.parent("$lucy's parent", 'Lucy')
print(list(r))
# [{$lucy's parent: 'John'}, {$lucy's parent: 'Sarah'}]

res = q.ancester('$ancester', '$decedant')
pprint(list(res))
# [{$ancester: 'John', $decedant: 'Lucy'},
#  {$ancester: 'John', $decedant: 'Lucas'},
#  {$ancester: 'Gregor', $decedant: 'John'},
#  {$ancester: 'Gregor', $decedant: 'Lucy'},
#  {$ancester: 'Gregor', $decedant: 'Lucas'}]
```

Some commonly used operators are overriden for schematic variables,
thus rules simulating *pattern matching* style functions are
here supported:

``` python
# Boundary case as fact to add
k.factorial[0, 1]               # let fatorial(0) == 1

# Recurive rule (can use list/tuple as RHS)
k.factorial[x, y] = [
    x >= 0,                     # let x >= 0, otherwise non-termination while exhausting
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
```


though more tricks for simplification are yet to be explored.


### TODO

+ Allow to retract registered facts/rules
+ Confering ideas from project [datomic](http://www.datomic.com/) - a *Datalog* system in *Clojure*
+ Figuring out relations between data *Record* and *Relations*
+ Ordering of query subexpressions (very non-trivial)
