pryo
=====

This is a experimental core implementation for *Prolog*
functionalities in *Python* environment. It aims to allow
experimenting Prolog-style *knowledge base* utilities within native
Python language environment.

The implementation is based on instructions in
book [AIMA](http://aima.cs.berkeley.edu/) with the most basic
*backward-chaining* query algorithm.

# Preparing a knowledge base

The knowledge base object `KB` stores a set of first-order logical
sentences and provides query interfaces. Further, the proxy object
`KBMan` (knowledge base manager) is a namespace and manager wrapping a
`KB` instance for simple accessing `KB`'s contents, where `KB` is no
more exposed to the user directly.

Simply calling `KBMan()` makes a new knowledge base:

``` python
from pryo import KBMan

k = KBMan()
```

Having the KB manager instance, any predicate can be declared through
accessing attribute (whose name is the name of the predicate and maybe
initialized by the first accessing), with several *Term*s as arguments
in brackets.

More specifically, *Facts* are declared through indexing several terms
(i.e. by calling overriden `__getitem__`). *Rules* (*definite
clauses*) are declared by `[]=` operation (i.e. calling overriden
`__setitem__`), where *left-hand-side* is a first-order conclusion
clause and *right-hand-side* is a `list` of premise clauses.


``` python
# Facts
k.father['John', 'Lucy']
k.father['John', 'Lucas']
k.mother['Sarah', 'Lucy']
k.mother['Sarah', 'Lucas']
k.father['Gregor', 'John']

# Schematic variables for first-order universal quantification
from pryo import scm

x, y, z, w = scm('xyzw')

# Declaring a rule
# - Using brackets for the LHS predicate, roughly meaning:
#   + "making a new indexed predicate"
# - Using parenthesis for each RHS predicate, roughly meaning:
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

We can inspect the knowledge-base status by accessing the attribute
`KBMan().kb`, which shows up the registered facts and rules. Note the
RHS list of clauses when declaring a rule has been converted into
underlying *conjunctive form* of clauses.

``` python
pprint(k.kb)

# Output:
[father/2['John', 'Lucy'],
 father/2['John', 'Lucas'],
 father/2['Gregor', 'John'],
 mother/2['Sarah', 'Lucy'],
 mother/2['Sarah', 'Lucas'],
 (sibling/2[x, y] :- father/2[z, x] & father/2[z, y] & (x != y).),
 (parent/2[x, y] :- father/2[x, y].),
 (parent/2[x, y] :- mother/2[x, y].),
 (ancester/2[x, y] :- father/2[x, y].),
 (ancester/2[x, y] :- father/2[x, z] & ancester/2[z, y].)]
```


# Doing queries

Having prepared facts and rules, queries can be fired by calling
attributes from the proxy `query`:

``` python
# The query proxy provides by `KBMan`
q = k.query

# Optionally using Var object for queries
from pryo import Var

# Do a query with q, with two variable arguments, each variable can be either
# - explicitly constructed: Var('name')
# - a string starting with '$': '$name'
r = q.sibling(Var('who1'), '$who2') print(next(r))
# Query results are iteratively generated
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

r = q.ancester('$ancester', '$decedant')
pprint(list(r))
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
