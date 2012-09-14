#zeta is a small lisp evaluator written in Python 3.

I thought 'lispy' would a reasonably whimsical and Pythonic name, but
Google said that someone else was using it. Since 'larry' has a small edit
distance from 'lispy', I tried that next, but I couldn't take an
interpreter named 'larry' very seriously. I settled on 'zeta' because it
looks cool and can be written as Z when brevity is so important that I
don't have time to type three more letters (this happens infrequently).
Still difficult to take seriously, which is why one probably shouldn't.

#Running
To start the interpreter, run 'python zeta.py'. By default, the interpreter
runs as a read-evaluate-print loop. However, one can use file redirection
to execute a script non-interactively:

`python zeta < script.lisp`

The interpreter adjusts to avoid printing unnecessary prompts.

To see what names are defined in the global environment, type `(help)` at
the prompt.

To exit interactive mode, type `ctrl-D` or `ctrl-C`.

Requires the [pyparsing](http://sourceforge.net/projects/pyparsing/) library.

No warranties, guarantees, etc. You know the drill.

