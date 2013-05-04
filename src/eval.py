from __future__ import print_function

"""
Evaluates lisp expressions. 'repl' reads from stdin. The other stuff probably
shouldn't be called unless you know what you're doing.
"""

__all__ = ['zeta', 'repl', 'eval', 'parse', 'parse_file']

from src.parsers import parse, parse_file
from src.primitives import *
from src.operators import *

class Forms(object):
    """Map symbol name to form implementation"""
    def __init__(self):
        self.actions = {}

    def register(self, function):
        """Register form with name"""
        name = function.__name__.split('_')[-1]
        self.actions[Symbol(name)] = function
        return function

    def get(self, name):
        """Get implementation by name"""
        return self.actions.get(name)

# Module level jump table for form implementations
forms = Forms()

@forms.register
def eval_if(exprs, env):
    """ (if (null? ls) nil (car ls)) """
    test, _ = eval(car(exprs), env)
    if test:
        return eval(car(cdr(exprs)), env)
    else:
        return eval(car(cdr(cdr(exprs))), env)

@forms.register
def eval_let(body, env):
    """ (let ([x 2] [y 8]) (+ x y)) """
    local_env = Environment(scope=env)
    for name, expr in car(body):
        value, _ = eval(expr, local_env)
        local_env[name] = value
    value, _ = eval(single(Symbol('BEGIN')) + cdr(body), local_env)
    return value, env

@forms.register
def eval_lambda(function, env):
    """
    (lambda (x)(* x x)) => (LAMBDA (X)(BEGIN (* x x)) (ENV))
    """
    formals = car(function)
    if isatom(car(cdr(function))):
        body = car(cdr(function))
    else:
        body = car(car(cdr(function)))
    if body == Symbol('DEF-BEGIN'):
        body = single(Symbol('BEGIN')) + cdr(car(cdr(function)))
    else:
        body = single(Symbol('BEGIN')) + cdr(function)
    return (Symbol('LAMBDA-CLOSURE'), formals, body, env), env

@forms.register
def eval_quote(ls, env):
    """ (quote (1 2 3 4)) or '(1 2 3 4) """
    return car(ls), env

@forms.register
def eval_cond(conds, env):
    """
    (cond
        ((null? ls) nil)
        (#t (car ls)))
    """
    while not isnil(conds):
        test, _ = eval(car(car(conds)), env)
        if test:
            return eval(car(cdr(car(conds))), env)
        conds = cdr(conds)
    return NIL, env

@forms.register
def eval_begin(expressions, env):
    """
    (begin
        (print "twice x" (* 2 x))
        (print "x squared" (* x x)))
    """
    value = NIL
    while not isnil(expressions):
        value, env = eval(car(expressions), env)
        expressions = cdr(expressions)
    return value, env

@forms.register
def eval_or(expressions, env):
    """Short circuit or"""
    value = False
    while not isnil(expressions):
        test, _ = eval(car(expressions), env)
        value = value or test
        if value:
            return True, env
        expressions = cdr(expressions)
    return value, env

@forms.register
def eval_and(expressions, env):
    """Short circuit and"""
    value = True
    while not isnil(expressions):
        test, _ = eval(car(expressions), env)
        value = value and test
        if not value:
            return False, env
        expressions = cdr(expressions)
    return value, env

@forms.register
def eval_define(rest, env):
    """
    Names:
    (define pi 3.1415926535897931)

    Functions:
    (define (gcd x y)
        (if (= y 0
            x
            (gcd y (mod x y)))))
    =>
    (LAMBDA-CLOSURE (X Y) (BEGIN (IF (= Y 0) X (GCD Y (MOD X Y)))) (ENV))
    """
    if isatom(car(rest)):
        name = car(rest)
        value, _  = eval(car(cdr(rest)), env)
        env[name] = value
        return NIL, env
    else:
        name = car(car(rest))
        formals = cdr(car(rest))
        body = single(Symbol('DEF-BEGIN')) + cdr(rest)
        function = (Symbol('LAMBDA'), formals, body)
        closure, _  = eval(function, env)
        env[name] = closure
        return NIL, env

@forms.register
def eval_delete(rest, env):
    if isatom(car(rest)):
        env.pop(car(rest))
    return NIL, env

@forms.register
def eval_load(ls, env):
    with open(car(ls)) as stream:
        value = NIL
        for expression in parse_file(stream):
            value, env = eval(expression, env)
        return value, env

# Some useful selectors
def closure_body(closure):
    return car(cdr(cdr(closure)))

def closure_params(closure):
    return car(cdr(closure))

def closure_env(closure):
    return car(cdr(cdr(cdr(closure))))

def eval(ls, env):
    """Evaluate s-expression parsed into nested tuples"""
    #print("EVAL: {}\n".format(str_list(ls)))
    if isinstance(ls, Symbol):
        return env[ls], env
    elif isnil(ls) or not isinstance(ls, tuple):
        return ls, env
    first, rest = car(ls), cdr(ls)
    action = forms.get(first)
    if action is not None:
        return action(rest, env)
    return apply(first, tuple(eval(expr, env)[0] for expr in rest), env)

def apply(closure, actuals, env):
    """Apply function to actual parameters"""
    #print("APPLY: {}".format(str_list(closure)))
    #print("ON:    {}\n".format(str_list(params)))
    if isatom(closure):
        function = env[closure]
        if hasattr(function, '__call__'):
            value = function(actuals)
        else:
            value, env = apply(function, actuals, env)
    else:
        if car(closure) == Symbol('LAMBDA-CLOSURE'):
            formals = closure_params(closure)
            if len(formals) != len(actuals):
                raise Exception("Wrong number of actual parameters")
            new_env = Environment.combine(closure_env(closure), env)
            new_env.update(**dict(zip(formals, actuals)))
            value, _ = eval(closure_body(closure), new_env)
        else:
            closure, _ = eval(closure, env)
            value, env = apply(closure, actuals, env)
    return value, env

def repl(env):
    print("Type (help) for global definitions")
    while 1:
        value = NIL
        try:
            value, env = eval(parse(), env)
            print("Value: {}\n".format(str_list(value)))
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print("{}: {}\n".format(e.__class__.__name__, str_list(e)))

def zeta(stream):
    _, env = eval_load(single('src/library.lisp'), global_env)
    if stream.isatty():
        repl(env)
    else:
        for expression in parse_file(stream):
            _, env = eval(expression, env)

