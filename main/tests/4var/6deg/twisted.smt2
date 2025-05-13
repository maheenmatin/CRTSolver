; 41a^6 + 35b^5 + 19c^4 + 27d^3 + 23e^2 + 1 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 41 a a a a a a)
        (* 35 b b b b b)
        (* 19 c c c c)
        (* 27 d d d)
        (* 23 e e)
        1
    )
    0
))

(check-sat)
