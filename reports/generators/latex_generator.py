from pathlib import Path
import pandas as pd
import re

class LaTeX_Generator:
    def __init__(self):
        # Paths
        self.ROOT = Path(__file__).resolve().parents[2]
        self.INPUT_PATH = self.ROOT / "results" / "combined_results.csv"
        self.OUTPUT_PATH = self.ROOT / "reports" / "latex_table.txt"
    
    def execute(self):
        latex_lines = self.populate_latex_lines()

        # Write to .txt file
        with open(self.OUTPUT_PATH, "w") as f:
            f.write("\n".join(latex_lines))

        print(f"LaTeX code written to {self.OUTPUT_PATH}")

    def populate_latex_lines(self):
        df = pd.read_csv(self.INPUT_PATH)
        latex_lines = []

        for _, row in df.iterrows():
            name = row["FileName"]
            var = int(row["Variables"])
            deg = int(row["Degree"])
            sat = row["SAT"]
            equations = "?"

            crt_int = self.format_runtime(row["CRT-INT Runtime"])
            crt_bv = self.format_runtime(row["CRT-BV Runtime"])
            z3 = self.format_runtime(row["Z3 Runtime"])
            cvc5 = self.format_runtime(row["cvc5 Runtime"])

            latex_row = f"{name} & {var} & {deg} & {equations} & {sat} & {crt_int} & {crt_bv} & {z3} & {cvc5} \\\\"
            latex_lines.append(latex_row)
        return latex_lines

    def format_runtime(self, runtime):
            # Handle T/O
            if runtime == "T/O":
                return runtime
            
            # Handle I/O
            elif runtime.startswith("I/O"):
                match = re.search(r"I/O\s*\((\d*\.?\d+)\)", runtime)
                overflow_time = match.group(1)
                formatted_time = self.format_runtime(overflow_time)
                return f"U ({formatted_time})"
            
            # Handle runtime
            else:
                runtime = float(runtime)

                # If less than 1s, use scientific notation to 3 significant figures
                if float(runtime) < 1:
                    # .2e -> 1 digit before the decimal and 2 digits after = 3 significant figures
                    return f"${runtime:.2e}".replace("e", r" \times 10^{") + "}$"
                
                # If greater than 1s, round to 3 decimal places
                else:
                    return f"${runtime:.3f}$"
                
def main():
    creator = LaTeX_Generator()
    creator.execute()
    

if __name__ == "__main__":
    main()
