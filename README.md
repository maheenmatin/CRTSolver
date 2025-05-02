# CRTSolver Setup Guide

## **Prerequisites**

Ensure the following are installed on your system:

- **Linux**
- **Python 3**
- **Jupyter Notebook**
- **Visual Studio Code**
- **Python and Jupyter extensions for Visual Studio Code**

---

## **Setup Instructions**

### 1. Open a terminal at the project root directory

```bash
cd /path/to/CRTSolver
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install all dependencies

```bash
pip install -r requirements.txt
```

### 5. Open the project in VS Code

```bash
code .
```

### 6. Select the Python interpreter

1. Press `Ctrl+Shift+P`
2. Select the option: `Python: Select Interpreter`
3. Select the interpreter: `Python 3.x.x ('venv') ./venv/bin/python`

### 7. Run the Jupyter Notebook

1. Open `main/comparative_analysis.ipynb` 
2. Select `Select Kernel`
3. Select the option `Python Environments...`
4. Select the option: `Python 3.x.x ('venv') ./venv/bin/python`
5. Select `Run All`

---

## **Project File Structure**

```plaintext
CRTSolver/
├── main/
│   ├── crt_components/
│   ├── results/
│   ├── tests/
│   ├── comparative_analysis.ipynb
│   ├── crt_solver.py
│   ├── cvc5_solver.py
│   └── z3_solver.py
├── venv/
├── README.txt
└── requirements.txt
```
