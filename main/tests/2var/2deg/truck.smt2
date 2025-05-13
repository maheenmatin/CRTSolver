; (x+2) (x-1) + (y-7) (y+4) = 0

(declare-const x Int)
(declare-const y Int)
(assert (= (+ (* (+ x 2) (+ x -1)) (* (+ y -7) (+ y 4))) 0))
(check-sat)
