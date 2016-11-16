from collections import namedtuple

BuiltIn = namedtuple('BuiltIn', 'bfunc')

Const = namedtuple('Const', 'value')
Var = namedtuple('Var', 'name')
Abst = namedtuple('Abst', 'pars body')
Appl = namedtuple('Appl', 'func args')

B = BuiltIn
C = Const
V = Var
A = Abst
P = Appl

def interpret(expr, env):
    if isinstance(expr, Const):
        return expr.value, env
    elif isinstance(expr, Var):
        return env[expr.name], env
    elif isinstance(expr, BuiltIn):
        return expr, env
    elif isinstance(expr, Abst):
        return expr, env
    elif isinstance(expr, Appl):
        v_func, _ = interpret(expr.func, env)
        v_args = []
        for arg in expr.args:
            v_arg, _ = interpret(arg, env)
            v_args.append(v_arg)

        if isinstance(v_func, BuiltIn):
            return v_func.bfunc(*v_args), env
        else:
            binds = dict(zip(v_func.pars, v_args))
            return interpret(v_func.body, {**env, **binds})


env = {'x': 9}

expr = Var('x')
v, env1 = interpret(expr, env)
print(v)


import operator as op
expr = Appl(BuiltIn(op.add), [
    Const(9), Const(1)
])
v, env1 = interpret(expr, env)
print(v)

expr = Appl(Abst(
    ('x', 'y'),
    Appl(BuiltIn(op.add), [Var('y'), Var('x')])
), [Const('abc'), Const('dd')])
v, env1 = interpret(expr, env)
print(v)

expr = P(A(['x', 'y'],
           P(B(op.add), [V('y'), V('x')])
), [C('abc'), C('dd')])
v, env1 = interpret(expr, env)
print(v)
