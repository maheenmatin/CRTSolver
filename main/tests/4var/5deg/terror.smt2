; 21a^5 + 4b^4 - 13c^5 - 42d^4 - 512 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)

(assert (= 
    (+ 
        (* 21 a a a a a)
        (* 4 b b b b)
        (* -13 c c c c c)
        (* -42 d d d d)
        -512
    )
    0
))

(check-sat)
