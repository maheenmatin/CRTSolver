; 8a^4 + 15b^4 + 27c^4 + 50d^4 + 63e^4 + 72f^4 = 1000

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 8 a a a a)
        (* 15 b b b b)
        (* 27 c c c c)
        (* 50 d d d d)
        (* 63 e e e e)
        (* 72 f f f f)
    )
    1000
))

(check-sat)
