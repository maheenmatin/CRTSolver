; 45a^5 + 12b^3 - 36c^2 + 27d - 64e - 152 = 0

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const e Int)

(assert (= 
    (+ 
        (* 45 a a a a a)
        (* 12 b b b)
        (* -36 c c)
        (* 27 d)
        (* -64 e)
        -152
    )
    0
))
