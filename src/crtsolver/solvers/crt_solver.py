import cvc5
from cvc5 import Kind
import time
import argparse
import builtins
import signal
from pathlib import Path
<<<<<<< HEAD:src/crtsolver/solvers/crt_solver.py
from crtsolver.input_output import reader, writer
from crtsolver.crt_components.engine import modulo, modulo_bv, candidate
from crtsolver.crt_components.helpers import dto, prime_generator, utility
from crtsolver.crt_components.errors import error
=======
import input_output.reader as reader
import input_output.writer as writer
import crt_components.solvers.modulo as modulo
import crt_components.solvers.modulo_bv as modulo_bv
import crt_components.solvers.candidate as candidate
import crt_components.helpers.dto as dto
import crt_components.helpers.prime_generator as prime_generator
import crt_components.helpers.utility as utility
import crt_components.errors.error as error
import crt_components.errors.handler as handler
>>>>>>> main:main/crt_solver.py

class CRTSolver:
    def __init__(self, time_limit="30000", solver_name="CRTSolver", use_bitvectors=True):
        # Set root directory for robust file paths
        # CRTSolver -> src -> solvers -> crt_solver.py
        # crt_solver.py = file, solvers = parents[0], crtsolver = parents[1],
        # src = parents[2], CRTSolver = parents[3]
        self.ROOT = Path(__file__).resolve().parents[3]

        # Set absolute paths from root directory
        self.TESTS = self.ROOT / "tests"
        self.RESULTS = self.ROOT / "results"

        if use_bitvectors:
            self.solver_name = solver_name + " (Bit-Vector Mode)"
        else:
            self.solver_name = solver_name + " (Integer Mode)"

        self.use_bitvectors = use_bitvectors
        self.time_limit = time_limit
        self.writer = writer.Writer(self.RESULTS, self.solver_name)
        
    def reinit(self):
        self.API = dto.API(self.time_limit)
        self.terms = dto.Terms()
        self.generator = prime_generator.Prime_Generator().get_next_prime()
        self.primes = dto.Primes()
        self.bitwidth = dto.Bitwidth()
        self.utility = utility.Utility(self.API, self.terms, self.primes, self.bitwidth, self)
        self.start_time = time.time()
        self.ast = []
        self.sat_model = [] # if SAT, stores satisfying values
        self.continue_sat = True # flag for while loop

    def get_solver_name(self):
        return self.solver_name

    def execute(self):
        for file in reader.get_sorted_files(self.TESTS):
            if file.is_file():
                #builtins.input("Press any key to continue:")

                # Reinitialize data for new file
                self.reinit()
                print(f"Reading file: {file}")

                # Get AST
                with file.open("r") as input:
                    self.ast = reader.preprocess(input, self.API, self.terms)

                # Initialize modulo and candidate
                self.init_mod_and_candidate()

                # Set up signal for solver timeout
                signal.signal(signal.SIGALRM, handler.timeout_handler)
                # Set alarm time -> integer division gives timeout in seconds
                signal.alarm(int(self.time_limit) // 1000)

                try:
                    while self.continue_sat:
                        # Attempt to solve modulo prime
                        self.solve_modulo()
                        # If UNSAT modulo prime, original problem is also UNSAT
                        if self.continue_sat:
                            # If SAT, attempt to solve original problem with candidate solution
                            self.solve_candidate()
                            # If SAT, original problem is SAT and candidate solution is correct
                            # If UNSAT, attempt to solve modulo new prime
                            #builtins.input("Press any key to continue:")
                except error.AbortFileException as e:
                    print(e)
                    print("UNKNOWN (ERROR)\n")
                    self.continue_sat = False
                    self.sat_model.append(["UNKNOWN (ERROR)"])
                    self.continue_sat = False
                except error.TimeoutException:
                    print("UNKNOWN (TIMEOUT)\n")
                    self.continue_sat = False
                    self.sat_model.append(["UNKNOWN (TIMEOUT)"])
                finally:
                    signal.alarm(0) # disable alarm

                self.writer.store_result(file, self.start_time, self.sat_model)
        self.writer.write()

    def init_mod_and_candidate(self):
        if self.use_bitvectors:
            self.modulo = modulo_bv.Modulo_BV(
                self.ast, self.API, self.terms, self.primes, self.bitwidth, self.utility)
        else:
            self.modulo = modulo.Modulo(
                self.ast, self.API, self.terms, self.primes, self.utility)
        self.candidate = candidate.Candidate(self.ast, self.API, self.terms, self.utility, self)

    def solve_modulo(self):
        # Get current prime
        self.primes.prime = next(self.generator)
        print(f"Attempting to solve with mod {self.primes.prime}")

        # Attempt to solve modulo prime
        self.modulo.compute_mod()
        #for assertion in self.API.mod_solver.getAssertions():
            #print(assertion)

        # Check satisfiability
        result = self.API.mod_solver.checkSat()
        if result.isUnsat():
            print("UNSAT\n")
            self.continue_sat = False
            self.sat_model.append(["UNSAT"])
        if result.isUnknown():
            print("UNKNOWN (TIMEOUT)\n")
            self.continue_sat = False
            self.sat_model.append(["UNKNOWN (TIMEOUT)"])

    def solve_candidate(self):
        # Get candidate values from solver (represented as int)
        print(f"Retrieving candidates for mod {self.primes.prime}")
        candidate_vals = [] # [result1, result2]
        var_names = list(self.terms.vars.keys()) # [constant_name1, constant_name2]
        if self.use_bitvectors:
            for name in var_names:
                # Get bv values from solver (represented as int)
                val = self.terms.bv_mod_vars[f"{name}_mod_{self.primes.prime}"]
                bitvector_val = self.API.mod_solver.getValue(val).getBitVectorValue()
                candidate_vals.append(int(bitvector_val, 2)) # conversion from base 2 to int
        else:
            for name in var_names:
                # Get int values from solver
                val = self.terms.mod_vars[f"{name}_mod_{self.primes.prime}"]
                candidate_vals.append(self.API.mod_solver.getValue(val).getIntegerValue())

        # Build candidate_list DTO
        candidate_list = [] # [(constant_name, modulus, result)]
        for name, value in zip(var_names, candidate_vals):
            print(f"{name}: {value}")
            candidate_list.append((name, self.primes.prime, value))
        
        # Attempt to solve original problem with candidate solution
        self.candidate.compute_candidate(candidate_list)
        #for assertion in self.API.solver.getAssertions():
            #print(assertion)

    def check_candidate(self):
        # If SAT, original problem is SAT and candidate solution is correct
        if self.API.solver.checkSat().isSat():
            self.continue_sat = continue_check = False
            print("Candidate SAT")
            for name, constant in self.terms.vars.items():
                # Get solution from solver
                model = self.API.solver.getValue(constant).getIntegerValue()
                print(f"{name}: {model}")
                self.sat_model.append([name, model])
            print()
        # If UNSAT, attempt to solve modulo new prime
        else:
            continue_check = True
            print("Candidate UNSAT")
        return continue_check
    
# CLI entry point
def main():
    #crt_solver_int = CRTSolver(False, "10000", "CRTSolver (Integer Mode)")
    #crt_solver_int.execute()

    parser = argparse.ArgumentParser(description="Run CRTSolver on a directory of SMT2 files.")
    parser.add_argument("--time_limit", type=int, default=30000,
        help="Time limit for each check-sat (in ms).")
    parser.add_argument("--solver_name", default="CRTSolver",
        help="Name for the solver run (used in output results).")
    parser.add_argument("--tests_dir", default=None,
        help="Path to directory containing test SMT2 files.")
    
    # Default: use_bitvectors = True (bit-vector mode)
    parser.set_defaults(use_bitvectors=True)
    parser.add_argument(
        "--integer_mode",
        dest="use_bitvectors",
        action="store_false",
        help="Disable bit-vector mode (use integer mode instead)."
    )
    args = parser.parse_args()

    solver = CRTSolver(
        time_limit=str(args.time_limit),
        solver_name=args.solver_name,
        use_bitvectors=args.use_bitvectors
    )
    solver.execute()

if __name__ == "__main__":
    main()
