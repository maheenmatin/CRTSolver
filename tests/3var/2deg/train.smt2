; x^2 - 2y = z
; 10y - 3z = 157
; 2x^2 - 6y = -16
; y^2 - 2z^2 = 119
; x=7, y=19, z=11

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)

(assert (= (+ (* x x) (* -2 y)) z))
(assert (= (+ (* 10 y) (* -3 z)) 157))
(assert (= (+ (* 2 x x) (* -6 y)) -16))
(assert (= (+ (* y y) (* -2 z z)) 119))
