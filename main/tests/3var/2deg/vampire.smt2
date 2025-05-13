; (2x+2)^2 + (3y-5)^2 = z

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(assert (= (+ (* (+ (* 2 x) 2) (+ (* 2 x) 2)) (+ (* 3 y) -5) (+ (* 3 y) -5)) z))
(check-sat)
