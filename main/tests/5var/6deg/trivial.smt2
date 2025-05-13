; 12a^6 + 45b^5 + 23c^4 + 67d^3 + 89e^2 + 52 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 12 a a a a a a)
        (* 45 b b b b b)
        (* 23 c c c c)
        (* 67 d d d)
        (* 89 e e)
        52
    )
    0
))

(check-sat)
