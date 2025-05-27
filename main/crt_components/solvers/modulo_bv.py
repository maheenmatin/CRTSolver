import cvc5
from cvc5 import Kind
import math

class Modulo_BV:
    def __init__(self, ast, API, terms, primes, bitwidth, utility):
        self.ast = ast
        self.API = API
        self.terms = terms
        self.primes = primes
        self.bitwidth = bitwidth
        self.utility = utility

    def compute_mod(self):
        # Reset bitvector dictionaries for current prime
        self.terms.bv_mod_vars.clear()
        self.terms.bv_ints.clear()

        # Find the smallest n such that 2^n >= p^2
        self.bitwidth.n = math.log2(self.primes.prime ** 2) # solve for n using n >= log2(p^2)
        self.bitwidth.n = math.ceil(self.bitwidth.n) # round up if necessary
        self.primes.prime_bv = self.utility.handle_bv_integer(str(self.primes.prime))
        # Create a bit-vector type of width n
        self.bitwidth.n_sort = self.API.tm.mkBitVectorSort(self.bitwidth.n)

        self.create_bv_mod_constants()
        self.add_bv_starting_assertion()
        self.process_bv_mod()

    def create_bv_mod_constants(self):
        for name in self.terms.vars:
            # Create constant and add to dictionary
            mod_name = f"{name}_mod_{self.primes.prime}"
            mod_const = self.API.tm.mkConst(self.bitwidth.n_sort, mod_name)
            self.terms.bv_mod_vars[mod_name] = mod_const

    def add_bv_starting_assertion(self):
        # ensures only constants for current prime are used
        suffix = f"_mod_{self.primes.prime}"
        for name in self.terms.bv_mod_vars:
            if name.endswith(suffix):
                # Assert that each constant is less than prime
                constraint = self.utility.create_bv_mod_term(
                    "<", [self.terms.bv_mod_vars[name], self.primes.prime_bv]
                )
                self.API.mod_solver.assertFormula(constraint)

    def process_bv_mod(self):
        # assertions are not reset - new modulo p assertions added each time
        for subtree in self.ast:
            if subtree[0] == "assert":
                # Process each assert command within context of modulo prime
                constraint = self.process_bv_mod_constraint(subtree[1])
                self.API.mod_solver.assertFormula(constraint)

    def process_bv_mod_constraint(self, subtree):
        # leaf node = string
        # subtree = list
        if (isinstance(subtree, str)):
            if subtree in self.terms.vars:
                return self.utility.handle_bv_mod_const(subtree) # return mod_p equivalent
            else:
                mod_term = int(subtree) % self.primes.prime
                return self.utility.handle_bv_integer(str(mod_term))
        else:
            # Call process_modulo_constraint for all operands (depth-first traversal)
            operator = subtree[0]
            operands = [self.process_bv_mod_constraint
                (operand) for operand in subtree[1:]]

            if operator == "*":
                # Special handling for multiplication - nesting required
                return self.process_mult(operands)
            else:
                term = self.utility.create_bv_mod_term(operator, operands)
                # For all operations other than equals, wrap with mod p
                if operator == "=":
                    return term
                else:
                    return self.API.mod_solver.mkTerm(Kind.BITVECTOR_UREM, term, self.primes.prime_bv)
                
    def process_mult(self, operands):
        # Raise assertion error if less than 2 operands
        assert len(operands) >= 2 

        # Create multiplication term with first two numbers, then apply mod p
        term = self.API.mod_solver.mkTerm(Kind.BITVECTOR_MULT, operands[0], operands[1])
        term = self.API.mod_solver.mkTerm(Kind.BITVECTOR_UREM, term, self.primes.prime_bv)

        # Create multiplication terms with remaining numbers, applying mod p for each additional number
        for operand in operands[2:]:
            term = self.API.mod_solver.mkTerm(Kind.BITVECTOR_MULT, term, operand)
            term = self.API.mod_solver.mkTerm(Kind.BITVECTOR_UREM, term, self.primes.prime_bv)
        
        return term
    