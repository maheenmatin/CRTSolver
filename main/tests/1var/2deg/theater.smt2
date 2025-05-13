; -2x^2 - 6 = 0

(declare-const x Int)
(assert (= (+ (* -2 x x) (* 0 x) -6) 0))
(check-sat)
