; 18a^4 - 76b^3 + 59c^2 + 44d + 2e - 5 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 18 a a a a)
        (* -76 b b b)
        (* 59 c c)
        (* 44 d)
        (* 2 e)
        -5
    )
    0
))

(check-sat)
