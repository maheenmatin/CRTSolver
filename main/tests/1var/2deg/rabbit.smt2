; (x-5) (x+1) = 0

(declare-const x Int)
(assert (= (* (+ x -5) (+ x 1)) 0))
(check-sat)
