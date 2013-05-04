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
(test "4. (+ 1 2 3)" (+ 1 2 3) 6)
(test "5. (* 2 3 4)" (* 2 3 4) 24)

;; And/Or forms
(test "6. (or #f #f)" (or #f #f) #f)
(test "7. (or #f #t)" (or #f #t) #t)
(test "8. (or #t #f)" (or #t #f) #t)
(test "9. (or #t #t)" (or #t #t) #t)
(test "10. (and #f #f)" (and #f #f) #f)
(test "11. (and #f #t)" (and #f #t) #f)
(test "12. (and #t #f)" (and #t #f) #f)
(test "13. (and #t #t)" (and #t #t) #t)

;; Cond form 
(test "14. (cond (#f 1) (#f 2))" (cond (#f 1) (#f 2)) nil)
(test "15. (cond (#f 1) (#t 2))" (cond (#f 1) (#t 2)) 2)
(test "16. (cond (#t 1) (#f 2))" (cond (#t 1) (#f 2)) 1)
(test "17. (cond (#t 1) (#t 2))" (cond (#t 1) (#t 2)) 1)

;; Let form
(test "18. (let ((x 10) (y 12)) (+ x y))" (let ((x 10) (y 12)) (+ x y)) 22)
(test "19. (let ((f (lambda (x) (* x x))) (x 12)) (f x))" (let ((f (lambda (x) (* x x))) (x 12)) (f x)) 144)


;; Function definition and deep binding	
(test "20. Deep binding"
	(((lambda (x)
		(lambda (y)
			(list x y))) 3) 4)
    (list 3 4))

(define (factorial n)
	(if (< n 2)
		1
		(* n (factorial (-- n)))))
(test "21. define factorial, (factorial 10)" (factorial 10) 3628800)

;; Multi-expression defines
(define (tail-factorial n)
	(define (loop acc x)
		(if (< x 2)
			acc
			(loop (* x acc) (- x 1))))
	(loop 1 n))

(test "22. define tail-recursive factorial, (factorial 10)" (tail-factorial 10) (factorial 10))

(print "Basic Tests completed")

