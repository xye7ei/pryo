pyro
=====

This is a experimental core implementation for native *Prolog* functionalities in *Python* environment. It aims to allow experimenting Prolog-style knowledge-base within Python without any dependencies.

The implementation is based on instructions in book [AIMA](http://aima.cs.berkeley.edu/) with simplest *backward-chaining* algorithm for querying. `dict` (hash table) is used for naive indexing.

### First View

The knowledge base can be simply declared as the following. `KBMan` - the knowledge base manager is the namespace and basic object. The *facts* are simply declared by *calling* attributes and *rules* (*definite clauses*) declared by `<=` notations:

``` python
import pryo as po

k = po.KBMan()

# Add facts
+k.father['opa', 'pap']
+k.father['pap', 'a']
+k.mother['mum', 'a']
+k.father['pap', 'b']
+k.mother['mum', 'b']

# Schematic variables for First-Order rules
x, y, z, w = po.scm('xyzw')

# Definite clause
k.sibling[x, y] <= (
    k.father[z, x] &
    k.father[z, y] &
    (x != y)
)

# Alternative clauses
k.parent[x, y] <= k.father[x, y]
k.parent[x, y] <= k.mother[x, y]

# Recursive rules
k.ancester[x, y] <= k.father[x, y]
k.ancester[x, y] <= k.father[x, z] & k.ancester[z, y]
```

Given facts/rules, queries can be fired by calling attributes from `query` attribute of `KBMan`:

``` python
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
```

Rules simulating *pattern matching* functions are supported:

``` python
# Boundary case as fact to add
+k.factorial[0, 1]              # fatorial[0] == 1

# Recurive rule
k.factorial[x, y] <= (
    (x >= 0) &                  # x >= 0
    k.factorial[x - 1, z] &     # z == factorial[x - 1]
    (y == x * z)                # y == x * z
)

# Query results
r = q.factorial(4, v.w)
print(list(r))
# [{$w: 24}]
```

In summary, several features are interesting here:

+ Non-literal specification of predicates/terms. For example
+ Querying with `And` (conjunctive) predicates;
+ Function application object `Func`;

though more tricks for simplification are yet to be explored.


### TODO

+ Confering ideas from project [datomic](http://www.datomic.com/) - a *Datalog* system in *Clojure*
+ Figuring out relations between data *Record* and *Relations*
+ Ordering of query subexpressions?
