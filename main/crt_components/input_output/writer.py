import csv
import time
from pathlib import Path

class Writer:
    def __init__(self, file_path, solver_name):
        self.file_name = file_path / f"results_{solver_name}.csv"
        self.results = []
        self.file_count = 0
        self.total_time = 0

    def write(self):
        # self.results = [[1, 0.538, [["UNSAT"]]]]
        
        # Build totals
        unsat_count = sum(1 for item in self.results if item[2][0][0] == "UNSAT")
        unknown_count = sum(1 for item in self.results if item[2][0][0] == "UNKNOWN (TIMEOUT)" or 
            item[2][0][0] == "UNKNOWN (ERROR)")
        sat_count = len(self.results) - unsat_count - unknown_count

        sat_count = f"Total: {sat_count} SAT, {unsat_count} UNSAT, {unknown_count} UNKNOWN"
        self.file_count = f"Total: {self.file_count}"
        self.total_time = f"Total: {self.total_time}"
        self.results.append([self.file_count, self.total_time, sat_count])

        # newline="" guarantees OS-independent behaviour
        with open(self.file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(["TestInput (number)", "Runtime (seconds)", "Model (constants)"])
            # Write remaining rows (including totals row)
            writer.writerows(self.results)

    def store_result(self, test_no, start_time, sat_model):
        # Store information and result for file
        end_time = time.time()
        time_taken = end_time - start_time
        self.results.append([test_no, time_taken, sat_model])
        self.file_count += 1
        self.total_time += time_taken
