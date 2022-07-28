pryo
=====

This is an experimental implementation for *Prolog*
functionalities in *pure Python*. You can create a Prolog-style
*knowledge base* and run queries in it with pure Python.

The implementation is based on instructions in the
book [AIMA](http://aima.cs.berkeley.edu/), based on the most basic
*backward-chaining* query algorithm.

# Usage

## Preparing knowledge base

A knowledge base object (ie. `KB`) stores a set of first-order logical
sentences and provides query interfaces. The proxy object
`KBMan` (knowledge base manager) is a manager object
wrapping a `KB` instance and offers simplified access patterns to the
content of `KB` (where `KB` is not exposed to the user directly).

Simply calling `KBMan()` creates a new knowledge base:

``` python
from pryo import KBMan

k = KBMan()
```

Given the KB manager instance, accessing an attribute (together with
*Term*s as arguments in brackets) declares a predicate. This syntactic
sugar is not super intuitive at first sight but simplifies code a lot.

More specifically,
- *Facts* are declared via indexing an attribute with a list of terms (where `__getitem__` wraps the logic of creating a fact behind the scene).
- *Rules* (*definite clauses*) are declared via `[]=` operation (where `__setitem__` contains the logic of creating a rule). The *left-hand-side* is a first-order conclusion clause and *right-hand-side* is a `list` of premise clauses.


``` python
# Facts
k.father['John', 'Lucy']
k.father['John', 'Lucas']
k.mother['Sarah', 'Lucy']
k.mother['Sarah', 'Lucas']
k.father['Gregor', 'John']

# Introduce schematic variables for first-order universal quantification
from pryo import scm
x, y, z, w = scm('xyzw')

# Declaring a rule
# - Using brackets for the LHS predicate, roughly meaning:
#   + "introduce a new indexed predicate"
# - Using parenthesis for each RHS predicate, roughly meaning:
#   + "call for unification"
k.sibling[x, y] = [
	k.father(z, x),
	k.father(z, y),
	x != y                      # overloaded not-equal on schematic vars
]


# Assignment means appending rule alternatives
k.parent[x, y] = k.father(x, y)
k.parent[x, y] = k.mother(x, y)

# Recursive rules are supported
k.ancester[x, y] = k.father(x, y)
k.ancester[x, y] = [k.father(x, z), k.ancester(z, y)]
```

We can inspect the knowledge-base status by accessing the attribute
`KBMan().kb`, which shows the registered facts and rules. Note the
RHS list of clauses has been converted into *conjunctive form* of clauses
under the hood.

``` python
pprint(k.kb)

# Output (The number means the arity, as in Prolog):
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
```


## Running Queries

Having prepared facts and rules, queries can be fired via calling
attributes from the proxy object `query`:

``` python
# The query proxy provided by `KBMan`
q = k.query

# Optionally using the Var object for queries
from pryo import Var

# Do a query with q, with two variable arguments and either variable can be
# - explicitly constructed, like: Var('name')
# - shorthand: a string starting with '$', like: '$name'
# Query results are returned in a generator
r = q.sibling(Var('who1'), '$who2') print(next(r))
# {$who2: 'Lucas', $who1: 'Lucy'}
print(next(r))
# {$who2: 'Lucy', $who1: 'Lucas'}
try:
	print(next(r))
except StopIteration:
	print('Query exhausted.')

# Variable name can be more self-descriptive.
# Here we query Lucy's parent, given "Lucy" as a constant to match
# the facts and rules:
r = q.parent("$lucy's parent", 'Lucy')
print(list(r))
# [{$lucy's parent: 'John'}, {$lucy's parent: 'Sarah'}]

# If both arguments are variables, all matching facts are returned
r = q.ancester('$ancester', '$decedant')
pprint(list(r))
# [{$ancester: 'John', $decedant: 'Lucy'},
#  {$ancester: 'John', $decedant: 'Lucas'},
#  {$ancester: 'Gregor', $decedant: 'John'},
#  {$ancester: 'Gregor', $decedant: 'Lucy'},
#  {$ancester: 'Gregor', $decedant: 'Lucas'}]
```

## Deductive Computation and Pattern Matching

Function call evaluation based on deductive processes are supported
also by the backward-chaining method. Hence it is possible to write
recursive functions.

While some commonly used operators are overriden for schematic
variables, we can write the `factorial` function like

``` python
# Boundary case as fact to add
k.factorial[0, 1]               # let fatorial(0) == 1

# Recurive rule (can use list/tuple as RHS)
# Note x >= 0 must be the first argument, otherwise the evaluation
# won't terminate due to eager expansion, similar to left recursion
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

Some user-defined structures are also supported, for example the
`Cons` structure (an instance of compound term `TermCnpd`) and the
`append` predicate as an operation on such a structure:

``` python
# Define the constructor for a compound data type
Cons = lambda car, cdr: TermCnpd('Cons', car, cdr)
NIL = None

xs, ys, zs = scm('xs ys zs'.split())

k.append[NIL, ys, ys]
k.append[Cons(x, xs), ys, Cons(x, zs)] = k.append(xs, ys, zs)
# The equation above is a shorthand for:
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


### TODO

+ Allow retracting registered facts/rules
+ Adopt ideas from project [datomic](http://www.datomic.com/) - a *Datalog* system in *Clojure*
+ Figure out relations between data *Record* and *Relations*
+ Ordering of query subexpressions (very non-trivial)
