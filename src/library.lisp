;; Author: Christopher D. Parks
;; Email: chris.parks@uky.edu
;; Date: 4 December 2011
;; Class: CS655


;; Some useful lisp functions. zeta loads this on startup.

;; Returns a list containing the values start..stop (inclusive on both ends)
(define (range start stop)
    (if (> start stop)
        nil
        (cons start (range (1+ start) stop]

;; Applies the unary function `fn' to each element in the list `ls' and
;; collects the output in a list
(define (map fn ls)
    (if (null? ls)
        nil
        (cons (fn (car ls)) (map fn (cdr ls]

;; Filter list by keeping only elements where pred(element) is T
(define (filter pred ls)
    (cond
        ((null? ls) nil)
        ((pred (car ls)) (cons (car ls) (filter pred (cdr ls))))
        (T (filter pred (cdr ls]

;; Membership Test for item `x' in list `ls'
(define (contains x ls)
    (not (null? (filter (lambda (y)(= x y)) ls]

;; Find 1-based position of item `x' in list `ls' or NIL
(define (find x ls)
    (define (loop count rest)
        (cond
            ((null? rest) nil)
            ((= x (car rest)) count)
            (T (loop (1+ count) (cdr rest)))))
    (loop 1 ls]

;; Use the specified binary function `fn' to reduce the list `ls' to a single
;; value. An initial value is required.
(define (reduce fn initial ls)
    (if (null? ls)
        initial
        (fn (car ls) (reduce fn initial (cdr ls]

;; Turn two lists into a single list of pairs. The length of the output list
;; is the same as the shortest input list.
(define (zip l1 l2)
    (if (or (null? l1) (null? l2))
        nil
        (cons (list (car l1) (car l2)) (zip (cdr l1) (cdr l2]

;; Return the length of a list. Not a "deep" length.
(define (length ls)
    (if (null? ls)
        0
        (1+ (length (cdr ls]

;; Return the sublist of `ls' by skipping the first `n' elements
(define (drop n ls)
    (cond
        ((and (null? ls) (/= n 0)) (error "Accessed beyond end of list"))
        ((or (null? ls) (= n 0)) ls)
        (T (drop (1- n) (cdr ls]

;; Return the sublist of `ls' made up of the first `n' elements
(define (take n ls)
    (cond
        ((and (null? ls) (/= n 0)) (error "Accessed beyond end of list"))
        ((or (null? ls) (= n 0)) nil)
        (T (cons (car ls) (take (1- n) (cdr ls]

;; Return the `n'th element of a list `ls'
(define (list-ref n ls)
    (cond
        ((null? ls) (error "Accessed beyond end of list"))
        ((= n 1) (car ls))
        (T (list-ref (1- n) (cdr ls]

;; Reverse a list `ls'
(define (reverse ls)
    (if (null? ls)
        nil
        (append (reverse (cdr ls)) (cons (car ls) nil]

;; Accumulate `ls' with +
(define (sum ls)
    (reduce + 0 ls))

;; Accumulate `ls' with *
(define (product ls)
    (reduce * 1 ls))

;; Maximum element in list `ls'
(define (max ls)
    (define (selector fn)
        (lambda (x y)
            (if (fn x y) x y)))
    (reduce (selector >) (car ls) (cdr ls]

;; Minimum element in list `ls'
(define (min ls)
    (define (selector fn)
        (lambda (x y)
            (if (fn x y) x y)))
    (reduce (selector <) (car ls) (cdr ls]

;; Euclid's Algorithm for greatest common divisor
(define (gcd x y)
    (if (= y 0)
        x
        (gcd y (mod x y]
