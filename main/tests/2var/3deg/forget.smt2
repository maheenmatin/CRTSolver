; 3x^3 + 2y^3 - 11xy = -47

(declare-const x Int)
(declare-const y Int)
(assert (= (+ (* 3 x x x) (* 2 y y y) (* -11 x y)) -47))
(check-sat)
