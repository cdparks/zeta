# encoding: utf-8
from __future__ import print_function, unicode_literals

"""
All "builtin" functions and operators are defined here.
"""

import math
import operator
from functools import wraps
from src.primitives import *

__all__ = [
    'global_env', 'UserError'
]

def native(function):
    """Turn a lisp list into an args tuple for native python functions"""
    @wraps(function)
    def decorated(ls):
        return function(*ls)
    return decorated

def variadic_op(binary_op):
    """Turn a binary operator into a variadic operator using a left fold"""
    @wraps(binary_op)
    def new_op(ls):
        if isnil(ls):
            raise ValueError("{} takes at least 1 operand".format(binary_op))
        else:
            out, ls = splits(ls)
            while not isnil(ls):
                out = binary_op(out, car(ls))
                ls = cdr(ls)
            return out
    return new_op

class UserError(Exception):
    """Error raised by user"""
    pass

def error(msg):
    """Can't raise in a lambda"""
    raise UserError(msg)

def display(ls):
    print(str_list(ls)[1:-1])
    return NIL

def read():
    """Read input from stdin"""
    import sys
    from src.parsers.file_parser import parse_file
    from src.parsers.interactive_parser import parse
    return parse() if sys.stdin.isatty() else parse_file(sys.stdin)

def _eval(expr):
    """Evaluate an expression in the global environment"""
    from src import eval
    return eval(expr, global_env)

def help():
    print("Defined:")
    for key in sorted(global_env):
        print("  {}".format(key))
    return NIL

# Builtin functions
global_env = Environment(**{
    Symbol(key): native(value) for key, value in {
        # Nullary operator
        'HELP': help,
        'READ': read,

        # Unary operators
        '++': lambda x: x + 1,
        '--': lambda x: x - 1,
        '~': operator.neg,
        'SQRT': math.sqrt,
        'SIN': math.sin,
        'COS': math.cos,
        'TAN': math.tan,
        'NOT': operator.not_,
        'CAR': car,
        'CDR': cdr,
        'ATOM?': isatom,
        'NULL?': isnil,
        'INTEGER?': lambda x: isinstance(x, int),
        'REAL?': lambda x: isinstance(x, (int, float)),
        'NUMBER?': lambda x: isinstance(x, (int, float)),
        'STRING?': lambda x: isinstance(x, str) and not isinstance(x, Symbol),
        'SYMBOL?': lambda x: isinstance(x, Symbol),
        'LIST?': lambda x: isnil(x) or not isatom(x),
        'ERROR': error,
        'EVAL': _eval,

        # Binary Operators
        '<': operator.lt,
        '>': operator.gt,
        '=': operator.eq,
        '<=': operator.le,
        '>=': operator.ge,
        '/=': operator.ne,
        'MOD': operator.mod,
        'APPEND': append,
        'CONS': cons,
        'EQ?': lambda x, y: x is y,
    }.items()
})

# Variadic Operators
global_env.update(**{
    Symbol(key): variadic_op(value) for key, value in {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '//': operator.floordiv
    }.items()
})

# Add whole-list operators
global_env[Symbol('PRINT')] = display
global_env[Symbol('LIST')] = lambda ls: ls

# Generate car/cdr variants
def make_variants():
    from itertools import product

    letters = 'AD'
    doubles = [''.join(word) for word in product(letters, letters)]
    triples = [''.join(word) for word in product(letters, letters, letters)]
    quadles = [''.join(word) for word in product(letters, letters, letters, letters)]
    # quadles isn't a word (but it should be)

    def build_lambda(word):
        def body(letters):
            if not letters:
                return 'x'
            elif letters[0] == 'A':
                return 'car(' + body(letters[1:]) + ')'
            else:
                return 'cdr(' + body(letters[1:]) + ')'
        return eval('lambda x: ' + body(word)) # Danger

    for word in doubles + triples + quadles:
        global_env[Symbol(word.join('CR'))] = native(build_lambda(word))

# Add them to environment
make_variants()

