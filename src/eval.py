from __future__ import print_function

"""
Evaluates lisp expressions. 'repl' reads from stdin. The other stuff probably
shouldn't be called unless you know what you're doing.
"""

__all__ = ['zeta', 'repl', 'eval', 'parse', 'parse_file']

from src.parsers import parse, parse_file
from src.primitives import *
from src.operators import *

def eval_if(exprs, env):
    """ (if (null? ls) nil (car ls)) """
    test, _ = eval(car(exprs), env)
    if test:
        return eval(car(cdr(exprs)), env)
    else:
        return eval(car(cdr(cdr(exprs))), env)

def eval_let(body, env):
    """ (let ([x 2] [y 8]) (+ x y)) """
    local_env = Environment(scope=env)
    for name, expr in car(body):
        value, _ = eval(expr, local_env)
        local_env[name] = value
    value, _ = eval(single(Symbol('BEGIN')) + cdr(body), local_env)
    return value, env

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

def eval_quote(ls, env):
    """ (quote (1 2 3 4)) or '(1 2 3 4) """
    return car(ls), env

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

def eval_delete(rest, env):
    if isatom(car(rest)):
        env.pop(car(rest))
    return NIL, env

# Not part of 'forms', just used by the others
def eval_list(ls, env):
    if isnil(ls):
        return NIL
    else:
        value, _ = eval(car(ls), env)
        return cons(value, eval_list(cdr(ls), env))

def eval_load(ls, env):
    with open(car(ls)) as stream:
        value = NIL
        for expression in parse_file(stream):
            value, env = eval(expression, env)
        return value, env

# Jump table for forms.
forms = {
    Symbol('IF'): eval_if,
    Symbol('LAMBDA'): eval_lambda,
    Symbol('LET'): eval_let,
    Symbol('QUOTE'): eval_quote,
    Symbol('COND'): eval_cond,
    Symbol('OR'): eval_or,
    Symbol('AND'): eval_and,
    Symbol('BEGIN'): eval_begin,
    Symbol('DEFINE'): eval_define,
    Symbol('DELETE'): eval_delete,
    Symbol('LOAD'): eval_load,
}

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
    if isatom(ls) or isnil(ls):
        if isinstance(ls, Symbol):
            return env[ls], env
        else:
            return ls, env
    else:
        first, rest = car(ls), cdr(ls)
        if isatom(first):
            action = forms.get(first, None)
            if action is not None:
                return action(rest, env)
            else:
                return apply(first, eval_list(rest, env), env)
        else:
            return apply(first, eval_list(rest, env), env)

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
            parameter_mapping = {formal: actual for formal, actual in zip(formals, actuals)}
            new_env = Environment.combine(closure_env(closure), env)
            new_env.update(**parameter_mapping)
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
            print("Error: {}\n".format(str_list(e)))

def zeta(stream):
    _, env = eval_load(single('src/library.lisp'), global_env)
    if stream.isatty():
        repl(env)
    else:
        for expression in parse_file(stream):
            _, env = eval(expression, env)

