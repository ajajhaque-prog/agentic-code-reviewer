# test_file_b.py
# Contains critical and high severity patterns

# CRITICAL - unsafe eval
expr = "print('hi')"
eval(expr)

# HIGH - bare except
try:
    x = 1 / 0
except:
    pass

def f():
    pass
