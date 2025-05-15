; 11a^4 + 23b^4 + 17c^4 + 49d^4 - 251 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)

(assert (= 
    (+ 
        (* 11 a a a a)
        (* 23 b b b b)
        (* 17 c c c c)
        (* 49 d d d d)
        -251
    )
    0
))
