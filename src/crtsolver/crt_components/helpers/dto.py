from dataclasses import dataclass, field
import cvc5
from cvc5 import Kind

@dataclass
class API:
    time_limit: str = "30000" # init=False fields must come after regular fields
    tm: cvc5.TermManager = field(default_factory=cvc5.TermManager)
    # initialised in post_init
    solver: cvc5.Solver = field(init=False) # for candidate.py
    mod_solver: cvc5.Solver = field(init=False) # for modulo.py

    def __post_init__(self):
        self.solver = cvc5.Solver(self.tm)
        self.solver.setOption("produce-models", "true") # allows model retrieval
        self.solver.setOption("produce-unsat-cores", "true") # allows unsat core retrieval
        self.solver.setOption("tlimit-per", self.time_limit) # time limit for each check-sat
        self.solver.setLogic("QF_ALL")

        self.mod_solver = cvc5.Solver(self.tm)
        self.mod_solver.setOption("produce-models", "true")
        self.mod_solver.setOption("produce-unsat-cores", "true")
        self.mod_solver.setOption("tlimit-per", self.time_limit)
        self.mod_solver.setLogic("QF_ALL")

@dataclass
class Terms:
    # field(default_factory=dict) ensures that 
    # new dictionaries are created for every new instance of Terms
    vars: dict = field(default_factory=dict) # vars of int sort
    mod_vars: dict = field(default_factory=dict) # var_mod_p (int sort)
    ints: dict = field(default_factory=dict) # cvc5 ints
    bv_mod_vars: dict = field(default_factory=dict) # var_mod_p (bv sort)
    bv_ints: dict = field(default_factory=dict) # cvc5 integers with n bitwidth

@dataclass
class Primes:
    prime: int = field(default=None) # python int representation
    prime_int: cvc5.Term = field(default=None) # cvc5 int representation
    prime_bv: cvc5.Term = field(default=None) # cvc5 bv representation

@dataclass
class Bitwidth:
    n: int = field(default=None) # python int
    n_sort: cvc5.Sort = field(default=None) # bv sort with n bitwidth
