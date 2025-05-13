; 60a^5 + 34b^4 + 27c^3 + 18d^2 + 51e + 1 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 60 a a a a a)
        (* 34 b b b b)
        (* 27 c c c)
        (* 18 d d)
        (* 51 e)
        1
    )
    0
))

(check-sat)
