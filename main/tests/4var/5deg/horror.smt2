; 13a^5 + 29b^5 + 17c^5 + 42d^5 - 1000 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)

(assert (= 
    (+ 
        (* 13 a a a a a)
        (* 29 b b b b b)
        (* 17 c c c c c)
        (* 42 d d d d d)
        -1000
    )
    0
))

(check-sat)
