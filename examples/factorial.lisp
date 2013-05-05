(define (factorial n)
    (product (range 1 n)))

(define (run)
    (print "Enter a number (^D to quit)")
    (let [(x (read))]
           (if (number? x)
                (begin
                    (print "factorial" x "is" (factorial x))
                    (run))
                (begin
                    (print x "is not a number")
                    (run)))))

(run)

