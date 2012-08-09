from __future__ import print_function

# Author: Christopher D. Parks
# Email: chris.parks@uky.edu
# Date: 4 December 2011
# Class: CS655

"""
Parse s-expressions like this:

(lambda (x)(* 2 x))

and turn them into nested None-terminated tuples like this:

('LAMBDA', ('x', None), ('*', 2, 'x', None), None)
"""

__all__ = ['Parser']

import sys
from functools import wraps
from src.primitives import str_list, Symbol
from re import compile

class ParseError(BaseException):
    """When parsing fails and cannot continue"""
    pass

class Enum(object):
    """Python doesn't have enums. This is close enough."""
    def __init__(self, *args):
        for i, name in enumerate(args):
            setattr(self, name, i)
        self.last = i
        self.names = args

    def __contains__(self, id):
        return 0 <= id <= self.last

# This is kind of overkill since we really only test against LPAREN, RPAREN,
# QUOTE, and EOL. Consider it future-proofing. Use like lexemes.LPAREN or
# if thing in lexemes:
lexemes = Enum('LPAREN', 'RPAREN', 'INT', 'FLOAT', 'STRING', 'SYMBOL', 'QUOTE', 'NIL', 'TRUE', 'FALSE', 'EOL')

class Token(object):
    """Carries around an item's token type and canonical value"""
    def __init__(self, type, value):
        self.type = type
        self.value = value

def make_token(atom, str=False):
    """Build a token out of a list of characters"""

    # compile caches these the first time
    INT_PATTERN = compile('^-?\d+$')
    FLOAT_PATTERN = compile('-?^\d+\.\d+$')

    value = "".join(atom)
    token = None
    if str:
        # Allows empty string, cased strings
        token = Token(lexemes.STRING, value)
    elif value:
        # Canonical casing
        value = value.upper()
        # T => Python True
        if value == '#T':
            token = Token(lexemes.TRUE, True)
        elif value == '#F':
            token = Token(lexemes.FALSE, False)
        # NIL => Python empty list
        elif value == 'NIL':
            token = Token(lexemes.NIL, [])
        # INT => Python arbitrary precision int
        elif INT_PATTERN.match(value):
            token = Token(lexemes.INT, int(value))
        # FLOAT => Python 64-bit float
        elif FLOAT_PATTERN.match(value):
            token = Token(lexemes.FLOAT, float(value))
        # SYMBOL => Python Symbol extends str
        else:
            token = Token(lexemes.SYMBOL, Symbol(value))
    return token, []

def my_input(prompt=None, filein=sys.stdin, fileout=sys.stdout):
    """Replacement for builtin raw_input that adds stream parameters"""
    if prompt is not None:
        fileout.write(prompt)
        fileout.flush()
    line = filein.readline()
    if line:
        return line.strip()
    else:
        raise EOFError

class Parser(object):
    """
    Because we want to allow line-breaks in expressions, this parser has
    important (and easy to break) internal state. The 'stream' attribute in
    particular has to be refreshed by calling 'lex' when a break is encountered
    and the parentheses stack is non-zero. The only method a user should call
    from here is 'parse'
    """
    def __init__(self, stream=sys.stdin):
        self.stack = 0
        if stream.isatty():
            self.interactive = True
            self.readFirst = lambda: my_input('[]> ', filein=stream)
            self.readNext = lambda: my_input(filein=stream)
        else:
            self.interactive = False
            self.readFirst = self.readNext = lambda: my_input(filein=stream)
        # Put similar state transitions in a jump table
        self.punctuation = {
            '(': Token(lexemes.LPAREN, '('),
            ')': Token(lexemes.RPAREN, ')'),
            "'": Token(lexemes.QUOTE, Symbol('QUOTE')),
            ' ': None, '\t': None, '\n': None, '\r\n': None,
        }

    def lex(self, read):
        """Yield tokens to parser. Can yield empty tokens - see skip_empty"""
        atom = []
        instring = False
        for char in read():
            if not instring:
                if char in self.punctuation:
                    token, atom = make_token(atom)
                    yield token
                    token = self.punctuation[char]
                    yield token
                elif char == ']':
                    # "Finishes" a heavily parenthesized expression for user
                    token, atom = make_token(atom)
                    yield token
                    for i in range(self.stack):
                        yield Token(lexemes.RPAREN, ')')
                elif char == ';':
                    # Skip comment to EOL
                    break
                elif char == '"':
                    # Begin double-quoted string
                    instring = True
                else:
                    # Accumulate characters in atom-list
                    atom.append(char)
            elif char == '"':
                # End double-quoted string
                instring = False
                token, atom = make_token(atom, str=True)
                yield token
            else:
                # Accumulate string characters in atom-list
                atom.append(char)
        token, atom = make_token(atom)
        yield token
        # to avoid StopIteration, yield EOL when finished.
        yield Token(lexemes.EOL, None)

    def skip_empty(self):
        """Keep lex smaller by checking for empty tokens here"""
        token = next(self.stream)
        while token is None:
            token = next(self.stream)
        return token

    def next_token(self):
        """Replaces 'next' and refreshes stream on newlines"""
        token = self.skip_empty()
        while token.type == lexemes.EOL:
            self.stream = self.lex(self.readNext)
            token = self.skip_empty()
        return token

    def finish(self, msg):
        """Checks for extraneous output"""
        token = self.skip_empty()
        if token.type != lexemes.EOL:
                raise ParseError(msg)
        self.stream.close()

    def nested_expr(self):
        """Inside parens"""
        out = []
        self.stack += 1
        token = self.next_token()
        while token.type != lexemes.RPAREN:
            if token.type == lexemes.LPAREN:
                out.append(self.nested_expr())
            elif token.type == lexemes.QUOTE:
                out.append([token.value, self.s_expr()])
            else:
                out.append(token.value)
            token = self.next_token()
        self.stack -= 1
        return out

    def s_expr(self):
        """Outside parens"""
        token = self.next_token()
        if token.type == lexemes.LPAREN:
            return self.nested_expr()
        elif token.type == lexemes.RPAREN:
            raise ParseError("Expression cannot begin with ')'")
        elif token.type == lexemes.QUOTE:
            return [token.value, self.s_expr()]
        else:
            return token.value

    def parse(self):
        try:
            self.stream = self.lex(self.readFirst)
#value = self.to_list(self.s_expr())
            value = self.s_expr()
            self.finish("Extra input following '{}'".format(str_list(value)))
            return value
        except ParseError as e:
            print("ParseError: {}".format(e))
            return None
        except EOFError:
            if not self.interactive and self.stack != 0:
                print("ParseError: EOF inside unterminated expression")
            raise

if __name__ == '__main__':
    """Run the parser on stdin for testing"""
    parser = Parser()
    while 1:
        try:
            print(parser.parse())
        except (KeyboardInterrupt, EOFError):
            break
