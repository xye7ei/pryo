pryo
=====

This is a experimental core implementation for native *Prolog* functionalities in *Python* environment. It aims to allow experimenting Prolog-style knowledge-base within Python without any dependencies.

The implementation is based on instructions in book [AIMA](http://aima.cs.berkeley.edu/) with simplest *backward-chaining* algorithm for querying. `dict` (hash table) is used for naive indexing.

### First View

The knowledge base can be simply declared as the following. `KBMan` - the knowledge base manager is the namespace and basic object. The *facts* are simply declared by pushing n-ary tuple with `<` into a fact symbol and *rules* (*definite clauses*) declared by `<=` notations:

``` python
import pryo as pr

k = pr.KBMan()

# Add facts
k.father < ('opa', 'pap')
k.father < ('pap', 'a')
k.father < ('pap', 'b')

# Alterative way pushing a list of facts
k.mother << [
    ('mum', 'a'),
    ('mum', 'b')
]

# Schematic variables for First-Order rules
x, y, z, w = pr.scm('xyzw')

# Definite clause
k.sibling(x, y) <= (
    k.father(z, x),
    k.father(z, y),
    x != y,
)

# Alternative clauses
k.parent(x, y) <= k.father(x, y)
k.parent(x, y) <= k.mother(x, y)

# Recursive rules
k.ancester(x, y) <= k.father(x, y)
k.ancester(x, y) <= (
    k.father(x, z),
    k.ancester(z, y)
)

```

Given facts and rules, queries can be fired by calling attributes from `query` attribute of `KBMan`:

``` python
# Instant variable for queries
v = pr.var
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

```

Rules simulating *pattern matching* functions are supported:

``` python
# Boundary case as fact to add
k.factorial < (0, 1)            # fatorial[0] == 1

# Recurive rule
k.factorial(x, y) <= (
    x > 0,                      # x > 0
    k.factorial(x - 1, z),      # z == factorial(x - 1)
    y == x * z                  # y == x * z
)

# Query results
r = q.factorial(4, v.w)
print(list(r))
# [{$w: 24}]
```

Some user-defined or pre-defined structures are also no problem, for example the `Cons` structure and the `append` predicate over such structure:
``` python
# Declare literal data type
Cons = lambda car, cdr: TermCnpd('Cons', car, cdr)
NIL = None

# Declare predicate
xs, ys, zs = scm('xs ys zs'.split())

k.append < (NIL, y, y)

k.append(Cons(x, xs), y, Cons(x, zs)) <= k.append(xs, y, zs)

r = q.append(NIL, Cons(3, NIL), v.z)
print(list(r))
# [{$z: Cons(3, None)}]

r = q.append(Cons(1, NIL), Cons(3, NIL), v.z)
print(list(r))
# [{$z: Cons(1, Cons(3, None))}]
```


In summary, several features are interesting here:

+ Non-literal specification of predicates/terms.
+ Function application object `Func`;

though more tricks for simplification are yet to be explored.


### TODO

+ Confering ideas from project [datomic](http://www.datomic.com/) - a *Datalog* system in *Clojure*
+ Figuring out relations between data *Record* and *Relations*
+ Ordering of query subexpressions?
