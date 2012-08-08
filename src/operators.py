from __future__ import print_function

# Author: Christopher D. Parks
# Email: chris.parks@uky.edu
# Date: 4 December 2011
# Class: CS655

"""
All "builtin" functions and operators are defined here.
"""

import operator
import math
from functools import wraps
from src.primitives import *

__all__ = [
    'builtin_ops', 'UserError', 'print_ops',
]

def native(function):
    """Turn a lisp list into an args tuple for native python functions"""
    @wraps(function)
    def translator(ls):
        args = []
        while ls:
            args.append(car(ls))
            ls = cdr(ls)
        return function(*args)
    return translator

def variadic_op(binary_op):
    """Turn a binary operator into a variadic operator using a fold loop"""
    @wraps(binary_op)
    def new_op(ls):
        if isnil(ls):
            raise ValueError("{} takes at least 1 operand".format(binary_op))
        else:
            out = car(ls)
            ls = cdr(ls)
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

def display(list):
    """Can't put print in a lambda either"""
    print(str_list(list)[1:-1])

# Builtin functions
builtin_ops = {
    # Unary operators
    '1+': lambda x: x + 1,
    '1-': lambda x: x - 1,
    'SQRT': math.sqrt,
    'SIN': math.sin,
    'COS': math.cos,
    'TAN': math.tan,
    'NOT': operator.not_,
    'CAR': car,
    'CDR': cdr,
    'PAIR?': ispair,
    'ATOM?': isatom,
    'NULL?': isnil,
    'INTEGER?': lambda x: isinstance(x, int),
    'REAL?': lambda x: isinstance(x, (int, float)),
    'NUMBER?': lambda x: isinstance(x, (int, float)),
    'STRING?': lambda x: isinstance(x, str) and not isinstance(x, Symbol),
    'SYMBOL?': lambda x: isinstance(x, Symbol),
    'LIST?': lambda x: isnil(x) or not isatom(x),
    'ERROR': error,

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
}

# Convert to native
builtin_ops = dict((key, native(value)) for (key, value) in builtin_ops.items())

# Variadic Operators
variadic_ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv
}

# Add variadic operators
builtin_ops.update((key, variadic_op(value)) for (key, value) in variadic_ops.items())

# Add whole-list operators
builtin_ops["PRINT"] = display
builtin_ops["LIST"] = lambda ls: ls

# I was too lazy to type out all the car/cdr variants, so I made something to
# generate them.
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
        return eval('lambda x: ' + body(word)) # magic

    for word in doubles + triples + quadles:
        builtin_ops[word.join('CR')] = build_lambda(word)

make_variants()

# Make printing look nice
sorted_ops = sorted(op for op in builtin_ops)
op_width = max(len(name) for name in sorted_ops) + 2
op_columns = sum(1 for i in sorted_ops if len(i) <= 2)

def print_table(items, columns, width):
    """Prints items in ascii table"""
    for i, name in enumerate(items):
        if i % columns == 0:
            print("\t", end='')
        if (i + 1) % columns == 0:
            print('{0:{1}}'.format(name, width))
        else:
            print('{0:{1}}'.format(name, width), end='')
    if (i + 1) % columns != 0:
        print() # final newline

def print_ops():
    print("Builtin Functions/Operators:")
    print_table(sorted_ops, op_columns, op_width)
