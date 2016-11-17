from pryo import *

k = KBMan()

# Schema?
# from collections import namedtuple
# Person = namedtuple('Person', 'name age address house_number')
# k += Person(name='John', age=19, address='Morgan street.', house_number=25)
k.person<(123, 'John', 18, 'Morgan street.', 25)
k.person<(124, 'Jonathan', 18, 'Morgan street.', 21)
k.person<(225, 'Alice', 22, 'Titja street.', 88)
k.person<(336, 'Lucas', 25, 'Morgan street.', 2)
k.person<(487, 'Fury', 25, 'Titja street.', 30)
k.person<(998, 'Furios', 25, 'Titja street.', 28)

# q : q.age(var.x, var.y) & Assert(Func(op.gt, var.y, 21))

s = scm
f = Func
ap = Applier(globals)

k.neighbor(s.name1, s.name2) <= (
    # binding
    k.person(s.id1, s.name1, s.age1, s.street1, s.num1),
    k.person(s.id2, s.name2, s.age2, s.street2, s.num2),
    # qualification
    s.id1 != s.id2,
    s.street1 == s.street2,
    # Le(ap(abs, s.num1 - s.num2), 5),
    # f(abs, s.num1 - s.num2) <= 5,
    # ap.abs(s.num1 - s.num2) <= 5,
    abs@(s.num1 - s.num2) <= 5,
    # f.abs(s.num1 - s.num2) <= 5,
)


r = k.query.neighbor(var.n1, var.n2)
from pprint import pprint
pprint(list(r))


print(Le(Func(abs, s.num1 - s.num2), 5))
print(Func(abs, s.num1 - s.num2) <= 5)
