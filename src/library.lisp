;; Some useful lisp functions. zeta loads this on startup.

;; Reverse a list `ls'
(define (reverse ls)
    (define (loop acc x)
        (if (null? x)
            acc
            (loop (cons (car x) acc) (cdr x))))
    (loop nil ls))

;; Returns a list containing the values start..stop (inclusive on both ends)
(define (range start stop)
    (define (loop acc x)
        (if (< x start)
            acc
            (loop (cons x acc) (-- x))))
    (loop nil stop))

;; Applies the unary function `fn' to each element in the list `ls' and
;; collects the output in a list
(define (map f ls)
    (define (step acc x)
        (cons (f x) acc))
    (reverse (foldl step nil ls)))

;; Filter list by keeping only elements where pred(element) is #t
(define (filter pred ls)
    (define (step acc x)
        (if (pred x)
            (cons x acc)
            acc))
    (reverse (foldl step nil ls)))

;; Membership Test for item `x' in list `ls'
(define (contains x ls)
    (not (null? (filter (lambda (y) (= x y)) ls))))

;; Find 1-based position of item `x' in list `ls' or NIL
(define (find x ls)
    (define (loop count rest)
        (cond
            ((null? rest) nil)
            ((= x (car rest)) count)
            (#t (loop (++ count) (cdr rest)))))
    (loop 1 ls))

;; Use the specified binary function `fn' to reduce the list `ls' to a single
;; value. An initial value is required.
(define (foldl f init ls)
    (define (loop acc x)
        (if (null? x)
            acc
            (loop (f acc (car x)) (cdr x))))
    (loop init ls))

;; Turn two lists into a single list of pairs. The length of the output list
;; is the same as the shortest input list.
(define (zip l1 l2)
    (define (loop acc x1 x2)
        (if (or (null? x1) (null? x2))
            acc
            (loop (cons (list (car x1) (car x2)) acc) (cdr x1) (cdr x2))))
    (reverse (loop nil l1 l2)))

;; Return the length of a list.
(define (length ls)
    (foldl (lambda (x _) (++ x)) 0 ls))

;; Return the sublist of `ls' by skipping the first `n' elements
(define (drop n ls)
    (cond
        ((or (null? ls) (= n 0)) ls)
        (#t (drop (-- n) (cdr ls)))))

;; Return the sublist of `ls' made up of the first `n' elements
(define (take n ls)
    (define (loop acc count x)
        (cond
            ((or (null? x) (= count n)) acc)
            (#t (loop (cons (car x) acc) (++ count) (cdr x)))))
    (reverse (loop nil 0 ls)))

;; Return the `n'th element of a list `ls'
(define (list-ref n ls)
    (cond
        ((null? ls) (error "Accessed beyond end of list"))
        ((= n 1) (car ls))
        (#t (list-ref (-- n) (cdr ls)))))

;; Accumulate `ls' with +
(define (sum ls)
    (foldl + 0 ls))

;; Accumulate `ls' with *
(define (product ls)
    (foldl * 1 ls))

;; Maximum element in list `ls'
(define (max ls)
    (define (selector fn)
        (lambda (x y)
            (if (fn x y) x y)))
    (foldl (selector >) (car ls) (cdr ls)))

;; Minimum element in list `ls'
(define (min ls)
    (define (selector fn)
        (lambda (x y)
            (if (fn x y) x y)))
    (foldl (selector <) (car ls) (cdr ls)))

;; Euclid's Algorithm for greatest common divisor
(define (gcd x y)
    (if (= y 0)
        x
        (gcd y (mod x y))))

;; Operations for ational numbers
(load "src/rationals.lisp")

