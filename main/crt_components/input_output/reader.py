import cvc5
from cvc5 import Kind
from pathlib import Path
import re

# Case 1: match opening bracket
# Case 2: match closing bracket
# Case 3: match any sequence not containing whitespace or brackets
PATTERN = r"\(|\)|[^\s()]+"

def preprocess(input, API, terms):
    ast = tokenize_and_parse(input)
    create_constants(ast, API, terms)
    return ast

def tokenize_and_parse(input):
    code = input.read()
    tokens = tokenize(code)
    return parse(tokens)

def tokenize(code):
    token_stream = re.findall(PATTERN, code)
    #print(token_stream)
    return token_stream

def parse(tokens):
    # Stack-based iterative approach - O(n) time + space complexity
    tree = [[]] # contains wrapper list

    for token in tokens:
        if token == "(":
            # start new subtree
            tree.append([])
        elif token == ")":
            # append to previous subtree
            subTree = tree.pop()
            tree[-1].append(subTree)
        else:
            # append to current subtree
            tree[-1].append(token)

    ast = tree[0] # remove wrapper list
    #print(ast)
    return ast

def get_sorted_files(root):
    # O(n) scan, O(n log n) sort --> O(n log n)
    root = Path(root)
    files = root.rglob("*.smt2") # recursively scan all subdirectories + files for smt2
    sorted_files = sorted(files, key=lambda file: int(file.stem)) # sort in ascending numerical order
    return sorted_files

def create_constants(ast, API, terms):
    sort = API.tm.getIntegerSort()
    for subtree in ast:
        if subtree[0] == "declare-const":
            # Create constant and add to dictionary
            name = subtree[1]
            const = API.tm.mkConst(sort, name)
            terms.vars[name] = const
