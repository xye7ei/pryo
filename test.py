from pryo import *

if __name__ == '__main__':
    
    kb = KB()

    # Pred(str:<verb>, str:<Const>, str:<Const>)
    # kb.tell(pred.father('pap', 'a'))
    # kb.tell(father=[])

    kb.tell(Pred('father', 'pap', 'a'))
    kb.tell(Pred('father', 'pap', 'b'))
    kb.tell(Pred('mother', 'mum', 'a'))
    kb.tell(Pred.new.mother('mum', 'b'))
    kb.tell(pred.father('opa', 'pap'))
    kb.tell(Pred.new.father('opa', 'ucl'))
    kb.tell(pred.mother('oma', 'pap'))
    kb.tell(Pred('sibling', ScmVar('x'), ScmVar('y'))
            <=
            Pred('father', ScmVar('z'), ScmVar('x')) &
            Pred('father', ScmVar('z'), ScmVar('y')) &
            NotEq(ScmVar('x'), ScmVar('y'))
    )

    print(kb)

    # kb.father('pap', 'a')
    # kb.mother('mum', 'a')
    # kb.sibling(1, 2) <= kb.father(3, 1) & kb.father(3, 2) & (1 != 2)
    # with scm(3) as (X, Y, Z):
    #     kb.sibling(X, Y) <= kb.father(Z, X) & kb.father(Z, Y) & (X != Y)
    # # kb.sibling(1, 2) <= kb.father(3, 1) & kb.father(3, 2) & (1 != 2)

    kb.tell(
        pred.ancester(scm.x, scm.y)
        <=
        pred.father(scm.x, scm.y)
    )
    # kb.tell(
    #     Pred('ancester', ScmVar('x'), ScmVar('y'))
    #     <=
    #     Pred('father', ScmVar('x'), ScmVar('y'))
    # )
    kb.tell(
        Pred('ancester', scm.x, scm.y)
        <=
        Pred('father', scm.x, scm.z) &
        Pred('ancester', scm.z, scm.y)
    )

    from pprint import pprint
    # pprint(kb)

    # print('========== father ==========')
    q = kb.ask(Pred('father', var.x, var.y))
    lq = list(q)
    # pprint(lq)
    assert {var.x: 'pap', var.y: 'a'} in lq
    assert {var.x: 'pap', var.y: 'b'} in lq
    assert {var.x: 'opa', var.y: 'pap'} in lq

    # print('========== sibling ==========')
    q = kb.ask(Pred('sibling', Var('x'), Var('y')))
    lq = list(q)
    # pprint(lq)
    assert {var.x: 'a', var.y: 'b'} in lq
    assert {var.x: 'b', var.y: 'a'} in lq
    assert {var.x: 'pap', var.y: 'ucl'} in lq
    assert {var.x: 'ucl', var.y: 'pap'} in lq

    # print('========== ancester ==========')
    q = kb.ask(Pred('ancester', var.U, var.V))
    lq = list(q)
    # pprint(lq)
    assert {var.U: 'opa', var.V: 'a'} in lq
    assert {var.U: 'opa', var.V: 'b'} in lq
    assert {var.U: 'opa', var.V: 'ucl'} in lq

    # print('========== factorial ==========')
    # q = kb.ask(Pred('factorial', 0, var.W))
    import operator as op

    kb.tell(
        Pred('factorial', 0, 1)
    )
    kb.tell(
        Pred('factorial', scm.x, scm.y)
        <=
        AssertFunc(op.gt, scm.x, -1) &
        Pred('factorial', Func(op.sub, scm.x, 1), scm.y1) &
        Eq(scm.y, Func(op.mul, scm.x, scm.y1))
    )
    # Dead loop when asking for more than one answer...
    # Since it is not ruled out that (scm.x > -1)
    # Eq(True, Func(...)) can do the trick

    q = kb.ask(Pred('factorial', 2, var.W))
    lq = list(q)
    # pprint(lq)
    assert {var.W: 2} in lq
    q = kb.ask(Pred('factorial', 5, var.W))
    lq = list(q)
    # pprint(lq)
    assert {var.W: 120} in lq


    # print('========== more tinies ==========')
    kb.tell(pred.gt5(scm.x) <= Assert(Func(op.gt, scm.x, 5)))
    q = kb.ask(pred.gt5(8))
    lq = list(q)
    # pprint(lq)
    # Non-empty list means query gets answered with "YES".
    # Dedicated unifier in this list is naturally empty. 
    assert lq
    q = kb.ask(pred.gt5(4))
    lq = list(q)
    # pprint(lq)
    # Empty list means query was answered "No".
    assert not lq

