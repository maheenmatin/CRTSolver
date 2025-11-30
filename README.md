# CRTSolver - Solving QF_NIA Using the Chinese Remainder Theorem

**Tech Stack:** Python, Poetry, cvc5, Jupyter, Pandas, Matplotlib

## Introduction
CRTSolver is a novel Chinese Remainder Theorem-based heuristic algorithm in Python, extending the cvc5 SMT solver
to accelerate software/hardware verification workflows.

The algorithm is designed for more efficient and successful solving of QF_NIA problems, combining the CRT-based heuristic with bit-vector encoding to achieve up to 13.2x speedup over baseline cvc5.

### More formally...
CRTSolver is a prototype SMT solver for  non-linear integer equations that leverages a Chinese Remainder Theorem-based heuristic and bit-vector encoding to achieve performance comparable or better than Z3 and cvc5 in quantifier-free non-linear integer arithmetic logic (QF_NIA) under 10-second timeouts and 4GB memory limits, across 38 SMT-LIB benchmarks with one to three variables, quadratic or cubic degree, and mixed SAT/UNSAT status.

The algorithm uses an abstraction–refinement style semi-decision procedure for sets of polynomial equations over the integers. A modulo solver, implemented using cvc5, incrementally solves copies of the problem modulo an ascending sequence of pairwise-coprime moduli. Models from all modulo instances seen so far are combined using the Chinese Remainder Theorem to produce candidate solutions modulo the product of the moduli; these are lifted to a small family of integer candidates, each of which is checked by a second cvc5 instance over the original non-linear integer formula.

Unsatisfiability modulo some modulus proves UNSAT, while a satisfying candidate proves SAT; otherwise additional moduli and candidates are explored. The implementation offers Integer and Bit-Vector modes, using QF_NIA and quantifier-free bit-vector (QF_BV) logic respectively.

During development, it was also necessary to create cvc5 and Z3 batch-solving scripts, which are available as CLI tools within this repository.

---

# Setup Guide

## Prerequisites

You’ll need:

- **Linux**
- **Python 3.10–3.12**
- **Poetry** (for dependency and environment management)
- **Visual Studio Code**
- **Python** and **Jupyter** extensions for VS Code

Optional (for classic Jupyter usage):

- `jupyterlab` or `notebook` installed in your environment

---

## 1. Clone and enter the project

```bash
git clone https://github.com/maheenmatin/CRTSolver
cd CRTSolver
```

---

## 2. Environment & dependencies (Poetry)

Poetry will create a virtual environment in `.venv` inside the project:

```bash
poetry config virtualenvs.in-project true
poetry install
```

This will:

- Install the `crtsolver` package (from `src/`) in editable/development mode.
- Install all runtime dependencies (cvc5, z3-solver, numpy, pandas, matplotlib, …).
- Install dev dependencies (e.g. `ipykernel`) for notebook usage.

---

## 3. Running the solvers from the command line (CLI)

The project exposes three console scripts via Poetry:

- `crt-solver`
- `cvc5-solver`
- `z3-solver`

Each accepts:

- `--time_limit` (int, milliseconds; default: `30000`)
- `--solver_name` (string; used in result output)

In addition, `crt-solver` accepts:
- `--integer_mode` (flag; if present, use integer mode instead of bit-vector mode)

From the project root:

```bash
# CRTSolver (Bit-Vector Mode)
poetry run crt-solver \
  --time_limit 30000 \
  --solver_name "CRTSolver"

# CRTSolver (Integer Mode)
poetry run crt-solver \
  --time_limit 30000 \
  --solver_name "CRTSolver" \
  --integer_mode

# cvc5
poetry run cvc5-solver \
  --time_limit 30000 \
  --solver_name "cvc5"

# Z3
poetry run z3-solver \
  --time_limit 30000 \
  --solver_name "z3"
```

Results are written into the `results/` directory.

---

## 4. Running the comparative analysis notebook in VS Code

### 4.1 Open the project in VS Code

From the project root:

```bash
code .
```

### 4.2 Select the Poetry / `.venv` interpreter

1. Press `Ctrl+Shift+P`.
2. Run **“Python: Select Interpreter”**.
3. Choose the interpreter located in `.venv`, e.g.:

   ```
   Python 3.x.x ('.venv': poetry) ...
   ```

### 4.3 (Optional) Register a named Jupyter kernel

```bash
poetry run python -m ipykernel install --user --name=crtsolver-poetry
```

You can then choose `crtsolver-poetry` as the kernel in VS Code.

### 4.4 Open and run the notebook

1. In VS Code, open: `notebooks/comparative_analysis.ipynb`.
2. In the top-right, select **Kernel** → choose either:
   - `crtsolver-poetry`, or
   - the `.venv` Python environment.
3. Run all cells.

The notebook:

- Uses the installed `crtsolver` package:

  ```python
  from crtsolver.solvers import crt_solver, cvc5_solver, z3_solver
  ```

- Uses `reports.generators` utilities:

  ```python
  from reports.generators import csv_combiner, latex_generator
  ```

- Reads test instances from `tests/`.
- Writes solver results to `results/` and report artefacts (e.g. combined CSVs, cactus plot PDFs) to `reports/`.

---

## 5. Reports: CSV combiner & LaTeX generator

The `reports/generators` modules provide post-processing helpers:

- `csv_combiner.py` – combines per-run CSVs from `results/` into a single CSV under `reports/`.
- `latex_generator.py` – consumes the combined CSV and generates LaTeX artefacts.

### 5.1 From the command line

```bash
poetry run python reports/generators/csv_combiner.py
poetry run python reports/generators/latex_generator.py
```

### 5.2 From the notebook

```python
from reports.generators import csv_combiner, latex_generator

csv_combiner.main()
latex_generator.main()
```

---

## File Structure

```plaintext
CRTSolver/
├── .gitignore
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── third_party_licences/
│   └── ...
├── src/
│   └── crtsolver/
│       ├── __init__.py
│       ├── crt_components/
│       │   ├── __init__.py
│       │   ├── engine/
│       |   |   └── ...
│       │   ├── helpers/
│       |   |   └── ...
│       │   |── errors/
│       |   |   └── ...
│       ├── input_output/
│       │   ├── __init__.py
│       |   ├── ...
│       └── solvers/
│           ├── __init__.py
│           ├── crt_solver.py
│           ├── cvc5_solver.py
│           └── z3_solver.py
├── tests/
│   └── ...
├── results/
│   └── ...
├── reports/
│   ├── __init__.py
│   └── generators/
│       ├── __init__.py
│       ├── csv_combiner.py
│       └── latex_generator.py
└── notebooks/
    └── comparative_analysis.ipynb
```
