; x^2 - 2y + 3 = z
; 10y - 3z - 2 = 37
; 2x^2 - 6y + x + z = z
; y^2 - 2z^2 = -62
; x=4, y=6, z=7

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)

(assert (= (+ (* x x) (* -2 y) 3) z))
(assert (= (+ (* 10 y) (* -3 z) -2) 37))
(assert (= (+ (* 2 x x) (* -6 y) x z) z))
(assert (= (+ (* y y) (* -2 z z)) -62))
