from pathlib import Path
from z3 import *
import time
import input_output.reader as reader
import input_output.writer as writer

# NOTE: Inspired by code and instructions from the following sources:
# NOTE: https://ericpony.github.io/z3py-tutorial/guide-examples.htm
# NOTE: https://z3prover.github.io/papers/programmingz3.html
class Z3Solver:
    def __init__(self, time_limit, solver_name):
        # Set root directory for robust file paths
        # CRTSolver -> main -> cvc5_solver.py
        # cvc5_solver.py = file, main = parents[0], CRTSolver = parents[1]
        self.ROOT = Path(__file__).resolve().parents[1]

        # Set absolute paths from root directory
        self.TESTS = self.ROOT / "main" / "tests"
        self.RESULTS = self.ROOT / "main" / "results"

        self.time_limit = time_limit
        self.solver_name = solver_name
        self.writer = writer.Writer(self.RESULTS, self.solver_name)
        
    def reinit(self):
        # Create solver
        self.solver = Solver()
        
        # Set solver options
        self.solver.set(unsat_core=True)
        self.solver.set(timeout=int(self.time_limit))

        self.start_time = time.time()
        self.sat_model = [] # if SAT, stores satisfying values

    def get_solver_name(self):
        return self.solver_name

    def execute(self):
        for file in reader.get_sorted_files(self.TESTS):
            if file.is_file():
                # Reinitialize data for new file
                self.reinit()
                print(f"Reading file: {file}")

                #with file.open("r") as input:
                    #input_code = input.read()

                self.solver.from_file(str(file)) # from_file expects string, not Path

                # Check satisfiability
                result = self.solver.check()
                if result == sat:
                    model = self.solver.model()
                    # Get all declared variable names and terms
                    for decl in model.decls():
                        name = decl.name() # constant name
                        value = model[decl] # constant value
                        self.sat_model.append([name, value])
                elif result == unsat:
                    self.sat_model.append(["UNSAT"])
                elif result == unknown:
                    self.sat_model.append(["UNKNOWN (TIMEOUT)"])

                print()
                self.writer.store_result(file, self.start_time, self.sat_model)
        self.writer.write()

if __name__ == "__main__":
    z3_solver = Z3Solver("30000", "Z3")
    z3_solver.execute()
