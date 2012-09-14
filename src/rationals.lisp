;; Define a rational as a list of two integers.
(define (rational n d)
    (if (= d 0)
        (error "Denominator cannot be zero")
        (let ([g (gcd n d)]
              [rn (// n g)]
              [rd (// d g)])
        (if (< rd 0)
            (list (~ rn) (~ rd))
            (list rn rd)))))

;; Get numerator
(define (numerator rational)
    (car rational))

;; Get denominator
(define (denominator rational)
    (car (cdr rational)))

;; Arithmetic operators
(define (rational+ x y)
    (let ([dx (denominator x)]
          [dy (denominator y)]
          [nx (numerator x)]
          [ny (numerator y)]
          [new-d (* dx dy)]
          [new-n (+ (* nx dy) (* dx ny))])
    (rational new-n new-d)))

(define (rational~ x)
    (rational (~ (numerator x)) (denominator x)))

(define (rational- x y)
    (rational+ x (rational~ y)))

(define (rational* x y)
    (let ([dx (denominator x)]
          [dy (denominator y)]
          [nx (numerator x)]
          [ny (numerator y)])
    (rational (* nx ny) (* dx dy))))

(define (rational/ x y)
    (rational* x (rational (denominator y) (numerator y))))

;; Comparisons
(define (rational< x y)
    (let ([dx (denominator x)]
          [dy (denominator y)]
          [nx (numerator x)]
          [ny (numerator y)])
    (< (* nx dy) (* dx ny))))

(define (rational= x y)
    (and (not (rational< x y)) (not (rational< y x))))

(define (rational> x y)
    (and (not (rational< x y)) (rational< y x)))

(define (rational<= x y)
    (or (rational< x y) (rational= x y)))

(define (rational>= x y)
    (or (rational> x y) (rational= x y)))

;; Conversions
(define (rational->float x)
    (/ (numerator x) (denominator x)))

(define (rational->int x)
    (// (numerator x) (denominator x)))

