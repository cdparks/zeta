# Author: Christopher D. Parks
# Email: chris.parks@uky.edu
# Date: 4 December 2011
# Class: CS655

import sys

if __name__ == '__main__':
  from src import repl
  if '--debug' in sys.argv:
    repl(debug=True)
  else:
    repl(library='src/library.lisp')
