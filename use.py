from pryo import KB, P, scm, var

kb = KB()

kb.tell(P('father', 'pap', 'john'))
kb.tell(P('father', 'pap', 'lucas'))
kb.tell(P('father', 'unc', 'jacob'))


x, y, z = scm('xyz')

r = P('sibling', x, y) <= P('father', z, x) & P('father', z, y) & (x != y)

kb.tell(r)

from pprint import pprint
pprint(kb)
pprint(type(r))


res = kb.ask(P('sibling', var.x, var.y))

pprint(next(res))
pprint(next(res))
pprint(next(res))

from pryo import KB, P, scm, var

kb = KB()

kb.tell(P('father', 'pap', 'john'))
kb.tell(P('father', 'pap', 'lucas'))
kb.tell(P('father', 'unc', 'jacob'))


# x, y, z = scm('xyz')
# r = P('sibling', x, y) <= P('father', z, x) & P('father', z, y) & (x != y)
# kb.tell(r)
# from pprint import pprint
# pprint(kb)
# pprint(type(r))
# res = kb.ask(P('sibling', var.x, var.y))
# pprint(next(res))
# pprint(next(res))
# pprint(next(res))


# Add facts
kb.fact('father', 'opa', 'pap')
kb.fact('father', 'pap', 'a')
kb.fact('father', 'pap', 'b')

# Alterative way
kb.fact('mother', 'mum', ['a', 'b'])


# Schematic variables for First-Order rules
x, y, z, w = scm('xyzw')

# Definite clause
kb.rule(
    ('sibling', x, y),
    ('father', z, x) & ('father', z, y) & (x != y)
)

# Alternative clauses
kb.rule(
    ('parent', x, y), ('father', x, y))
kb.rule(
    ('parent', x, y), ('mother', x, y))

# Recursive rules
kb.rule(
    ('ancester', x, y), ('father', x, y))
kb.rule(
    ('ancester', x, y), ('father', x, z) & ('ancester', z, y))


kb.ask(P('sibling', var.x, var.y))


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


from pprint import pprint

import operator as op
from operator import ge, sub, mul

# Boundary case as fact to add
k.factorial < (0, 1)            # fatorial[0] == 1

# Recurive rule
k.factorial(x, y) <= (
    x >= 0,                     # x >= 0
    k.factorial(x - 1, z),      # z == factorial(x - 1)
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


# ??????????????????
NIL = 'NIL'

k.append < (NIL, y, y)
k.append(Cons(x, xs), y, Cons(x, zs)) <= k.append(xs, y, zs)

# # Short for:
# k.append(Cons(scm.x, scm.xs), scm.y, scm.z) <=\
#     k.append(scm.xs, scm.y, scm.zs) &\
#     (scm.z == Cons(scm.x, scm.zs))

# pprint(k._kb)

r = q.append(NIL, Cons(3, NIL), v.z)
pprint(list(r))
r = q.append(Cons(1, NIL), Cons(3, NIL), v.z)
pprint(list(r))
r = q.append(Cons(1, Cons(2, NIL)), Cons(3, Cons(4, NIL)), v.z)
pprint(list(r))


# Named compound term?

