; 15a^5 + 25b^4 + 35c^3 + 45d^5 + 55e^2 + 65f^4 = 2000

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 15 a a a a a)
        (* 25 b b b b)
        (* 35 c c c)
        (* 45 d d d d d)
        (* 55 e e)
        (* 65 f f f f)
    )
    2000
))

(check-sat)
