'''Define some utility functions and classes'''

from collections import namedtuple
from pyparsing import *

# Constants used by both parsers
LPAREN, RPAREN, LBRACKET, RBRACKET, LBRACE, RBRACE, QUOTE = "()[]{}'"

# Sets of left and right brackets for fast check in parser
LEFT = set([LPAREN, LBRACKET, LBRACE])
RIGHT = set([RPAREN, RBRACKET, RBRACE])

# Fast check for match
MATCHES = set([(LPAREN, RPAREN), (LBRACKET, RBRACKET), (LBRACE, RBRACE)])

# Get corresponding right bracket for left bracket
LEFT2RIGHT = {
    LPAREN: RPAREN,
    LBRACKET: RBRACKET,
    LBRACE: RBRACE,
}

class UnbalancedException(Exception):
    '''Unbalanced parentheses, brackets, or braces'''
    pass

def balance(left, right):
    '''Are left and right brackets matched?'''
    if (left, right) not in MATCHES:
        raise UnbalancedException("Expected '{}'".format(LEFT2RIGHT[left]))

def convert(f):
    '''Parse action that converts the token using unary function f'''
    return lambda string, location, tokens: f(tokens[0])

def constant(value):
    '''Parse action that returns a constant value'''
    return lambda *args: value

def do(parser, action):
    '''Make a copy (since we have different parsers using the same
       sub-parsers) and set the parse action
    '''
    return parser.copy().setParseAction(action)

