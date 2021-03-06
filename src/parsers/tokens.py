# encoding: utf-8
from __future__ import print_function, unicode_literals

'''Define token recognizers common to interactive and file parser'''

import sys
try:
    from pyparsing import *
except ImportError:
    print('Please install the pyparsing library')
    sys.exit(1)

from src.parsers.utils import *
from src.primitives import Symbol, NIL

# Empty list
nil = do(CaselessLiteral('nil'), constant(NIL))

# Booleans
true = do(Regex(r'#(t|T)'), constant(True))
false = do(Regex(r'#(f|F)'), constant(False))

# Numbers
real = do(Regex(r"[+-]?\d+\.\d*([eE][+-]?\d+)?"), convert(float))
decimal = do(Regex(r"-?(0|[1-9])\d*"), convert(int))

# Double quoted string
string = do(dblQuotedString, convert(lambda token: token[1:-1]))

# Symbols
specials = "-./_~:*+=!<>?&^%@$|"
identifier = do(Word(alphas + specials, alphanums + specials), convert(Symbol))

# Comment to end of line
comment = Literal(";") + restOfLine

# Non-composite tokens
atom = nil | true | false | real | decimal | string | identifier

