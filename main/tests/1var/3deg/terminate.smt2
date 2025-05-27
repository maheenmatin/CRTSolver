; x^3 + 2x + 8 = 71
; 3x + 1 = 22
; 7x^3 - 65 = 207

(declare-const x Int)

(assert (= (+ (* x x x) (* 2 x) 8) 71))
(assert (= (+ (* 3 x) 1) 22))
(assert (= (+ (* 7 x x x) -65) 207))
