; 25a^4 + 32b^3 + 61c^2 + 18d + 2e + 1 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 25 a a a a)
        (* 32 b b b)
        (* 61 c c)
        (* 18 d)
        (* 2 e)
        1
    )
    0
))
