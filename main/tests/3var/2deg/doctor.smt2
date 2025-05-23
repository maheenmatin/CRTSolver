; x^2 + y = z
; 7y - 3z = 81
; 2x^2 - 6y = -8
; y^2 - 2z^2 = 56

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)

(assert (= (+ (* x x) y) z))
(assert (= (+ (* 7 y) (* -3 z)) 81))
(assert (= (+ (* 2 x x) (* -6 y)) -8))
(assert (= (+ (* y y) (* -2 z z)) 56))
