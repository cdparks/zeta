#zeta is a small lisp evaluator written in Python. 

I thought 'lispy' would a reasonably whimsical and Pythonic name, but
Google said that someone else was using it. Since 'larry' has a small edit
distance from 'lispy', I tried that next, but I couldn't take an
interpreter named 'larry' very seriously. I settled on 'zeta' because it
looks cool and can be written as Z when brevity is so important that I
don't have time to type three more letters (this happens infrequently).

#Running
To start the interpreter, run 'python zeta.py'. By default, the interpreter 
runs as a read-evaluate-print loop. However, one can use file redirection 
to execute a script non-interactively:

`python zeta < script.lisp`

The interpreter adjusts to avoid printing unnecessary prompts.

For help at the prompt, type `help`.

To exit interactive mode, type `ctrl-D` or `ctrl-C`.
