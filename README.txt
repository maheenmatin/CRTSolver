0) Prerequisites:
- Using Linux
- Python 3 installed
- Jupyter Notebook installed
- VS Code installed
- Python and Jupyter extensions added to VS Code

1) Open a terminal at the "SMTSolvers" directory with Python installed

2) Run the following command to create a virtual environment:
	python3 -m venv venv

3) Run the following command to activate the virtual environment:
	source venv/bin/activate

6) Open the root directory "SMTSolvers" in VS Code

7) Press Ctrl+Shift+P and select "Python: Select Interpreter"

8) Select "Python 3.12.3('venv')./venv/bin/python"

9) In the same terminal, run the following command to install all dependencies:
	pip install -r requirements.txt

10) Run main/comparative_analysis.ipynb


File structure:
SMTSolvers
--main
----crt_components
----results
----tests
----comparative_analysis.ipynb
----crt_solver.py
----cvc5_solver.py
----z3_solver.py
--venv
--README.txt
--requirements.txt
