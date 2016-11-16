from collections import namedtuple

class Pred(object):

    def __init__(self, *dat):
        self.dat = dat

    def __repr__(self):
        return 'P{}'.format(self.dat)

P = Pred

kb = [

    P('father', 'pap', 'a'),
    P('mother', 'mum', 'a'),
    P('father', 'pap', 'b'),

    # (sibling x y) :-
    #   (parent z x)
    #   (parent z y)

    # [x y]
    #   (sibling x y) :-
    #     [z]{
    #       (parent z x)
    #       (parent z y)
    #     }
    #     
    (P('sibling', '?x', '?y'),
     P('father', '?z', '?x'),
     P('father', '?z', '?y')),

    (P('parent', '?x', '?y'),
     [P('father', '?x', '?y'),
      P('mother', '?x', '?y')]),

    (P('ancester', '?x', '?y'),
     [P('parent', '?x', '?y'),
      (P('parent', '?x', '?z'),
       P('ancester', '?z', '?y'))]),
]


def is_symbol(x):
    return isinstance(x, str) and not x.startswith('?')

def is_scm_var(x):
    return isinstance(x, str) and x.startswith('?')

def is_var(x):
    return isinstance(x, str) and x.startswith('#')

def is_cmpd(x):
    return isinstance(x, (list, tuple))

def is_pred(x):
    return isinstance(x, Pred)

# from collections import Iterable


def univ_inst(expr, u={}, i=0):
    if is_scm_var(expr):
        if expr not in u:
            v = '$%d' % i
            return v, {**u, expr: v}, i+1
        else:
            return u[expr], u, i
    elif is_symbol(expr):
        return expr, u, i
    elif is_pred(expr):
        dat = []
        for d in expr.dat:
            expr1, u, i = univ_inst(d, u, i)
            dat.append(expr1)
        return Pred(*dat), u, i
    elif is_cmpd(expr):
        t = type(expr)
        subs = []
        for e in expr:
            e1, u, i = univ_inst(e, u, i)
            subs.append(e1)
        return t(subs), u, i

from pprint import pprint

p, u, i = univ_inst(kb[3], {}, 0)
pprint(p)

p, u, i = univ_inst(kb[-2], {}, 0)
pprint(p)

p, u, i = univ_inst(kb[-1], {}, 0)
pprint(p)
