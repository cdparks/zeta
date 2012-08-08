# Author: Christopher D. Parks
# Email: chris.parks@uky.edu
# Date: 4 December 2011
# Class: CS655

"""
Includes the basic things needed to make the interpreter work. There's some
weirdness in 'cdr' related to the fact that the parser produces non-canonical
lists. This is done for performance and does not affect the user.
"""

from functools import wraps

__all__ = [
    'cons', 'car', 'cdr', 'isnil', 'isatom', 'ispair', 'make_list', 'append',
    'str_list', 'Symbol', 'Environment'
]

class Symbol(str):
    """
    We need to use something string-like for symbols but we want to be able to
    differentiate them using isinstance(thing, type)
    """
    pass

class Environment(object):
    """
    Environments are still represented as association lists. This just wraps
    an association list so closures aren't printing huge lists. Purely
    aesthetic.
    """
    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return "(ENV)"

def type_check(types):
    """Certain functions should check their arguments"""
    def make_decorator(function):
        @wraps(function)
        def checked(*args):
            for thing in args:
                if not isinstance(thing, types):
                    raise TypeError("Wrong argument type")
            return function(*args)
        return checked
    return make_decorator

def cons(a, b):
    """Tuples instantiate fast and have random access"""
    return (a, b)

@type_check(tuple)
def car(x):
    return x[0]

@type_check(tuple)
def cdr(x):
    """
    cdr cheats - this works on 'real' linked-lists as well as
    'flat' s-expressions represented by random access tuples.
    This allows us to optimize accessing values and cons'ing.

    for example:
        cdr of ('1', ('2', ('3', None))) is ('2', ('3', None))
        cdr of ('1', '2', '3', None) is ('2', '3', None)
    """

    if len(x) == 2:
        return x[-1]
    else:
        return x[1:]

def isnil(thing):
    return thing is None

def isatom(thing):
    return not isinstance(thing, tuple)

def ispair(thing):
    if isatom(thing):
        return False
    else:
        first, rest = car(thing), cdr(thing)
        return isatom(first) and not isnil(rest) and isatom(rest)

def isenv(thing):
    return isinstance(thing, Environment)

def str_list(ls, sep=' '):
    """Print lists, atoms, and dotted pairs"""
    out = []
    if isatom(ls):
        if ls is True:
            return 'T'
        elif ls is None or ls is False:
            return 'NIL'
        else:
            return str(ls)
    while not isnil(ls):
        if isatom(ls):
            if isenv(ls):
                out.append(str_list(ls))
            else:
                out.append('.' + sep + str_list(ls))
            break
        elif isnil(cdr(ls)):
            out.append(str_list(car(ls)))
        else:
            out.append(str_list(car(ls)) + sep)
        ls = cdr(ls)
    return '(' + ''.join(out) + ')'

def make_list(*args):
    """Make tuple None-terminated"""
    return args + tuple([None])

@type_check((tuple, type(None)))
def append(ls1, ls2):
    if isnil(ls1):
        return ls2
    elif isnil(ls2):
        return ls1
    else:
        return cons(car(ls1), append(cdr(ls1), ls2))
