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

        self.create_bitwidth()
        self.create_bv_mod_constants()
        self.add_bv_starting_assertion()
        self.process_bv_mod()

    def create_bitwidth(self):
        def count_mul_operands(expression):
            max_mul = 0
            # Search given expression
            if isinstance(expression, list):
                if expression[0] == "*":
                    max_mul = len(expression) - 1 # subtract 1 for operator
                # Recursively search all children in the expression
                for child in expression[1:]:
                    max_mul = max(max_mul, count_mul_operands(child))
            return max_mul
        
        def calculate_bitwidth(w):
            if self.primes.prime == 2:
                return 2

            # Problem is non-linear
            if w < 2:
                w = 2

            # Use 64-bit or multi-precision integers
            if math.ceil(math.log2(self.primes.prime-1)) * w >= 32:
                raise ValueError(
                    "Bitwidth too small for 32-bit integer representation. " \
                    "Use 64-bit or multi-precision integers."
                )

            # Work out the largest number that can be computed under modulo p
            largest_number = 1
            for i in range(w):
                largest_number *= (self.primes.prime-1)

            for b in range(31): # 32-1
                largest_representable = (1 << b) - 1
                if largest_number <= largest_representable:
                    return b

            raise ValueError(
                "Bitwidth too small for 32-bit integer representation. " \
                "Use 64-bit or multi-precision integers."
            )
        
        # Find largest number of multiplication operands from all assertions (w)
        w = 0
        for command in self.ast:
            if isinstance(command, list) and command[0] == "assert":
                # Search all expressions in the assertion
                w = max(w, count_mul_operands(command[1]))
        print(f"w: {w}")

        self.bitwidth.n = calculate_bitwidth(w)
        self.primes.prime_bv = self.utility.handle_bv_integer(str(self.primes.prime))
        # Create a bit-vector type of width n
        self.bitwidth.n_sort = self.API.tm.mkBitVectorSort(self.bitwidth.n)
        print(f"Bitwidth: {self.bitwidth.n}")

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
            term = self.utility.create_bv_mod_term(operator, operands)

            # For all operations other than equals, wrap with mod p
            if operator == "=":
                return term
            else:
                return self.API.mod_solver.mkTerm(Kind.BITVECTOR_UREM, term, self.primes.prime_bv)
            