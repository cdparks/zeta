#zeta is a small lisp interpreter written in Python 3.

It started as a project for a class, and now I just hack on it occasionally for fun.

#Running
To start the interpreter, run 'python zeta.py'. By default, the interpreter
runs as a read-evaluate-print loop. However, one can pass a filename as the first
argument to execute a script non-interactively:

`python zeta script.lisp`

The interpreter adjusts to avoid printing unnecessary prompts.

To see what names are defined in the global environment, type `(help)` at
the prompt.

To exit interactive mode, type `ctrl-D` or `ctrl-C`.

#Features
* Built-in types: integer, float, bool, string, symbol, and list
* Scheme-like define syntax
* Tail-call optimization
* Parentheses-aware REPL

#Canonical Example

    ;; Applications in tail position will execute in
    ;; constant stack space
    (define (factorial n)
        (define (loop acc x)
            (if (< x 2)
                acc
                (loop (* x acc) (- x 1))))
        (loop 1 n))

    ;; Nicer to use a fold
    (define (factorial^ n)
        (foldl * 1 (range 1 n)))

    ;; Even better if the library expects such a thing
    (define (factorial^^ n)
        (product (range 1 n)))

    (print (factorial   10))
    (print (factorial^  10))
    (print (factorial^^ 10))

#Credits
* Originally a port of the Common Lisp meta-circular evaluator in [Dr. Raphael Finkel's](http://www.cs.uky.edu/~raphael/) book ["Advanced Programming Language Design"](http://www.amazon.com/dp/0805311912).
* Figured out tail-call optimization by reading Peter Norvig's ["(An ((Even Better) Lisp) Interpreter (in Python))"](http://norvig.com/lispy2.html).

#Miscellaneous
Requires the [pyparsing](http://sourceforge.net/projects/pyparsing/) library.

Released under the [MIT License](http://opensource.org/licenses/MIT).

