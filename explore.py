from pryo import *

k = KBMan()
q = k.query

k.age('John', 18)
k.age('Alice', 22)
k.age('Lucas', 25)

k.address('John', 'Morgan street.', 25)
k.address('Alice', 'Titja street.', 88)
k.address('Lucas', 'Morgan street.', 2)

# Schema?
# from collections import namedtuple
# Person = namedtuple('Person', 'name age address house_number')
# k += Person(name='John', age=19, address='Morgan street.', house_number=25)
k.person('John', 18, 'Morgan street.', 25)
k.person('Alice', 22, 'Titja street.', 88)
k.person('Lucas', 25, 'Morgan street.', 2)

# q : q.age(var.x, var.y) & Assert(Func(op.gt, var.y, 21))

kb = k._kb

from pprint import pprint
pprint(kb)

import operator as op


print('=== Find all persons with age > 21 ===')
r = kb.ask(
    pred.age(var.X, var.Y) &
    Assert(Func(op.gt, var.Y, 21))
)
pprint(list(r))

r = kb.ask(
    pred.person(var.name, var.age, var.street, var.house_number) &
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
