import cvc5
from cvc5 import Kind
import crt_components.errors.error as error

class Utility:
    def __init__(self, API, terms, primes, bitwidth, main):
        self.API = API
        self.terms = terms
        self.primes = primes
        self.bitwidth = bitwidth
        self.main = main
        self.operator_mapping = {
            "=": Kind.EQUAL,
            "+": Kind.ADD,
            "-": Kind.SUB,
            "*": Kind.MULT,
            ">": Kind.GT,
            "<": Kind.LT,
            ">=": Kind.GEQ,
            "<=": Kind.LEQ
        }
        self.bv_operator_mapping = {
            "=": Kind.EQUAL,
            "+": Kind.BITVECTOR_ADD,
            "-": Kind.BITVECTOR_SUB,
            "*": Kind.BITVECTOR_MULT,
            ">": Kind.BITVECTOR_UGT, # unsigned greater than
            "<": Kind.BITVECTOR_ULT,
            ">=": Kind.BITVECTOR_UGE,
            "<=": Kind.BITVECTOR_ULE
        }

    def create_term(self, operator, operands):
        return self.API.solver.mkTerm(self.operator_mapping[operator], *operands)
    
    def create_mod_term(self, operator, operands):
        return self.API.mod_solver.mkTerm(self.operator_mapping[operator], *operands)
    
    def create_bv_mod_term(self, operator, operands):
        return self.API.mod_solver.mkTerm(self.bv_operator_mapping[operator], *operands)
        
    def handle_integer(self, num):  
        try: 
            if num in self.terms.ints: # if num already exists
                return self.terms.ints[num]
            else:     
                num_term = self.API.tm.mkInteger(int(num)) # convert string to integer
                self.terms.ints[num] = num_term # add to dictionary
                return num_term
        except OverflowError:
            raise error.AbortFileException(num)
        
    def handle_bv_mod_const(self, const):
        # Return equivalent constant for mod p
        mod_name = f"{const}_mod_{self.primes.prime}"

        if mod_name in self.terms.bv_mod_vars: # if equivalent constant already exists
            return self.terms.bv_mod_vars[mod_name]
        else:
            #print(f"Making constant {mod_name}")
            new_const = self.API.tm.mkConst(self.bitwidth.n_sort, mod_name)
            self.terms.bv_mod_vars[mod_name] = new_const
            return new_const
        
    def handle_bv_integer(self, num):
        if num in self.terms.bv_ints:
            return self.terms.bv_ints[num]
        else:
            # Represent as bitvector of width n     
            num_term = self.API.tm.mkBitVector(self.bitwidth.n, int(num))
            self.terms.bv_ints[num] = num_term
            return num_term
