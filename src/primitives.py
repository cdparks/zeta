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
    'cons', 'car', 'cdr', 'isnil', 'isatom', 'ispair', 'append',
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

def type_check(*arg_types, **kw_types):
    def make_decorator(function):
        @wraps(function)
        def checked(*args, **kwargs):
            if len(args) != len(arg_types):
                raise TypeError("Wrong number of positional arguments")
            for arg, type in zip(args, arg_types):
                if not isinstance(arg, type):
                    raise TypeError("Wrong argument type")
            for key, value in kwargs.items():
                if key in kw_types and not isinstance(value, kw_types[kw]):
                    raise TypeError("Wrong argument type")
            return function(*args, **kwargs)
        return checked
    return make_decorator


@type_check(object, list)
def cons(a, b):
    return [a] + b

@type_check(list)
def car(x):
    return x[0]

@type_check(list)
def cdr(x):
    return x[1:]

def isnil(thing):
    return thing == []

def isatom(thing):
    return not isinstance(thing, list)

def ispair(thing):
    if isatom(thing):
        return False
    else:
        first, *rest = thing
        return isatom(first) and not isnil(rest) and isatom(rest)

def isenv(thing):
    return isinstance(thing, Environment)

def str_list(ls, sep=' '):
    """Print lists, atoms, and dotted pairs"""
    out = []
    if isatom(ls):
        if ls is True:
            return '#t'
        elif ls is False:
            return '#f'
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

@type_check(list, list)
def append(ls1, ls2):
    return ls1 + ls2
