; (x+2)^2 + (y-9)^2 = -1

(declare-const x Int)
(declare-const y Int)
(assert (= (+ (* (+ x 2) (+ x 2)) (* (+ y -9) (+ y -9))) -1))
(check-sat)
