; 15a^6 + 28b^5 + 19c^4 + 63d^3 + 80e^2 + 300 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 15 a a a a a a)
        (* 28 b b b b b)
        (* 19 c c c c)
        (* 63 d d d)
        (* 80 e e)
        300
    )
    0
))

(check-sat)
