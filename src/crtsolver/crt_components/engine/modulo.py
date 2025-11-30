import cvc5
from cvc5 import Kind
import math

class Modulo:
    def __init__(self, ast, API, terms, primes, utility):
        self.ast = ast
        self.API = API
        self.terms = terms
        self.primes = primes
        self.utility = utility

    def compute_mod(self):
        self.primes.prime_int = self.utility.handle_integer(str(self.primes.prime))
        self.create_mod_constants()
        self.add_starting_assertion()
        self.process_mod()

    def create_mod_constants(self):
        sort = self.API.tm.getIntegerSort()
        for name in self.terms.vars:
            # Create constant and add to dictionary
            mod_name = f"{name}_mod_{self.primes.prime}"
            mod_const = self.API.tm.mkConst(sort, mod_name)
            self.terms.mod_vars[mod_name] = mod_const

    def add_starting_assertion(self):
        # ensures only constants for current prime are used
        suffix = f"_mod_{self.primes.prime}"
        for name in self.terms.mod_vars:
            if name.endswith(suffix):
                # Assert that each constant is less than prime
                constraint = self.utility.create_mod_term(
                    "<", [self.terms.mod_vars[name], self.primes.prime_int]
                )
                self.API.mod_solver.assertFormula(constraint)

    def process_mod(self):
        # assertions are not reset - new modulo p assertions added each time
        for subtree in self.ast:
            # Process each assert command within context of modulo prime
            if subtree[0] == "assert":
                constraint = self.process_mod_constraint(subtree[1])
                self.API.mod_solver.assertFormula(constraint)

    def process_mod_constraint(self, subtree):
        # leaf node = string
        # subtree = list
        if (isinstance(subtree, str)):
            if subtree in self.terms.vars:
                return self.terms.mod_vars[
                    f"{subtree}_mod_{self.primes.prime}"] # return mod_p equivalent
            else:
                num_term = self.utility.handle_integer(subtree)
                return self.API.mod_solver.mkTerm(Kind.INTS_MODULUS, num_term, self.primes.prime_int)
        else:
            # Call process_modulo_constraint for all operands (depth-first traversal)
            operator = subtree[0]
            operands = [self.process_mod_constraint
                (operand) for operand in subtree[1:]]
            term = self.utility.create_mod_term(operator, operands)

            # For all operations other than equals, wrap with mod p
            if operator == "=":
                return term
            else:
                return self.API.mod_solver.mkTerm(Kind.INTS_MODULUS, term, self.primes.prime_int)
