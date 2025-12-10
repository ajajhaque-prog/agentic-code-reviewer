# test_all_severities.py
"""
This file intentionally contains various issues
to test all severity levels of the Agentic Code Reviewer.
"""

# CRITICAL: Use of eval (unsafe)
code = "print('Hello')"
eval(code)

# HIGH: Bare except
try:
    print("Something risky")
except:
    pass

# MEDIUM: Long function
def long_function_example():
    # This function is intentionally long
    for i in range(70):
        print(i)
    return "done"

# LOW: TODO / unused import
import os  # unused import
# TODO: add proper docstrings and typing

# INFO: simple okay function
def hello():
    print("Hello world")
