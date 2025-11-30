from pathlib import Path
import cvc5
from cvc5 import Kind
import time
from crtsolver.input_output import reader, writer

# NOTE: Inspired by code and instructions from the following sources:
# NOTE: https://cvc5.github.io/docs-ci/docs-main/api/python/base/quickstart.html
# NOTE: https://cvc5.github.io/docs-ci/docs-main/examples/parser.html
class cvc5Solver:
    def __init__(self, time_limit, solver_name):
        # Set root directory for robust file paths
        # CRTSolver -> src -> solvers -> cvc5_solver.py
        # cvc5_solver.py = file, solvers = parents[0], crtsolver = parents[1],
        # src = parents[2], CRTSolver = parents[3]
        self.ROOT = Path(__file__).resolve().parents[3]

        # Set absolute paths from root directory
        self.TESTS = self.ROOT / "tests"
        self.RESULTS = self.ROOT / "results"

        self.time_limit = time_limit
        self.solver_name = solver_name
        self.writer = writer.Writer(self.RESULTS, self.solver_name)
        
    def reinit(self):
        # Create solver
        self.solver = cvc5.Solver()
        
        # Set solver options
        self.solver.setOption("produce-models", "true") # allows model retrieval
        self.solver.setOption("produce-unsat-cores", "true") # allows unsat core retrieval
        self.solver.setOption("tlimit-per", self.time_limit) # time limit for each check-sat
        self.solver.setLogic("QF_NIA")

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

                with file.open("r") as input:
                    input_code = input.read()

                # Create parser
                parser = cvc5.InputParser(self.solver)

                # Send input code to parser
                parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6, input_code, "")

                # Get symbol manager for parser
                sm = parser.getSymbolManager()

                # Parse all commands in input code
                while True:
                    command = parser.nextCommand()
                    if command.isNull():
                        break
                    # Invoke command using solver and symbol manager
                    print(command.invoke(self.solver, sm), end="")

                # Check satisfiability
                result = self.solver.checkSat()
                if result.isSat():
                    # Get all declared variable names and terms
                    declared_terms = sm.getDeclaredTerms()
                    for term in declared_terms:
                        name = str(term) # constant name
                        model = self.solver.getValue(term) # constant value
                        self.sat_model.append([name, model])
                elif result.isUnsat():
                    self.sat_model.append(["UNSAT"])
                elif result.isUnknown():
                    self.sat_model.append(["UNKNOWN (TIMEOUT)"])

                print()
                self.writer.store_result(file, self.start_time, self.sat_model)
        self.writer.write()

def main():
    base_cvc5 = cvc5Solver("100", "cvc5")
    base_cvc5.execute()

if __name__ == "__main__":
    main()
