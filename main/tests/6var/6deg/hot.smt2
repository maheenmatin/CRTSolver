; 15a^6 + 25b^5 + 35c^4 + 45d^6 + 55e^3 + 65f^2 = 1000000

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 15 a a a a a a)
        (* 25 b b b b b)
        (* 35 c c c c)
        (* 45 d d d d d d)
        (* 55 e e e)
        (* 65 f f)
    )
    1000000
))
