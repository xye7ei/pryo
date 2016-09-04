from pryo import scm, var, KBMan

k = KBMan()

k.father('John', 'Lucy')
k.father('Andreas', 'John')

k.ancester(scm.x, scm.y) <= k.father(scm.x, scm.y)
k.ancester(scm.x, scm.y) <= (
    k.father(scm.x, scm.z) &
    k.ancester(scm.z, scm.y)
)

q = k.query.ancester('X', 'Lucy')
q = k.query.ancester('X', 'Y')
# print(next(q))
# print(next(q))
# print(next(q))

print(list(q))
