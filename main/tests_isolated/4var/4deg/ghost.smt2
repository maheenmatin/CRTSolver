; 3a^4 + 5b^3 - 23c^4 + 56d^2 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)

(assert (= 
    (+ 
        (* 3 a a a a)
        (* 5 b b b)
        (* -23 c c c c)
        (* 56 d d)
    )
    0
))
