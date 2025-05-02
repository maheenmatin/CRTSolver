; (x+3) (x+4) = 0

(declare-const x Int)
(assert (= (* (+ x 3) (+ x 4)) 0))
(check-sat)
