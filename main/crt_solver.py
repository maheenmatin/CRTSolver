import cvc5
from cvc5 import Kind
import time
import builtins
import multiprocessing
from pathlib import Path
import input_output.reader as reader
import input_output.writer as writer
import crt_components.solvers.modulo as modulo
import crt_components.solvers.modulo_bv as modulo_bv
import crt_components.solvers.candidate as candidate
import crt_components.helpers.dto as dto
import crt_components.helpers.prime_generator as prime_generator
import crt_components.helpers.utility as utility
import crt_components.errors.error as error

class CRTSolver:
    def __init__(self, use_bitvectors, time_limit, solver_name):
        # Set root directory for robust file paths
        # CRTSolver -> main -> crt_solver.py
        # crt_solver.py = file, main = parents[0], CRTSolver = parents[1]
        self.ROOT = Path(__file__).resolve().parents[1]

        # Set absolute paths from root directory
        self.TESTS = self.ROOT / "main" / "tests"
        self.RESULTS = self.ROOT / "main" / "results"

        self.use_bitvectors = use_bitvectors
        self.time_limit = time_limit # timeout for each check-sat in cvc5 (milliseconds)
        self.total_time_limit = float(time_limit) / 1000.0 # total time limit (seconds)
        self.solver_name = solver_name
        self.writer = writer.Writer(self.RESULTS, self.solver_name)
        
    def reinit(self):
        self.API = dto.API(self.time_limit)
        self.terms = dto.Terms()
        self.generator = prime_generator.Prime_Generator().get_next_prime()
        self.primes = dto.Primes()
        self.bitwidth = dto.Bitwidth()
        self.utility = utility.Utility(self.API, self.terms, self.primes, self.bitwidth, self)
        self.ast = []
        self.sat_model = [] # if SAT, stores satisfying values
        self.continue_sat = True # flag for while loop

    def get_solver_name(self):
        return self.solver_name

    def execute(self):
        for file in reader.get_sorted_files(self.TESTS):
            if file.is_file():
                #builtins.input("Press any key to continue:")
                result_queue = multiprocessing.Queue() # queue for sat_model
                start_time = time.time()

                # Start a new subprocess for each file
                process = multiprocessing.Process(
                    target=self.process_file_wrapper,
                    args=(str(file), result_queue)
                )
                process.start()
                process.join(self.total_time_limit)

                # If process times out, terminate and store result
                if process.is_alive():
                    print(f"Timeout reached for {file.name}. Terminated process.")
                    process.terminate()
                    process.join()
                    self.writer.store_result(file, start_time, [["UNKNOWN (TIMEOUT)"]])

                # If process terminates normally, get result from queue and store
                else:
                    sat_model = result_queue.get_nowait() # do not block and wait
                    self.writer.store_result(file, start_time, sat_model)
        self.writer.write()

    def process_file_wrapper(self, file, result_queue):
        try:
            self.reinit()
            self.process_file(file)
        except error.AbortFileException as e:
            print(f"AbortFileException: {e}")
            self.sat_model.append(["UNKNOWN (ERROR)"])
        result_queue.put(self.sat_model)

    def process_file(self, file):
        file = Path(file) # convert back to Path object
        print(f"Reading file: {file}")

        # Get AST
        with file.open("r") as input:
            self.ast = reader.preprocess(input, self.API, self.terms)

        # Initialize modulo and candidate
        self.init_mod_and_candidate()

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
            self.continue_sat = False
            print("Candidate SAT")
            for name, constant in self.terms.vars.items():
                # Get solution from solver
                model = self.API.solver.getValue(constant).getIntegerValue()
                print(f"{name}: {model}")
                self.sat_model.append([name, model])
            print()
            return False
        # If UNSAT, attempt to solve modulo new prime
        else:
            print("Candidate UNSAT")
            return True

if __name__ == "__main__":
    #crt_solver_int = CRTSolver(False, "10000", "CRTSolver (Integer Mode)")
    #crt_solver_int.execute()

    crt_solver_bv = CRTSolver(True, "10000", "CRTSolver (Bit-Vector Mode)")
    crt_solver_bv.execute()
