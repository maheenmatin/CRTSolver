; 7a^4 + 13b^4 + 25c^4 + 38d^4 + 41e^4 + 56f^4 = 300

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)
(declare-const f Int)

(assert (= 
    (+ 
        (* 7 a a a a)
        (* 13 b b b b)
        (* 25 c c c c)
        (* 38 d d d d)
        (* 41 e e e e)
        (* 56 f f f f)
    )
    300
))
