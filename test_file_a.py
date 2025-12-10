# test_file_a.py
# Contains flake8, todo, and medium severity issues

import os  # unused import - flake8 F401

# TODO: Add docstrings and tests.

def big_function():
    # long function to trigger medium severity
    for i in range(80):
        print(i)

def ok():
    print("ok")
