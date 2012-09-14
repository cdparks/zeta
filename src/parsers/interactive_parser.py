__all__ = ["parse"]

import readline
from src.primitives import Symbol
from src.parsers.tokens import atom, comment
from src.parsers.utils import *

# Drive the parser with brackets and quote
punctuation = MatchFirst([
    do(Literal(char), constant(char)) for char in "()[]{}'"
])

# Build lexer
lexer = ZeroOrMore(punctuation | atom).ignore(comment)

def build_parser():
    '''Build interactive parse() function'''
    stack = []
    pop = stack.pop
    push = stack.append

    def stream():
        '''Token generator. Yields empty list with no input'''
        for parsed, start, end in lexer.scanString(input('[]> ')):
            for token in parsed:
                yield token
        while stack:
            for parsed, start, end in lexer.scanString(input()):
                for token in parsed:
                    yield token
        yield NIL

    def s_expr(stream):
        '''Input is an s-expression, a quoted s-expression, or an atom'''
        token = next(stream)
        if token in LEFT:
            return nested_expr(stream, token)
        elif token in RIGHT:
            raise UnbalancedException("Expression cannot begin with '{}'".format(token))
        elif token == QUOTE:
            return Symbol('QUOTE'), s_expr(stream)
        else:
            return token

    def nested_expr(stream, left):
        '''Input is an expression between two brackets'''
        out = []
        push(left)
        token = next(stream)
        while token not in RIGHT:
            if token in LEFT:
                out.append(nested_expr(stream, token))
            elif token == QUOTE:
                out.append((Symbol('QUOTE'), s_expr(stream)))
            else:
                out.append(token)
            token = next(stream)
        balance(pop(), token)
        return tuple(out)

    def parser():
        '''Reset bracket stack and start parsing'''
        while stack:
            pop()
        return s_expr(stream())
    return parser

parse = build_parser()

