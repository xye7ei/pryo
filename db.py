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

k.neighbor(scm.name1, scm.name2) <= (
    # binding
    k.person(scm.id1, scm.name1, scm.age1, scm.street1, scm.num1),
    k.person(scm.id2, scm.name2, scm.age2, scm.street2, scm.num2),
    # qualification
    scm.id1 != scm.id2,
    scm.street1 == scm.street2,
    Le(ap(abs, scm.num1 - scm.num2), 5),
)


r = k.query.neighbor(var.n1, var.n2)
from pprint import pprint
pprint(list(r))

