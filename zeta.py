# encoding: utf-8
from __future__ import print_function, unicode_literals

if __name__ == '__main__':
    import sys
    from src.eval import zeta, printError

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename) as stream:
                zeta(stream)
        except IOError as e:
            printError(e)
    else:
        zeta(sys.stdin)

