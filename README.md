#zeta is a small lisp interpreter written in Python 3.

It started as a project for a class, and now I just hack on it occasionally for fun.

#Running
To start the interpreter, run 'python zeta.py'. By default, the interpreter
runs as a read-evaluate-print loop. However, one can use file redirection
to execute a script non-interactively:

`python zeta < script.lisp`

The interpreter adjusts to avoid printing unnecessary prompts.

To see what names are defined in the global environment, type `(help)` at
the prompt.

To exit interactive mode, type `ctrl-D` or `ctrl-C`.

#Features
* Built-in types: integer, float, bool, string, symbol, and list
* Scheme-like define syntax
* Tail-call optimization
* Parentheses-aware REPL

#Credits
* Originally a port of the Common Lisp meta-circular evaluator in [Dr. Raphael Finkel's](http://www.cs.uky.edu/~raphael/) book ["Advanced Programming Language Design"](http://www.amazon.com/dp/0805311912).
* Figured out tail-call optimization by reading Peter Norvig's ["(An ((Even Better) Lisp) Interpreter (in Python))"](http://norvig.com/lispy2.html).

#Miscellaneous
Requires the [pyparsing](http://sourceforge.net/projects/pyparsing/) library.

Released under the [MIT License](http://opensource.org/licenses/MIT).

