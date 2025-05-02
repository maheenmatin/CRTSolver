; 13(x-1)^3 + 3(y-11)^3 + 17(z+19)^3 = -101

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(assert (= (+ (* 13 (+ x -1) (+ x -1) (+ x -1)) (* 3 (+ y -11) (+ y -11) (+ y -11)) (* 17 (+ z 19) (+ z 19) (+ z 19))) -101))
(check-sat)
