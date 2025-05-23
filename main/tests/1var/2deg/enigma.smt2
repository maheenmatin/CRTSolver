; x^2 + 2x + 8 = 71
; 3x + 9 = 30
; 5x^2 - 66 = 179

(declare-const x Int)

(assert (= (+ (* x x) (* 2 x) 8) 71))
(assert (= (+ (* 3 x) 9) 30))
(assert (= (+ (* 5 x x) -66) 179))
