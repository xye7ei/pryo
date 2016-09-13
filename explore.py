from pryo import *

k = KBMan()
q = k.query

k.id<(123, 'John')
k.id<(456, 'Alice')
k.id<(789, 'Lucas')

k.age<(123, 18)
k.age<(456, 22)
k.age<(789, 25)

k.address<(123, 'Morgan street.', 25)
k.address<(456, 'Titja street.', 88)
k.address<(789, 'Morgan street.', 2)

# Schema?
# from collections import namedtuple
# Person = namedtuple('Person', 'name age address house_number')
# k += Person(name='John', age=19, address='Morgan street.', house_number=25)
k.person<(123, 'John', 18, 'Morgan street.', 25)
k.person<(456, 'Alice', 22, 'Titja street.', 88)
k.person<(789, 'Lucas', 25, 'Morgan street.', 2)


kb = k._kb

from pprint import pprint
pprint(kb)

import operator as op

print('=== Show persons with ages ===')
r = kb.ask(
    pred.id(var.id, var.name) &
    pred.age(var.id, var.age)
)
pprint(list(r))



print('=== Find all persons with age > 21 ===')
r = kb.ask(
    pred.age(var.X, var.Y) &
    Assert(Func(op.gt, var.Y, 21))
)
pprint(list(r))

r = kb.ask(
    pred.person(var.id, var.name, var.age, var.street, var.house_number) &
    Assert(Func(op.gt, var.age, 21))
)
pprint(list(r))


print('=== Find all persons with address street Morgan ===')
r = kb.ask(
    pred.address(var.name, var.street, var.number) &
    Assert(Func(op.contains, var.street, 'Morgan'))
)
pprint(list(r))


print('=== Group persons who live in the same street??? ===')

k.same_street(scm.p1, scm.p2) <= (
    k.id(scm.id1, scm.p1),
    k.id(scm.id2, scm.p2),
    k.address(scm.id1, scm.a1, scm.an1),
    k.address(scm.id2, scm.a2, scm.an2),
    scm.id1 != scm.id2,
    scm.a1 == scm.a2,
)

r = kb.ask(pred.same_street(var.x, var.y))
pprint(list(r))
