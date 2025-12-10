# bad_python.py
# Sample Python file with common issues

import os, sys  # unused imports

def dangerous_function(x):
    # TODO: Handle invalid input
    eval("print(x)")  # SECURITY: using eval
    if x > 10:
        print("Large value")
    else:
        print("Small value")

def long_function():
    total = 0
    for i in range(1000):
        total += i
        if i % 100 == 0:
            print(i)
    return total
