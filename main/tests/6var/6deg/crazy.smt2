; 18a^6 + 32b^6 + 20c^6 + 24d^5 + 56e^4 + 36f^3 = -500000

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 18 a a a a a a)
        (* 32 b b b b b b)
        (* 20 c c c c c c)
        (* 24 d d d d d)
        (* 56 e e e e)
        (* 36 f f f)
    )
    -500000
))

(check-sat)
