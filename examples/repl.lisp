(define (repl)
    (print (eval (read)))
    (repl))

(print "Starting repl (^D to quit)")
(repl)

