from pathlib import Path
import pandas as pd

class Results_Combiner:
    def __init__(self):
        # Paths
        self.ROOT = Path(__file__).resolve().parents[1]
        self.RESULTS_PATH = self.ROOT / "main" / "results"
        self.RESULTS = list(self.RESULTS_PATH.glob("*.csv"))
        self.OUTPUT_PATH = Path("combined_runtimes.csv")

        # Column order for combined file
        self.SOLVER_ORDER = [
            "CRTSolver (Integer Mode)",
            "CRTSolver (Bit-Vector Mode)",
            "Z3",
            "cvc5"
        ]

    def create_combined_runtimes(self):
        # Declare dictionary to store runtime columns
        runtimes = {}

        # Extract runtime from each CSV to populate runtimes
        for file in self.RESULTS:
            df = pd.read_csv(file)

            # Omit results_ prefix from column heading
            column_heading = file.stem.replace("results_", "")

            # Drop last row from - contains summary data that cannot be converted to float
            df = df[:-1]

            runtime = df["Runtime (s)"].astype(float)
            runtimes[column_heading] = runtime

        # Combine runtime data into a single dataframe
        combined_df = pd.DataFrame(runtimes)

        # Reorder dataframe columns
        combined_df = combined_df[self.SOLVER_ORDER]

        # Convert to CSV and save
        combined_df.to_csv(self.OUTPUT_PATH, index=False)
        print(f"Combined CSV saved to {self.OUTPUT_PATH}")
    
    def convert_to_format(self):
        return

if __name__ == "__main__":
    combiner = Results_Combiner()
    combiner.create_combined_runtimes()
    combiner.convert_to_format()
    