; 3x^2 + x + 4 = 0

(declare-const x Int)
(assert (= (+ (* 3 x x) (* 1 x) 4) 0))
(check-sat)
