;; Compare evaluated expression to expected
(define (test name expression expected)
	(print name "->" expression)
	(if (= expression expected)
		nil
		(print "FAILED!")))

;; Primitive operations
(test "1. car" (car (cons 1 (cons 2 nil))) 1)
(test "2. cdr" (cdr (cons 1 (cons 2 nil))) (list 2))
(test "3. cons" (cons 1 (cons 2 (cons 3 nil))) (list 1 2 3))

;; Function definition and deep binding	
(test "4. Deep binding"
	(((lambda (x)
		(lambda (y)
			(list x y))) 3) 4)
    (list 3 4))

(define (factorial n)
	(if (< n 2)
		1
		(* n (factorial (-- n)))))
(test "5. factorial 10" (factorial 10) 3628800)

;; Library functions
(define (square x)(* x x))
(test "6. range 1..10" (range 1 10) '(1 2 3 4 5 6 7 8 9 10))
(test "7. map square over 1..5" (map square (range 1 5)) '(1 4 9 16 25))
(test "8. reduce add over 1..10" (reduce + 0 (range 1 10)) 55)
(test "9. reverse 1..10" (reverse (range 1 10)) '(10 9 8 7 6 5 4 3 2 1))

;; Multi-expression defines (tail call optimization is not implemented yet).
(define (tail-factorial n)
	(define (iter out remainder)
		(if (< remainder 2)
			out
			(iter (* remainder out) (- remainder 1))))
	(iter 1 n))

(define (tail-range start stop)
	(define (iter out end)
		(if (< end start)
			out
			(iter (cons end out) (- end 1))))
	(iter nil stop))
(test "10. tail-factorial 10" (tail-factorial 10) (factorial 10))
(test "11. tail-range 1..10" (tail-range 1 10) (range 1 10))

(print "Tests completed")

