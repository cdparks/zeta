from functools import wraps

__all__ = [
    'NIL', 'single', 'cons', 'car', 'cdr', 'isnil', 'isatom', 'append',
    'str_list', 'Symbol', 'Environment'
]

NIL = ()

class Symbol(str):
    """
    We need to use something string-like for symbols but we want to be able to
    differentiate them using isinstance(thing, type)
    """

    def __new__(cls, value):
        return str.__new__(cls, value.upper())

class Empty(object):
    def __init__(self):
        self.bindings = NIL

empty = Empty()

class Environment(Empty):
    def __init__(self, scope=empty, **local_bindings):
        if hasattr(scope, 'bindings'):
            self.bindings = cons(local_bindings, scope.bindings)
        else:
            self.bindings = cons(local_bindings, scope)

    @classmethod
    def combine(cls, env1, env2):
        return Environment(scope=env1.bindings + env2.bindings)

    def __repr__(self):
        return "<ENV>"

    def get(self, key, default=NIL):
        try:
            return self[key]
        except NameError:
            return default

    def __getitem__(self, key):
        for binding in self.bindings:
            if key in binding:
                return binding[key]
        raise NameError("No binding for name '{}' in scope".format(key))

    def update(self, iterable=None, **kwargs):
        if iterable is None:
            iterable = NIL
        car(self.bindings).update(iterable, **kwargs)

    def __setitem__(self, key, value):
        car(self.bindings)[key] = value

    def pop(self, key):
        for binding in self.bindings:
            if key in binding:
                binding.pop(key)
        raise NameError("No binding for name '{}' in scope".format(key))

    def __iter__(self):
        for binding in self.bindings:
            for key in binding:
                yield key

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

def single(x):
    '''Making singleton tuples is ugly'''
    return x,

@type_check(object, tuple)
def cons(a, b):
    return single(a) + b

@type_check(tuple)
def car(x):
    return x[0]

@type_check(tuple)
def cdr(x):
    return x[1:]

def isnil(thing):
    return thing == NIL

def isatom(thing):
    return not isinstance(thing, tuple)

def isenv(thing):
    return isinstance(thing, Environment)

def str_list(ls):
    if isatom(ls):
        if ls is True:
            return '#t'
        elif ls is False:
            return '#f'
        elif ls == NIL:
            return 'nil'
        elif hasattr(ls, '__call__'):
            return '#{native-code}'
        else:
            return str(ls)
    return '(' + ' '.join(str_list(x) for x in ls) + ')'

@type_check(tuple, tuple)
def append(ls1, ls2):
    return ls1 + ls2
