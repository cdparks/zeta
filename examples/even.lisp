(define (even x)
    (cond [(< x 0) (odd (++ x))]
          [(> x 0) (odd (-- x))]
          [#t #t]))

(define (odd x)
    (cond [(< x 0) (even (++ x))]
          [(> x 0) (even (-- x))]
          [#t #f]))

(define (run)
    (print "Enter a number (^D to quit)")
    (let [(x (read))]
        (if (number? x)
            (begin
                (print "Even?" (even x))
                (run))
            (begin
                (print x "is not a number")
                (run)))))

(run)

