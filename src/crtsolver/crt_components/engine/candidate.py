import itertools
import cvc5
from cvc5 import Kind

class Candidate:
    def __init__(self, ast, API, terms, utility, main):
        self.ast = ast
        self.API = API
        self.terms = terms
        self.utility = utility
        self.main = main
        self.prime = 2
        self.mod_results = {} # {constant_name: (modulus, result)}

    def compute_candidate(self, candidate_list):
        # candidate_list = [(constant_name, modulus, result)]
        self.prime = candidate_list[0][1] # update prime

        # Create one candidate term for each 
        # These are the starting values for finding further candidates
        candidate_dict = {} # candidate_dict = {constant_name, integer_value}
        if self.mod_results: # mod 3 onwards
            for candidate in candidate_list:
                old_mod_result = self.mod_results[candidate[0]]
                new_mod_result = self.find_new_candidate((candidate[1], candidate[2]), old_mod_result)
                self.mod_results[candidate[0]] = new_mod_result
                candidate_dict[candidate[0]] = new_mod_result[1]
        else: # mod 2
            for candidate in candidate_list:
                self.mod_results[candidate[0]] = (candidate[1], candidate[2])
                candidate_dict[candidate[0]] = candidate[2]

        candidate_terms = self.populate_candidate_terms(candidate_dict)
        self.check_all_candidates(candidate_terms)

    def populate_candidate_terms(self, candidate_dict):
        # 2 constants, 2 build_candidates each = 2^2 = 4 total variations
        # 3 constants, 4 build_candidates each = 4^3 = 64 total variations

        # Construct Cartesian product of offsets (one list for each constant)
        offset_list = [0, -self.prime, self.prime, -(2*self.prime), 2*self.prime]
        offset_variations = list(itertools.product(offset_list, repeat=len(candidate_dict)))

        candidate_terms = []

        # Construct lists of all possible variations
        for variation in offset_variations:
            candidate_section = {}
            for (name, value), offset in zip(candidate_dict.items(), variation):
                new_value = value + offset
                term = self.utility.handle_integer(new_value)
                candidate_section[name] = term
            candidate_terms.append([candidate_section])          
        return candidate_terms

    def check_all_candidates(self, candidate_terms):
        # candidate_terms = [
        # [{constant_name1: value1, constant_name2: value2, constant_name3: value3}],
        # [{constant_name1: value4, constant_name2: value5, constant_name3: value6}]]

        for candidate_section in candidate_terms:
            self.process() # reset assertions + ready solver for candidate checking
            print("Attempting to solve with candidates:")
            for candidate_dict in candidate_section:
                for name, value in candidate_dict.items():
                    print(f"{name}: {value}")
                    # Create one constraint for each candidate
                    constraint = self.API.solver.mkTerm(
                        Kind.EQUAL, self.terms.vars[name], value)
                    self.API.solver.assertFormula(constraint)

            if not (self.main.check_candidate()):
                # Break loop if candidate solution is correct
                break

    def process(self):
        # Reset constant=candidate assertion
        self.API.solver.resetAssertions()
        for subTree in self.ast:
            if subTree[0] == "assert":
                # Process each assert command
                constraint = self.process_constraint(subTree[1])
                self.API.solver.assertFormula(constraint)

    def process_constraint(self, subtree):
        # leaf node = string
        # subtree = list
        if (isinstance(subtree, str)):
            if subtree in self.terms.vars:
                return self.terms.vars[subtree] # return constant
            else:
                return self.utility.handle_integer(subtree)
        
        else:
            # Call process_constraint for all operands (depth-first traversal)
            operator = subtree[0]
            operands = [self.process_constraint(operand) for operand in subtree[1:]]
            return self.utility.create_term(operator, operands)
    
    # NOTE: find_new_candidate uses the Chinese Remainder Theorem
    # NOTE: Follows the equation detailed in the Wikipedia page for the Chinese Remainder Theorem
    # NOTE: Specifically, the equation for the "Case of two modulo" in the
    # NOTE: "Existence (constructive proof) section". Source:
    # NOTE: https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Existence_(constructive_proof)
    def find_new_candidate(self, candidate1, candidate2):
        # candidate = (modulus, result)
        
        # x = r1 (mod m1), x = r2 (mod m2)
        # Bezout's identity: a1*m1 + a2*m2 = 1
        # Extended Euclidean algorithm: computes a1 and a2
        # x = (r1*a2*m2 + r2*a1*m1) mod m1*m2

        # Extract values
        r1 = candidate1[1]
        r2 = candidate2[1]
        m1 = candidate1[0]
        m2 = candidate2[0]

        a1, a2 = self.calculate_coefficients(m1, m2)
        new_mod = m1*m2
        new_result = (r1*a2*m2 + r2*a1*m1) % new_mod
        
        # Ensure result is positive
        if new_result < 0:
            new_result += new_mod
        return (new_mod, new_result)

    # NOTE: calculate_coefficients uses the Extended Euclidean algorithm
    # NOTE: Implements a modified version of a Python implementation of the Extended Euclidean algorithm
    # NOTE: from a website entitled "GeeksforGeeks". Source:
    # NOTE: https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
    # NOTE: However, this modified version is simplified and adapted for calculating Bezout's identity
    def calculate_coefficients(self, m1, m2):
        if m2 == 0:
            # when m2 = 0, gcd(m1, m2) = m1
            # a1 = 1, a2 = 0
            return (1, 0)
        else:
            # Recursively calculate coefficients
            # gcd(m1, m2) = gcd(m2, m1 mod m2)
            x, y = self.calculate_coefficients(m2, m1 % m2)
            a1 = y # set a1 to previous value of y
            a2 = x - ((m1 // m2) * y) # integer division
            return (a1, a2)
        