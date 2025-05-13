; 2x^3 - 3y^3 = 9

(declare-const x Int)
(declare-const y Int)
(assert (= (- (* 2 x x x) (* 3 y y y)) 9))
(check-sat)
