# encoding: utf-8
from __future__ import print_function, unicode_literals

'''Define some utility functions and classes'''

from collections import namedtuple
from pyparsing import *

# Constants used by both parsers
PUNCTUATION = (
    LPAREN,
    RPAREN,
    LBRACKET,
    RBRACKET,
    LBRACE,
    RBRACE,
    QUOTE,
) = "()[]{}'"

# Sets of left and right brackets for fast check in parser
LEFT = {
    LPAREN,
    LBRACKET,
    LBRACE,
}

RIGHT = {
    RPAREN,
    RBRACKET,
    RBRACE,
}

# Fast check for match
MATCHES = {
    (LPAREN, RPAREN),
    (LBRACKET, RBRACKET),
    (LBRACE, RBRACE),
}

# Get corresponding right bracket for left bracket
LEFT2RIGHT = {
    LPAREN: RPAREN,
    LBRACKET: RBRACKET,
    LBRACE: RBRACE,
}

class ParseError(Exception):
    '''General parse error'''
    pass

class UnbalancedError(ParseError):
    '''Unbalanced parentheses, brackets, or braces'''
    pass

def balance(left, right):
    '''Are left and right brackets matched?'''
    if (left, right) not in MATCHES:
        raise UnbalancedError("Expected '{}'".format(LEFT2RIGHT[left]))

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

