from __future__ import print_function

# Author: Christopher D. Parks
# Email: chris.parks@uky.edu
# Date: 4 December 2011
# Class: CS655

"""
Evaluates lisp expressions. 'repl' reads from stdin. The other stuff probably
shouldn't be called unless you know what you're doing.
"""

__all__ = ['eval', 'repl']

import sys
import operator
from functools import wraps
from src.parse import Parser
from src.primitives import *
from src.operators import *

def help(env):
    """Print environment, forms, and builtin operators/functions"""
    def env_only(env):
        if isnil(env):
            print("\t{}".format(str_list(env)))
        else:
            print("\t{} -> {}".format(str_list(car(car(env))), str_list(car(cdr(car(env))))))
            env_only(cdr(env))
    print("Environment:")
    env_only(env.list)
    print("Forms:")
    for name in sorted(forms.keys()):
        print("\t{}".format(name))
    print_ops()
    return None, env

def reverse(ls):
    """
    Python has a short stack and no tail-call optimization. Since we're
    "sharing" the stack with the user, most helper functions replace a
    normally recursive action with a while loop. Sometimes this means
    building things in reverse.
    """
    reversed = None
    while not isnil(ls):
        reversed = cons(car(ls), reversed)
        ls = cdr(ls)
    return reversed

# The following 10 functions are form evaluation actions. They're fairly self-
# explanatory, but the policy is important. Each function takes a list and an
# environment and returns a value and an environment. This consistency allows
# us to put them in a jump table called 'forms' and dispatch from there.
def eval_if(exprs, env):
    """ (if (null? ls) nil (car ls)) """
    test, _ = lisp_eval(car(exprs), env)
    if test:
        return lisp_eval(car(cdr(exprs)), env)
    else:
        return lisp_eval(car(cdr(cdr(exprs))), env)

def eval_let(body, env):
    """ (let ((x 2) (y 8)) (+ x y)) """
    def make_env(ls, env):
        if isnil(ls):
            return env.list
        else:
            first, rest = car(ls), cdr(ls)
            name = car(first)
            value, _ = lisp_eval(car(cdr(first)), env)
            return cons(make_list(name, value), make_env(rest, env))
    local_env = Environment(make_env(car(body), env))
    value, _ = lisp_eval(append(make_list(Symbol('BEGIN')), cdr(body)), local_env)
    return value, env

def eval_lambda(function, env):
    """
    (lambda (x)(* x x)) => (LAMBDA (X)(BEGIN (* x x)) (ENV))
    """
    params = car(function)
    if isatom(car(cdr(function))):
        body = car(cdr(function))
    else:
        body = car(car(cdr(function)))
    if body == 'DEF-BEGIN':
        body = append(make_list(Symbol('BEGIN')), cdr(car(cdr(function))))
    else:
        body = append(make_list(Symbol('BEGIN')), cdr(function))
    return cons('LAMBDA-CLOSURE', cons(params, cons(body, env))), env

def eval_quote(ls, env):
    """ (quote (1 2 3 4)) or '(1 2 3 4) """
    def fix(ls):
        """Turn a non-canonical list into a canonical one"""
        real = None
        while not isnil(ls):
            real = cons(car(ls), real)
            ls = cdr(ls)
        return reverse(real)
    value = car(ls)
    if isatom(value):
        return value, env
    else:
        return fix(value), env

def eval_cond(conds, env):
    """
    (cond
        ((null? ls) nil)
        (T (car ls)))
    """
    while not isnil(conds):
        test, _ = lisp_eval(car(car(conds)), env)
        if test:
            return lisp_eval(car(cdr(car(conds))), env)
        conds = cdr(conds)
    return None, env

def eval_begin(expressions, env):
    """
    (begin
        (print "twice x" (* 2 x))
        (print "x squared" (* x x)))
    """
    value = None
    while not isnil(expressions):
        value, env = lisp_eval(car(expressions), env)
        expressions = cdr(expressions)
    return value, env

def eval_or(expressions, env):
    """Short circuit or"""
    value = None
    while not isnil(expressions):
        test, _ = lisp_eval(car(expressions), env)
        value = value or test
        if value:
            return True, env
        expressions = cdr(expressions)
    return value, env

def eval_and(expressions, env):
    """Short circuit and"""
    value = True
    while not isnil(expressions):
        test, _ = lisp_eval(car(expressions), env)
        value = value and test
        if not value:
            return None, env
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

    Allows multiple expressions:
    (define (factorial n)
        (define (loop x out)
            (if (< x 2)
                out
                (loop (* x out) (- x 1))))
        (loop n 1))

    =>

    (LAMBDA-CLOSURE (N) (BEGIN (DEFINE (LOOP X OUT) (IF (< X 2) OUT (LOOP (* X OUT) (- X 1)))) (LOOP N 1)) (ENV))
    """
    if isatom(car(rest)):
        name = car(rest)
        value, _  = lisp_eval(car(cdr(rest)), env)
        return None, Environment(cons(cons(name, cons(value, None)), env.list))
    else:
        name = car(car(rest))
        params = cdr(car(rest))
        body = append(make_list('DEF-BEGIN'), cdr(rest))
        function = make_list(Symbol('LAMBDA'), params, body)
        env = Environment(remove(name, env.list))
        closure, _  = lisp_eval(function, env)
        return None, Environment(cons(cons(name, cons(closure, None)), env.list))

def eval_delete(rest, env):
    if isatom(car(rest)):
        env = Environment(remove(car(rest), env.list))
    return None, env

def eval_load(file, env):
    """Modify current environment by evaluating file"""
    with open(car(file)) as stream:
        env = repl(env, stream)
    return None, env

# Not part of 'forms', just used by the others
def eval_list(ls, env):
    if isnil(ls):
        return None
    else:
        value, _ = lisp_eval(car(ls), env)
        return cons(value, eval_list(cdr(ls), env))

# Jump table for forms.
forms = {
    'IF': eval_if,
    'LAMBDA': eval_lambda,
    'LET': eval_let,
    'QUOTE': eval_quote,
    'COND': eval_cond,
    'OR': eval_or,
    'AND': eval_and,
    'BEGIN': eval_begin,
    'DEFINE': eval_define,
    'DELETE': eval_delete,
    'LOAD': eval_load,
}

def lookup(id, env, msg):
    """Find id in env or builtins, else raise NameError with msg"""
    while not isnil(env):
        if id == car(car(env)):
            return car(cdr(car(env)))
        env = cdr(env)
    if id in builtin_ops:
        return id
    raise NameError(msg.format(id))

def remove(id, env):
    """Attempt to remove an id from the environment"""
    new_env = None
    while not isnil(env):
        if id != car(car(env)):
            new_env = cons(car(env), new_env)
        env = cdr(env)
    return reverse(new_env)

def update(formals, actuals, env):
    """Bind formals to actuals in environment"""
    while 1:
        if isnil(formals):
            if isnil(actuals):
                return env
            raise TypeError("Too many arguments")
        elif isnil(actuals):
            raise TypeError("Not enough arguments")
        else:
            env = cons(cons(car(formals), cons(car(actuals), None)), env)
        formals = cdr(formals)
        actuals = cdr(actuals)

# Some useful selectors
def closure_body(closure):
    return car(cdr(cdr(closure)))

def closure_params(closure):
    return car(cdr(closure))

def closure_env(closure):
    return cdr(cdr(cdr(closure)))

def lisp_eval(ls, env):
    """Evaluate s-expression parsed into nested None-terminated tuple"""
    #print "EVAL: " + str_list(ls) + "\n"
    if isatom(ls):
        if ls == 'HELP':
            return help(env)
        elif isinstance(ls, Symbol):
            return lookup(ls, env.list, "Cannot find '{}'"), env
        else:
            return ls, env
    else:
        first, rest = car(ls), cdr(ls)
        if isatom(first):
            action = forms.get(first, None)
            if action is not None:
                return action(rest, env)
            else:
                return lisp_apply(first, eval_list(rest, env), env)
        else:
            return lisp_apply(first, eval_list(rest, env), env)

def lisp_apply(function, params, env):
    """Apply function to params in environment"""
    #print "APPLY: " + str_list(function)
    #print "ON:    " + str_list(params) + "\n"
    if isatom(function):
        op = builtin_ops.get(function, None)
        if op is not None:
            value = op(params)
        else:
            value, env = lisp_apply(lookup(function, env.list, "Cannot find/apply '{}'"), params, env)
    else:
        if car(function) == 'LAMBDA-CLOSURE':
            new_env = Environment(update(closure_params(function), params, append(closure_env(function).list, env.list)))
            value, _ = lisp_eval(closure_body(function), new_env)
        else:
            function, _  = lisp_eval(function, env)
            value, env = lisp_apply(function, params, env)
    return value, env

def repl(env=Environment(None), stream=sys.stdin, library=None, debug=False):
    """
    Provide read-eval-print-loop on stream in environment. Returns modified
    environment.
    """

    parser = Parser(stream)
    if library is not None:
        try:
            env = repl(env, stream=open(library))
        except IOError:
            print("Warning: Could not load library '{}'".format(library))
        else:
            if parser.interactive:
                print("Using library '{}'. Type 'help' for more information.".format(library))
    while 1:
        value = None
        try:
            value, env = lisp_eval(parser.parse(), env)
            if parser.interactive:
                print("Value: {}\n".format(str_list(value)))
            if debug:
                print("[DEBUG] Environment: {}".format(str_list(env.list)))
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print("Error: {}\n".format(str_list(e)))
    return env
