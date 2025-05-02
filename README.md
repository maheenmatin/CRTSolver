An outline of the program:

1. Parse the input equations into your internal representation.

2. Pick a prime that you haven't used so far, call it p.

3. Generate a copy of the equations that are modulo p and add them to
the solver.

4. Run the solver.

5. A. If the solver says UNSAT then the whole problem is UNSAT and you
are done and can return UNSAT.

5. B. If the solver says SAT then it might all be SAT or maybe you
haven't used enough primes yet.

6. Use the solution from the solver to compute a candidate solution to
the original problem.

7. Try it.  If it works then the original problem is SAT and you can
return SAT.  If it doesn't then you need another prime, so go back to
step 2.

Credits: Martin Nyx Brain
