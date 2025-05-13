; x^3 + y^3 = -3

(declare-const x Int)
(declare-const y Int)
(assert (= (+ (* x x x) (* y y y)) -3))
(check-sat)
