; 20a^5 + 30b^4 + 40c^3 + 50d^5 + 60e^2 + 70f^4 = -10000

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 20 a a a a a)
        (* 30 b b b b)
        (* 40 c c c)
        (* 50 d d d d d)
        (* 60 e e)
        (* 70 f f f f)
    )
    -10000
))
