# encoding: utf-8
from __future__ import print_function, unicode_literals

"""
Evaluates lisp expressions. 'repl' reads from stdin. The other stuff probably
shouldn't be called unless you know what you're doing.
"""

__all__ = ['zeta', 'printError']

from src.parsers import parse, parse_file
from src.primitives import *
from src.operators import *

import functools

class Context(object):
    """Map symbol name to form implementation"""
    def __init__(self):
        self.forms = {}

    def register(self, function):
        """Register form by name"""
        name = function.__name__.split('_')[-1]
        self.forms[Symbol(name)] = function
        return function

    def get(self, name):
        """Get implementation by name"""
        return self.forms.get(name)

# Module level jump table for form implementations
context = Context()

@context.register
def eval_let(body, env):
    """Bind each name and evaluate the body"""
    local_env = Environment(scope=env)
    for name, expr in car(body):
        value = eval(expr, local_env)
        local_env[name] = value
    return eval(single(Symbol('BEGIN')) + cdr(body), local_env)

@context.register
def eval_lambda(function, env):
    """Build a closure"""
    formals = car(function)
    if isatom(car(cdr(function))):
        body = car(cdr(function))
    else:
        body = car(car(cdr(function)))
    if body == Symbol('DEF-BEGIN'):
        body = single(Symbol('BEGIN')) + cdr(car(cdr(function)))
    else:
        body = single(Symbol('BEGIN')) + cdr(function)
    return Closure(body, formals, env)

@context.register
def eval_quote(ls, env):
    """Return the quoted object unevaluated"""
    return car(ls)

@context.register
def eval_begin(exprs, env):
    """Evaluate a sequence of expressions and return the last one in
       a Thunk to keep simplifying"""
    for expr in exprs[:-1]:
        eval(expr, env)
    return Thunk(exprs[-1])

@context.register
def eval_if(exprs, env):
    """Evaluate the first expression and return the second or third
       in a Thunk to keep simplifying"""
    if len(exprs) != 3:
        raise Exception('Malformed if: "{}"'.format(exprs))
    test, consequent, alternative = exprs
    return Thunk(consequent if eval(test, env) else alternative)

@context.register
def eval_cond(exprs, env):
    """Evaluate conditions until one evaluates to True. Then
       return the body in a Thunk to keep simplifying"""
    for cond, expr in exprs:
        test = eval(cond, env)
        if test:
            return Thunk(expr)
    return NIL

@context.register
def eval_or(exprs, env):
    """Short circuit or"""
    for expr in exprs:
        if eval(expr, env):
            return True
    return False

@context.register
def eval_and(exprs, env):
    """Short circuit and"""
    for expr in exprs:
        if not eval(expr, env):
            return False
    return True

@context.register
def eval_define(expr, env):
    """Define a name or function in the current environment"""
    if isatom(car(expr)):
        name = car(expr)
        env[name] = eval(car(cdr(expr)), env)
        return NIL
    else:
        name = car(car(expr))
        formals = cdr(car(expr))
        body = single(Symbol('DEF-BEGIN')) + cdr(expr)
        function = (Symbol('LAMBDA'), formals, body)
        closure = eval(function, env)
        env[name] = closure
        return NIL

@context.register
def eval_delete(expr, env):
    """Remove a named object from the current environment"""
    if isatom(car(expr)):
        env.pop(car(expr))
    return NIL

@context.register
def eval_load(s, env):
    """Evaluate sequence of expressions in current environment"""
    with open(car(s)) as stream:
        value = NIL
        for expression in parse_file(stream):
            value = eval(expression, env)
        return value

def eval(expr, env):
    """Evaluate s-expression parsed into tuples"""
    while 1:
        if isinstance(expr, Symbol):
            return env[expr]
        elif isnil(expr) or not isinstance(expr, tuple):
            return expr

        first, rest = splits(expr)
        form = context.get(first)
        if form is not None:
            expr = form(rest, env)
            if isinstance(expr, Thunk):
                expr = expr.value
            else:
                return expr
        else:
            exprs = tuple(eval(expr, env) for expr in expr)
            function, actuals = splits(exprs)
            if isinstance(function, Closure):
                if len(function.formals) != len(actuals):
                    raise Exception("Wrong number of actual parameters")
                env = Environment(function.env, **dict(zip(function.formals, actuals)))
                expr = function.body
            elif hasattr(function, '__call__'):
                return function(actuals)
            else:
                raise Exception("Cannot apply '{}'".format(function))

def printError(e):
    """Print exception with name and reason"""
    print('{}: {}\n'.format(e.__class__.__name__, str_list(e)))

def repl(env):
    print("Type (help) for global definitions")
    while 1:
        value = NIL
        try:
            value = eval(parse('[]> '), env)
            print("Value: {}\n".format(str_list(value)))
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            printError(e)

def zeta(stream):
    eval_load(single('src/library.lisp'), global_env)
    if stream.isatty():
        repl(global_env)
    else:
        for expr in parse_file(stream):
            try:
                eval(expr, global_env)
            except (KeyboardInterrupt, EOFError):
                break
            except Exception as e:
                printError(e)
                break

