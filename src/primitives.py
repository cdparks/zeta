# encoding: utf-8
from __future__ import print_function, unicode_literals

try:
    # Python 2
    str = unicode
except NameError:
    # Python 3
    pass

from functools import wraps

__all__ = [
    'NIL', 'single', 'cons', 'car', 'cdr', 'splits', 'isnil', 'isatom', 'append',
    'str_list', 'Symbol', 'Environment', 'Closure', 'Thunk',
]

NIL = ()

class Symbol(str):
    """
    We need to use something string-like for symbols but we want to be able to
    differentiate them using isinstance(thing, type)
    """

    def __new__(cls, value):
        return str.__new__(cls, value.upper())

class Thunk(object):
    """Wrap an expression that can be further simplified"""
    def __init__(self, value):
        self.value = value

class Closure(object):
    """Expression 'body' closes over environment 'env'"""

    def __init__(self, body, formals, env):
        self.body = body
        self.formals = formals
        self.env = env

    def __repr__(self):
        return '<CLOSURE>'

class Environment(object):
    """Stack of bindings mapping symbols to values"""

    def __init__(self, scope=None, **bindings):
        self.next = scope
        self.bindings = bindings

    def __repr__(self):
        return "<ENV>"

    def __getitem__(self, key):
        """Find key starting in most local scope"""
        scope = self
        while scope is not None:
            if key in scope.bindings:
                return scope.bindings[key]
            scope = scope.next
        raise NameError("No binding for name '{}' in scope".format(key))

    def __setitem__(self, key, value):
        """Map key to value in current scope"""
        self.bindings[key] = value

    def pop(self, key):
        """Remove key from environment"""
        scope = self
        while scope is not None:
            if key in scope.bindings:
                return binding.pop(key)
            scope = scope.next
        raise NameError("No binding for name '{}' in scope".format(key))

    def update(self, **kwargs):
        """Add bindings to current scope"""
        self.bindings.update(**kwargs)

    def __iter__(self):
        """Get all keys defined in environment"""
        scope = self
        while scope is not None:
            for key in scope.bindings:
                yield key
            scope = scope.next

def type_check(*arg_types, **kw_types):
    """Check types of arguments for function"""
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

def single(x):
    '''Making singleton tuples is ugly'''
    return x,

@type_check(object, tuple)
def cons(a, b):
    """Push value on front of list"""
    return single(a) + b

@type_check(tuple)
def car(x):
    """Get value on front of list"""
    return x[0]

@type_check(tuple)
def cdr(x):
    """Get all values comprising tail of list"""
    return x[1:]

@type_check(tuple)
def splits(x):
    """Split list into head and tail"""
    return x[0], x[1:]

def isnil(x):
    """Is x an empty list?"""
    return x == NIL

def isatom(x):
    """Is x a non-composite object?"""
    return not isinstance(x, tuple)

def isenv(x):
    """Is x an environment?"""
    return isinstance(x, Environment)

def str_list(ls):
    if isatom(ls):
        if ls is True:
            return '#t'
        elif ls is False:
            return '#f'
        elif hasattr(ls, '__call__'):
            return '#{native-code}'
        else:
            return str(ls)
    elif ls == NIL:
        return 'nil'
    else:
        return '(' + ' '.join(str_list(x) for x in ls) + ')'

@type_check(tuple, tuple)
def append(ls1, ls2):
    """Append ls2 to ls1"""
    return ls1 + ls2

