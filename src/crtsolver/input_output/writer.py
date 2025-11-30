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
        # self.results = [[1, "Cat", 0.538, [["UNSAT"]]]]

        # Build totals
        unsat_count = sum(1 for item in self.results if item[5][0][0] == "UNSAT")
        unknown_count = sum(1 for item in self.results if item[5][0][0] == "UNKNOWN (TIMEOUT)" or 
            item[5][0][0] == "UNKNOWN (ERROR)")
        sat_count = len(self.results) - unsat_count - unknown_count

        self.file_count = f"Totals: {self.file_count}"
        total_na = "n/a"
        self.total_time = f"{self.total_time}s"
        total_results = f"{sat_count} SAT, {unsat_count} UNSAT, {unknown_count} UNKNOWN"

        self.results.append([self.file_count, total_na, self.total_time, total_results])

        # newline="" guarantees OS-independent behaviour
        with open(self.file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(["TestInput", "FileName", "Variables", "Degree", "Runtime (s)", "Result"])
            # Write remaining rows (including totals row)
            writer.writerows(self.results)

    def store_result(self, file, start_time, sat_model):
        # Get information from file object
        file_name = file.stem
        no_of_vars = file.parent.parent.name
        no_of_degrees = file.parent.name

        # Store information and result for file
        end_time = time.time()
        time_taken = end_time - start_time
        self.file_count += 1

        self.results.append(
            [self.file_count, file_name, no_of_vars, no_of_degrees, time_taken, sat_model])
        
        self.total_time += time_taken
