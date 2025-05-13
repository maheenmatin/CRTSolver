; 10a^5 + 20b^3 + 30c^4 + 40d^5 + 50e^2 + 60f^3 = 1000

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 10 a a a a a)
        (* 20 b b b)
        (* 30 c c c c)
        (* 40 d d d d d)
        (* 50 e e)
        (* 60 f f f)
    )
    1000
))

(check-sat)
