; 33a^6 + 12b^5 + 17c^4 + 44d^3 + 25e^2 - 20284 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 33 a a a a a a)
        (* 12 b b b b b)
        (* 17 c c c c)
        (* 44 d d d)
        (* 25 e e)
        -20284
    )
    0
))

(check-sat)
