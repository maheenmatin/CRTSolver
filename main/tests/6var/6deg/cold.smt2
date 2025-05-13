; 10a^6 + 20b^5 + 30c^4 + 40d^6 + 50e^3 + 60f^2 = 50000

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 10 a a a a a a)
        (* 20 b b b b b)
        (* 30 c c c c)
        (* 40 d d d d d d)
        (* 50 e e e)
        (* 60 f f)
    )
    50000
))

(check-sat)
