; 4x^3 + 2y^3 = -31

(declare-const x Int)
(declare-const y Int)
(assert (= (+ (* 4 x x x) (* 2 y y y)) -31))
(check-sat)
