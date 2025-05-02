; (x-9) (x+1) (x-6) = 0

(declare-const x Int)
(assert (= (* (+ x -9) (+ x 1) (+ x -6)) 0))
(check-sat)
