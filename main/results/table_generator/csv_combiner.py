from pathlib import Path
import pandas as pd

class CSV_Combiner:
    def __init__(self):
        # Paths
        self.ROOT = Path(__file__).resolve().parents[3]
        self.INPUT_PATH = self.ROOT / "main" / "results"
        self.OUTPUT_PATH = self.ROOT / "main" / "results" / "tables" / "combined_results.csv"

        self.SOLVER_LIST = [
            "CRTSolver (Integer Mode)",
            "CRTSolver (Bit-Vector Mode)",
            "Z3",
            "cvc5"
        ]

        self.COLUMN_ORDER = [
            "FileName", "Variables", "Degree",
            "CRT-INT Runtime", "CRT-INT Result",
            "CRT-BV Runtime", "CRT-BV Result",
            "Z3 Runtime", "Z3 Result", "cvc5 Runtime", "cvc5 Result"
        ]

    def execute(self):
        combined_df = self.collate_runtimes()
        combined_df = self.reorder_rows_and_columns(combined_df)
        combined_df = self.clean_data(combined_df)

        # Convert to CSV and save
        combined_df.to_csv(self.OUTPUT_PATH, index=False)
        print(f"Combined CSV saved to {self.OUTPUT_PATH}")

    def collate_runtimes(self):
        # Declare combined dataframe
        combined_df = None

        # Extract runtime from each CSV to populate runtimes
        for solver_name in self.SOLVER_LIST:
            file_path = self.INPUT_PATH / f"results_{solver_name}.csv"

            # Establish runtime and result column names
            if solver_name == "CRTSolver (Integer Mode)":
                solver_name = "CRT-INT"
            elif solver_name == "CRTSolver (Bit-Vector Mode)":
                solver_name = "CRT-BV"
            runtime_column_name = f"{solver_name} Runtime"
            result_column_name = f"{solver_name} Result"

            df = pd.read_csv(file_path)

            # Drop last row from - contains summary data that cannot be converted to float
            df = df[:-1]

            # Drop unnecessary columns
            df = df[["FileName", "Variables", "Degree", "Runtime (s)", "Result"]]

            # Rename runtime and result columns
            df = df.rename(columns={
                "Runtime (s)": runtime_column_name,
                "Result": result_column_name})

            # If first file, use metadata from this file
            if combined_df is None:
                combined_df = df

            # For all other files, add runtime column by merging on FileName (do not use metadata)
            else:
                # Merge using FileName column as primary key
                # Keep only the "solver_name Runtime (s)" column
                # Outer join retains rows with no matching FileName - for error-checking
                combined_df = pd.merge(combined_df, 
                    df[["FileName", runtime_column_name, result_column_name]], 
                    on="FileName", how="outer")
        return combined_df

    def reorder_rows_and_columns(self, combined_df):
        # Reformat number of variables and number of degrees entries
        combined_df["Variables"] = combined_df["Variables"].str.extract(r"(\d+)").astype(int)
        # Match one or more digits, then convert to int
        combined_df["Degree"] = combined_df["Degree"].str.extract(r"(\d+)").astype(int)

        # Sort by VarNum, then DegNum
        combined_df = combined_df.sort_values(by=["Variables", "Degree"])

        # Reorder columns
        combined_df = combined_df[self.COLUMN_ORDER]
        return combined_df

    def clean_data(self, combined_df):
        # Add and populate SAT column
        # Format T/O and I/O as necessary
        # Drop results columns

        # Initialise SAT column and inconsistent_files list
        combined_df["SAT"] = "?"
        inconsistent_files = []

        # Specify list of solvers
        solvers = [
            "CRT-INT",
            "CRT-BV",
            "Z3",
            "cvc5"
        ]

        for solver in solvers:
            runtime_col_name = f"{solver} Runtime"
            combined_df[runtime_col_name] = combined_df[runtime_col_name].astype("object")
            result_col_name = f"{solver} Result"

            for index, row in combined_df.iterrows():
                # Obtain result, current SAT value, and file name
                result = str(row[result_col_name]) # row is read-only -> row[col_name]
                current_sat = combined_df.at[index, "SAT"] # at is read-write -> at.[index, col_name]
                file_name = row["FileName"]

                # Handle UNKNOWN (TIMEOUT)
                if "UNKNOWN (TIMEOUT)" in result:
                    combined_df.at[index, runtime_col_name] = "T/O"

                # Handle UNKNOWN (ERROR)
                elif "UNKNOWN (ERROR)" in result:
                    combined_df.at[index, runtime_col_name] = f"I/O ({row[runtime_col_name]})"

                # Handle UNSAT
                elif "UNSAT" in result:
                    if current_sat == "SAT":
                        inconsistent_files.append(file_name)
                    combined_df.at[index, "SAT"] = "UNSAT"

                # Handle SAT (with model)
                else:
                    if current_sat == "UNSAT":
                        inconsistent_files.append(file_name)
                    combined_df.at[index, "SAT"] = "SAT"


        # Identify unresolved files (still marked as "?")
        unresolved_files = combined_df[combined_df["SAT"] == "?"]["FileName"].tolist()

        # Identify files requiring manual input (union of inconsistent and x)
        manual_files = set(inconsistent_files) | set(unresolved_files)

        # Resolve files using manual input
        if manual_files:
            print("Manual intervention required for the following files:")
            for file in manual_files:
                while True:
                    sat_value = input(f"Enter SAT or UNSAT for '{file}': ").strip()
                    if sat_value in {"SAT", "UNSAT", "?"}:
                        # Set SAT value for file
                        combined_df.loc[combined_df["FileName"] == file, "SAT"] = sat_value
                        break
                    else:
                        print("Invalid input - type SAT, UNSAT or ?")

        # Drop result columns
        result_columns = [f"{solver} Result" for solver in solvers]
        combined_df = combined_df.drop(columns=result_columns)

        # Move SAT column to correct position (after degree)
        columns = list(combined_df.columns)
        columns.insert(columns.index("Degree") + 1, columns.pop(columns.index("SAT")))
        combined_df = combined_df[columns]
        return combined_df

if __name__ == "__main__":
    combiner = CSV_Combiner()
    combiner.execute()
    