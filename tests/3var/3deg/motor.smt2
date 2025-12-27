; x^2 - 2y = z
; 10y - 3z^3 = 157
; 2x^2 - 6y = -16
; 3y^3 - 2z^2 = x

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)

(assert (= (+ (* x x) (* 2 y)) z))
(assert (= (+ (* 10 y) (* -3 z z z)) 157))
(assert (= (+ (* 2 x x) (* 63 y)) -16))
(assert (= (+ (* y y y) (* -2 z z)) x))
