; (x-4)^3 + (y+5)^3 = z

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(assert (= (+ (* (+ x -4) (+ x -4) (+ x -4)) (* (+ y 5) (+ y 5) (+ y 5)) ) z))
