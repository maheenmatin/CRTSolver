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
    def extract_dir_no(dir_name):
        match = re.match(r"(\d+)", dir_name)
        number = (match.group(1)) # first group of re.match()
        return int(number) # convert to int before returning

    root = Path(root)
    sorted_files = []

    var_dirs = [dir for dir in root.iterdir() if dir.is_dir()]
    var_dirs = sorted(var_dirs, key=lambda dir: extract_dir_no(dir.name))

    for var_dir in var_dirs:
        deg_dirs = [dir for dir in var_dir.iterdir() if dir.is_dir()]
        deg_dirs = sorted(deg_dirs, key=lambda dir: extract_dir_no(dir.name))

        for deg_dir in deg_dirs:
            files = deg_dir.glob("*.smt2")
            sorted_files.extend(files) # append each item from the iterable separately

    return sorted_files

def create_constants(ast, API, terms):
    sort = API.tm.getIntegerSort()
    for subtree in ast:
        if subtree[0] == "declare-const":
            # Create constant and add to dictionary
            name = subtree[1]
            const = API.tm.mkConst(sort, name)
            terms.vars[name] = const
