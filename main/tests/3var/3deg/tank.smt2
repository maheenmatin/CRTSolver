; (x+7)^3 + (y-9)^3 = z

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(assert (= (+ (* (+ x 7) (+ x 7) (+ x 7)) (* (+ y -9) (+ y -9) (+ y -9)) ) z))
(check-sat)
