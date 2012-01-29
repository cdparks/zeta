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
from primitives import *

__all__ = [
    'unary_ops', 'binary_ops', 'variadic_ops', 'builtin_ops', 'UserError',
    'print_ops', 'print_accessors'
]

class UserError(Exception):
    """Error raised by user"""
    pass

def error(msg):
    """Can't raise in a lambda"""
    raise UserError(msg)

# Must parse out 1 argument from argument list
unary_ops = {
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
}

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
        unary_ops[word.join('CR')] = build_lambda(word)

make_variants()

# Must parse out 2 arguments from argument list
binary_ops = {
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

def variadic_op(binary_op):
    """Turn a binary operator into a variadic operator using a fold loop"""
    @wraps(binary_op)
    def new_op(ls):
        if isnil(ls):
            raise ValueError("%s takes at least 1 operand" % binary_op)
        else:
            out = car(ls)
            ls = cdr(ls)
            while not isnil(ls):
                out = binary_op(out, car(ls))
                ls = cdr(ls)
            return out
    return new_op

def display(list):
    """Can't put print in a lambda either"""
    print str_list(list)[1:-1]

# Send the whole argument list
variadic_ops = {
    '+': variadic_op(operator.add),
    '-': variadic_op(operator.sub),
    '*': variadic_op(operator.mul),
    '/': variadic_op(operator.div),
    'LIST': lambda ls: ls,
    'PRINT': display,
}

# When function names appear in arg-list, pretend all names are in one
# namespace so 'lookup' can find them.
builtin_ops = set(unary_ops.keys() + binary_ops.keys() + variadic_ops.keys())

# Make printing look nice
regular_ops = sorted(op for op in builtin_ops if not (op.startswith('C') and op.endswith('R')))
accessor_ops = sorted(sorted(op for op in builtin_ops if op.startswith('C') and op.endswith('R')), key = len)
op_width = max(len(name) for name in regular_ops) + 2
op_columns = sum(1 for i in regular_ops if len(i) <= 2)

def print_table(items, columns, width):
    """Prints items in ascii table"""
    for i, name in enumerate(items):
        if i % columns == 0:
            print "\t",
        if (i + 1) % columns == 0:
            print '{0:{1}}'.format(name, width)
        else:
            print '{0:{1}}'.format(name, width),
    if (i + 1) % columns != 0:
        print # final newline

def print_ops():
    print "Builtin Functions/Operators:"
    print_table(regular_ops, op_columns, op_width)

def print_accessors():
    print "CAR/CDR Variants:"
    print_table(accessor_ops, op_columns, op_width)
