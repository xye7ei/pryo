# Subgrammar for FOL-Sentence
#
# Sen      : SenAtom | SenCplx
# SenAtom  : Pred    | Pred Term* | Term == Term | Term != Term | Assert Term
# SenCplx  : AND Sen Sen
#          | Or  Sen Sen
#          | IMP Sen Sen
#          | EQV Sen Sen
#          | Qua Var* Sen
# Qua      : FORALL | EXISTS
# Pred     : TRUE | FALSE | UserPred
# UserPred : IDENTIFIER

# Subgrammar for Term
#
# Term     : TermFunc | TermCnpd | Const | Var | ScmVar
# TermFunc : FUNC FUNCOP Term*
# TermCnpd : DATA CONSTR Term* | List
# List     : NIL | CONS Term List
# Const    : NUMBER | STRING | BOOLEAN
# Var      : VARSYMBOL
# ScmVar   : SCMSYMBOL

from pprint import pformat


# === FOL-Structures ===

class Sen(object):

    def __init__(self, *subs):
        self.subs = subs

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __not__(self):
        return Not(self)

    def __le__(self, other):
        return Rule(self, other)

    def __repr__(self):
        return '{}{}'.format(self.__class__.__name__, self.subs)


class And(Sen):

    def __repr__(self):
        return '{} & {}'.format(*self.subs)


class Or(Sen):
    pass


class Not(Sen):
    pass


class Rule(Sen):

    def __repr__(self):
        return '{{{} <= {}}}'.format(self.lhs, self.rhs)

    @property
    def lhs(self): return self.subs[0]

    @property
    def rhs(self): return self.subs[1]

    @property
    def key(self):
        return self.lhs.verb


class SenAtom(Sen):
    pass


class Pred(SenAtom):

    """A predicate is upon 0 or more terms.

    A term can be a constant, Variable or Schematic Variable when
    defining rule.

    """

    def __init__(self, verb, *terms):
        assert type(verb) is str
        self.verb = verb
        self.terms = terms

    def __repr__(self):
        return '{}/{}{}'.format(self.verb, self.arity, list(self.terms) or '')

    def __call__(self, *terms):
        self.terms = terms
        return self

    @property
    def arity(self):
        return len(self.terms)

    @property
    def key(self):
        return self.verb


class Eq(SenAtom):

    "Eq is a special Atomic Sentence on 2 terms."

    def __repr__(self):
        t1, t2 = self.subs
        return '({} == {})'.format(t1, t2)


class NotEq(SenAtom):

    "NotEq is a special Atomic Sentence on 2 terms."

    def __repr__(self):
        t1, t2 = self.subs
        return '({} != {})'.format(t1, t2)


class Term(object):

    "Abstract class."

    def __init__(self, *a, **kw):
        raise NotImplementedError(
            'Need override constructor in subclasses.')


class TermCnpd(Term):

    'Compound Term.'

    def __init__(self, con, *terms):
        self.con = con
        self.terms = terms

    def __repr__(self):
        return '{}{}'.format(self.con, self.terms)

    def __call__(self, *terms):
        self.terms = terms


class Var(Term):

    "Variable Term."

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return '${}'.format(self.symbol)

    def __hash__(self):
        return hash(self.symbol)

    def __eq__(self, other):
        return type(other) == type(self) and self.symbol == other.symbol


class Func(Term):

    "Function Term is *evaluable* term."

    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def __iter__(self):
        yield self.op
        yield self.args

    def __repr__(self):
        op_name = self.op.__name__
        return '{}{}'.format(op_name, self.args or '')
        # return '{}{}'.format(self.op, self.args or '')

    def __call__(self, *args):
        self.args = args
        return self

    def __hash__(self):
        return hash(self.op)

    def eval(self):
        return self.op(*self.args)

    def can_eval(self):
        """Test if each argument term already has value."""
        return all(type(a) not in (Var, Func) for a in self.args)


ap = Func


def Assert(func):
    return Eq(True, func)

def AssertFunc(op, *terms):
    return Eq(True, Func(op, *terms))


def Gt(l, r):
    return Eq(True, Func(op.gt, l, r))

def Lt(l, r):
    return Eq(True, Func(op.lt, l, r))

def Ge(l, r):
    return Eq(True, Func(op.ge, l, r))

def Le(l, r):
    return Eq(True, Func(op.le, l, r))

asp = AssertFunc

import operator as op


class ScmVar(Term):

    """Schematic/Template Variable is a special term only used during
    defining rules.

    A ScmVar is instantiated to Var Term by *universal instantiation*
    (standardize-apart) during ask/query.

    """

    def __init__(self, mark):
        assert isinstance(mark, str) and mark
        self._mark = mark

    def __repr__(self):
        return ':{}'.format(self._mark)

    # def __getattr__(self, k):
    #     if not k.startswith('_'): return ap(getattr,)

    def __eq__(self, other): return Eq(self, other)
    def __ne__(self, other): return NotEq(self, other)
    def __gt__(self, other): return AssertFunc(op.gt, self, other)
    def __ge__(self, other): return AssertFunc(op.ge, self, other)

    def __add__(self, other): return ap(op.add, self, other)
    def __sub__(self, other): return ap(op.sub, self, other)
    def __mul__(self, other): return ap(op.mul, self, other)
    def __rmul__(self, other): return ap(op.mul, self, other)
    def __mod__(self, other): return ap(op.mod, self, other)
    def __pow__(self, other): return ap(op.pow, self, other)
    def __pos__(self, other): return ap(op.pos, self, other)
    def __neg__(self, other): return ap(op.neg, self, other)
    def __matmul__(self, other): return ap(op.matmul, self, other)
    def __truediv__(self, other): return ap(op.truediv, self, other)
    def __rtruediv__(self, other): return ap(op.truediv, other, self)


# === Easy Use ===
def easy(cls):
    class _E(object):
        def __getattr__(self, k):
            return cls(k)
        def __call__(self, words):
            for w in words:
                yield cls(w)
    cls.new = _E()
    # return cls
    return cls.new

var = easy(Var)
scm = easy(ScmVar)
pred = easy(Pred)


# === Unification | Substitution*Evaluation ===

FAIL = '-FAIL-'


def unify(x, y, u={}):

    "Unification can apply to `Term` as well as `Pred`."

    if u is FAIL:
        return FAIL

    # unify Term (9-cases in total)
    # - Constant Term (implicit): c=c
    elif x == y:
        return u
    elif isinstance(x, list) and isinstance(y, list) or \
         isinstance(x, tuple) and isinstance(y, tuple):
        for a, b in zip(x, y):
            u = unify(a, b, u)
            if u is FAIL: break
        return u

    # - Variable Term: v=v, v=c|v=f, c=f|v=f
    elif isinstance(x, Var):
        return unify_var(x, y, u)
    elif isinstance(y, Var):
        return unify_var(y, x, u)

    # - Functional Term: f=f, f=c|c=f
    # FIXME: To suppress the need with cases involving Func, keep
    # every targeted Func instance evaluated before entering `unify`.
    elif isinstance(x, Func) or isinstance(y, Func):
        raise ValueError(
            'Unsupported unification for unevaluated Func object. '
            '(cf. equivalence of functions - undecidability).')

    # - Compound Term
    # FIXME: Support Compound Term in the future maybe.
    # - Can Func be treated as specialized Compound Term?
    elif isinstance(x, TermCnpd) and isinstance(y, TermCnpd):
        if x.con != y.con:
            return FAIL
        else:
            return unify(x.terms, y.terms, u)

    # unify Atomic Sentence
    # - Eq/NotEq
    #   Verify both to be true?
    # - User Predicate
    elif isinstance(x, Pred) and isinstance(y, Pred):
        if x.verb != y.verb:
            return FAIL
        # FIXME: Whether to allow variable to bind to any predicate
        # verb, i.e. to allow variable to represent Relations
        # (predicate symbols, verbs) besides Constants
        # (subjective/objective)?
        #
        u = unify(x.verb, y.verb, u)
        if len(x.terms) != len(y.terms):
            raise ValueError('Arity mismatch: {} =?= {}'.format(x, y))
        return unify(x.terms, y.terms, u)

    # unify Complex Sentence

    # FIXME: Sentences can only be unified after
    # evaluation. Unification successes iff both sides have the same
    # truth value.
    elif isinstance(x, Sen) and isinstance(y, Sen):
        if type(x) == type(y):
            return unify(x.subs, y.subs, u)
        else:
            raise NotImplementedError()

    # FAIL: type inconsistent
    else:
        return FAIL


def occurs_in(v, x):
    "Occurence check."
    assert isinstance(v, Var)
    if isinstance(x, Var):
        # Unifiable whether they are equal Var.
        return False
    elif isinstance(x, TermCnpd):
        return any(occurs_in(v, y) for y in x.terms)
    elif isinstance(x, Pred):
        return any(occurs_in(v, y) for y in x.terms)
    else:
        return False


def unify_var(v, z, u):
    "Try append a consistent binding `(v: z)` into unifier `u`."
    assert isinstance(v, Var)
    if u is FAIL:
        return FAIL
    elif isinstance(z, Var) and v == z:
        return u
    elif occurs_in(v, z):
        raise ValueError('Occurence found.')
        # return FAIL
    elif v in u:
        return unify(u[v], z, u)
    elif z in u:
        return unify(v, u[z], u)
    else:
        u1 = dict(u); u1[v] = z
        return u1


def updated_subst(u):
    "Substitute all Var's in `u` w.R.t. itself until fix point."
    def root(x):
        if x in u:
            return root(u[x])
        elif isinstance(x, TermCnpd):
            return TermCnpd(x.con, *map(root, x.terms))
        else:
            return x
    return {k: root(k) for k in u}


def subst(u, x):
    """Substitute `u[x]` for `x` recursively.

    - Evaluate `Func` when possible - this is also 'substitution':
    `Func` is replaced by another value: `result of Func`.

    """
    # Term
    if isinstance(x, Var):
        if x in u: return u[x]
        else:      return x
    elif isinstance(x, TermCnpd):
        return TermCnpd(x.con, *[subst(u, y) for y in x.terms])
    elif isinstance(x, Func):
        # Eval func here after post-order construction.
        f = Func(x.op, *(subst(u, a) for a in x.args))
        if f.can_eval():
            return f.eval()
        else:
            return f
    # Sentence
    elif isinstance(x, Pred):
        return Pred(x.verb, *(subst(u, y) for y in x.terms))
    elif isinstance(x, Sen):
        return type(x)(*(subst(u, y) for y in x.subs))
    # Constant term
    else:
        # Constant
        return x


from itertools import count

stand_count = count()
def univ_inst(x, env=None):
    """Instantiate ScmVar to Var. This is like beta-reduction in the
    context of lambda calculus.

    """
    if env is None:
        env = {}
    if isinstance(x, ScmVar):
        if x._mark not in env:
            env[x._mark] = Var('{}_#{}'.format(x._mark, next(stand_count)))
        return env[x._mark]
    elif isinstance(x, Var):
        raise
    elif isinstance(x, TermCnpd):
        return TermCnpd(x.con, *(univ_inst(y, env) for y in x.terms))
    elif isinstance(x, Func):
        return Func(x.op, *(univ_inst(a, env) for a in x.args))
    elif isinstance(x, Pred):
        return Pred(x.verb, *(univ_inst(y, env) for y in x.terms))
    elif isinstance(x, Sen):
        return type(x)(*(univ_inst(y, env) for y in x.subs))
    else:
        # Constant
        return x

def stand_reset():
    global stand_count
    stand_count = count()


# === Knowledge Base ===
#
# Properties of a KB
# + tell: register a logical sentence
# + ask : perform a query
# + indexing: quick retrieval of matching sentences w.R.t.
#   - verifying a new tell
#   - a real-time query

class KB(object):

    def __init__(self):
        self.facts = {}
        self.rules = {}

    def __repr__(self):
        return pformat((self.facts, self.rules))

    # Augmenting KB
    def tell(self, sen):
        """Let the KB tell a sentence, which can be either
        - An Atomic Sentence or
        - A Definite Clause (Rule).
        Complex Sentence supported?
        """
        if isinstance(sen, SenAtom):
            if isinstance(sen, Pred):
                self.add_fact(sen)
            elif isinstance(sen, Eq):
                raise NotImplementedError
            elif isinstance(sen, NotEq):
                raise NotImplementedError
            else: raise
        elif isinstance(sen, Rule):
            self.add_rule(sen)
        elif isinstance(sen, (And, Or, Not)):
            raise NotImplementedError

    # Dealing facts
    def has_fact(self, key):
        return key in self.facts

    def add_fact(self, pred):
        if pred.key not in self.facts:
            self.facts[pred.key] = []
        self.facts[pred.key].append(pred)

    def get_facts(self, symbol):
        if symbol in self.facts:
            yield from self.facts[symbol]

    # Dealing rules
    def has_rule(self, key):
        return key in self.rules

    def add_rule(self, rule):
        if rule.key not in self.rules:
            self.rules[rule.key] = []
        self.rules[rule.key].append(rule)

    def get_rules(self, key):
        if key in self.rules:
            yield from self.rules[key]

    # ASK
    def ask(kb, goal):
        stand_reset()
        for u in kb.ask_1(goal, {}):
            # Update all RHS in `u` recursively thus each rooted Var
            # gets substituted by its root.
            u1 = updated_subst(u)
            for k in set(u):
                if '#' in k.symbol:
                    u1.pop(k)
            yield u1

    # Dispatch ASK of 1 query.
    def ask_1(kb, goal0, u):
        goal = subst(u, goal0)
        # !query Atomic Sentence
        if isinstance(goal, SenAtom):
            yield from kb.ask_atom(goal, u)
        # !query Complex Sentence
        elif isinstance(goal, Not):
            yield from kb.ask_not(goal, u)
        elif isinstance(goal, And):
            yield from kb.ask_and(goal, u)
        elif isinstance(goal, Or):
            yield from kb.ask_or(goal, u)
        elif isinstance(goal, Rule):
            yield from kb.ask_rule(goal, u)
        else:
            raise ValueError('Illegal goal: {}'.format(goal0))

    # ASK for Atomic Sentence.
    def ask_atom(kb, goal, u):
        'Dispatch Atomic Sentence asked.'
        if isinstance(goal, Eq):
            yield from kb.ask_eq(goal, u)
        elif isinstance(goal, NotEq):
            yield from kb.ask_not_eq(goal, u)
        else:
            yield from kb.ask_pred(goal, u)

    def ask_eq(kb, goal, u):
        s1, s2 = goal.subs
        u1 = unify(s1, s2, u)
        if u1 is not FAIL:
            yield u1

    def ask_not_eq(kb, goal, u):
        s1, s2 = goal.subs
        u1 = unify(s1, s2, u)
        if u1 is FAIL:
            yield u

    def ask_pred(kb, goal, u):
        yield from kb.ask_fact(goal, u)
        yield from kb.ask_rule(goal, u)

    # ASK for Complex Sentence.
    def ask_or(kb, goal, u):
        for sub in goal.subs:
            yield from kb.ask_1(sub, u)

    def ask_and(kb, a, u):
        if type(a) is And:
            l, r = a.subs
            for u1 in kb.ask_and(l, u):
                for u2 in kb.ask_1(r, u1):
                    yield u2
        else:
            yield from kb.ask_1(a, u)

    def ask_not(kb, goal, u):
        if not any(kb.ask_1(goal, u)):
            yield u

    # Ask for simple Predicate.
    def ask_fact(kb, goal, u):
        for fact in kb.get_facts(goal.key):
            fact1 = univ_inst(fact)
            u1 = unify(fact1, goal, u)
            # u1 = unify(fact, goal, u)
            if u1 is not FAIL:
                yield u1

    # Ask for rule (complex predicate).
    def ask_rule(kb, goal, u):
        for rule in kb.get_rules(goal.key):
            rule1 = univ_inst(rule)
            if isinstance(rule, Rule):
                u1 = unify(rule1.lhs, goal, u)
                if u1 is not FAIL:
                    yield from kb.ask_and(rule1.rhs, u1)
                # Retract standardized-apart-counter?
                pass
            else:
                # Singleton rule like k.append(NIL, scm.y, scm.y)
                yield from kb.ask_1(rule1, u)


# === API ===



# === Front-end ===
# - Supply tricky sugar for using KB functionalities neatly.

class PredM(Pred):
    "Subtyping `Pred` to support adding instance into KB when called."
    def __init__(self, verb, kb=None):
        self.verb = verb
        self.kb = kb

    def __call__(self, *terms):
        self.terms = terms
        return self

    def __lt__(self, terms):
        assert isinstance(terms, tuple)
        self.kb.tell(Pred(self.verb, *terms))

    def __lshift__(self, tlist):
        assert isinstance(tlist, list)
        for terms in tlist:
            self.kb.tell(Pred(self.verb, *terms))

    def __le__(self, rhs):
        lhs = Pred(self.verb, *self.terms)
        if isinstance(rhs, (list, tuple)):
            assert len(rhs) > 0
            sub = rhs[0]
            for sub1 in rhs[1:]:
                sub = And(sub, sub1)
            self.kb.tell(Rule(lhs, sub))
        elif isinstance(rhs, Sen):
            self.kb.tell(Rule(lhs, rhs))

    # def __getitem__(self, terms):
    #     if type(terms) != tuple:
    #         terms = (terms,)
    #     self.terms = terms
    #     return self

    # def __setitem__(self, terms, rhs):
    #     lhs = self[terms]
    #     self.kb.tell(Rule(lhs, rhs))

    def __pos__(self):
        "For tell schematic facts?"
        self.kb.tell(Pred(self.verb, *self.terms))


class KBMan(object):

    """KB-Manager simplifies adding facts/rules.

    Example declarations:

        k = KBMan()
        k.father('John', 'Lucy')
        k.father('Andreas', 'John')
        k.ancester(scm.x, scm.y) <= k.father(scm.x, scm.y)
        k.ancester(scm.x, scm.y) <= (
            k.father(scm.x, scm.z) &
            k.ancester(scm.z, scm.y)
        )

    Example queries:

        >>> q = k.query
        >>> q1 = q.ancester(var.x, 'Lucy')
        >>> next(q1)
        {$x: 'John'}
        >>> next(q1)
        {$x: 'Andreas'}
        >>> next(q1)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        StopIteration

    """

    class QueryMan(object):
        def __init__(self, kb):
            self._kb = kb
        def __getattr__(self, k):
            if k in self.__dict__:
                return object.__getattr__(self, k)
            else:
                kb = self._kb
                if k in kb.facts or k in kb.rules:
                    def q(*args):
                        args1 = []
                        # Convert uppercase str to Var.
                        for arg in args:
                            if isinstance(arg, str) and \
                               (arg.isupper() or\
                                arg.startswith('$')):
                                args1.append(Var(arg))
                            else:
                                args1.append(arg)
                        yield from self._kb.ask(Pred(k, *args1))
                    q.__doc__ = "Query with keyword {}.".format(repr(k))
                    return q
                else:
                    raise ValueError('Unrecognized predicate to be queried.')

    def __init__(self):
        kb = KB()
        self._kb = kb
        self.query = KBMan.QueryMan(kb)

    def __getattr__(self, k):
        if k in self.__dict__:
            return object.__getattr__(self, k)
        else:
            return PredM(k, kb=self._kb)


class builtins:
    Eq = Eq
    NotEq = NotEq
    Func = Func
    Assert = Assert
