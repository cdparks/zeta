# encoding: utf-8
from __future__ import print_function, unicode_literals

__all__ = ['parse_file']

from src.parsers.utils import *
from src.parsers.tokens import *
from src.primitives import Symbol

# Accept but remove from output
lparen, rparen, lbracket, rbracket, lbrace, rbrace = map(Suppress, "()[]{}")

# Recursive rules need a forward declaration
sexpression = Forward()

# Quoted expression
quoted = Group("'" + sexpression)
@quoted.setParseAction
def _(string, location, tokens):
    return (Symbol('QUOTE'), tokens[0][1])

# Parenthesized expressions
body = ZeroOrMore(sexpression)
composite = (
      do(Group(lparen + body + rparen), convert(tuple))
    | do(Group(lbracket + body + rbracket), convert(tuple))
    | do(Group(lbrace + body + rbrace), convert(tuple))
)

# Set recursive value
sexpression << (composite | quoted | atom)

# A program is just a series of s-expressions
program = ZeroOrMore(sexpression).ignore(comment)

def parse_file(stream):
    return program.parseFile(stream, parseAll=True).asList()

