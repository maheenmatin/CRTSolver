; 2x^2 + 2x - 1 = 363
; 9y - 1 = 62
; x^2 - 4x = 117
; 5y^2 - 51 = 194
; x=13, y=7

(declare-const x Int)
(declare-const y Int)

(assert (= (+ (* 2 x x) (* 2 x) -1) 363))
(assert (= (+ (* 9 y) -1) 62))
(assert (= (+ (* x x) (* -4 x)) 117))
(assert (= (+ (* 5 y y) -51) 194))
