;; Compare evaluated expression to expected
(define (test name expression expected)
	(print name "->" expression)
	(if (= expression expected)
		nil
		(print "FAILED!")))


(define (square x) (* x x))
(define (even x) (= 0 (mod x 2)))
(define ls '(1 2 3 4 5))

;; Library functions
(test "1. reverse 1..5" (reverse ls) '(5 4 3 2 1))
(test "2. range 1..5" (range 1 5) ls)
(test "3. map square 1..5" (map square ls) '(1 4 9 16 25))
(test "4. filter even 1..5" (filter even ls) '(2 4))
(test "5. contains 4 1..5" (contains 4 ls) #t)
(test "5. contains 7 1..5" (contains 7 ls) #f)
(test "6. find 4 1..5" (find 4 ls) 4)
(test "7. find 7 1..5" (find 7 ls) nil)
(test "8. foldl + 0 1..5" (foldl + 0 ls) 15)
(test "8. foldl * 1 1..5" (foldl * 1 ls) 120)
(test "9. zip 1..5 1..5" (zip ls ls) '((1 1) (2 2) (3 3) (4 4) (5 5)))
(test "10. zip 1..5 1..3" (zip ls '(1 2 3)) '((1 1) (2 2) (3 3)))
(test "11. zip 1..3 1..5" (zip '(1 2 3) ls) '((1 1) (2 2) (3 3)))
(test "12. length 1..5" (length ls) 5)
(test "13. drop 1 1..5" (drop 1 ls) '(2 3 4 5))
(test "14. take 1 1..5" (take 1 ls) '(1))
(test "15. list-ref 1 1..5" (list-ref 1 ls) 1)
(test "16. list-ref 5 1..5" (list-ref 5 ls) 5)
(test "17. sum 1..5" (sum ls) 15)
(test "18. product 1..5" (product ls) 120)
(test "19. max 1..5" (max ls) 5)
(test "20. min 1..5" (min ls) 1)
(test "21. gcd 100 8" (gcd 100 8) 4)

(print "Library tests completed")
