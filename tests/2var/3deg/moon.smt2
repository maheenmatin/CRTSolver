; 2x^3 + 2x = 364
; 10y - 1 = 69
; 2x^2 + 3x = 56
; 3y^3 - 11 = 67

(declare-const x Int)
(declare-const y Int)

(assert (= (+ (* 2 x x x) (* 2 x)) 364))
(assert (= (+ (* 10 y) -1) 69))
(assert (= (+ (* 2 x x) (* 3 x)) 56))
(assert (= (+ (* 3 y y y) -11) 67))
