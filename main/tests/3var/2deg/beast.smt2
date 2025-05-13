; (x-3)^2 + (y+6)^2 = z

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(assert (= (+ (* (+ x -3) (+ x -3)) (* (+ y 6) (+ y 6))) z))
(check-sat)
