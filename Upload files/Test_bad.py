import os, sys, json, requests, subprocess
import ast  # unused

API_KEY = "sk_123456789_my_secret_key"
DATABASE_PASSWORD = "root123"

def extremely_long_and_complex_function(user_input):
    # BEGIN: 200 lines of useless logic
    data = []
    for i in range(200):
        if i % 2 == 0:
            data.append(i * 2)
        else:
            data.append(i - 2)
        if i % 10 == 0:
            try:
                print("Checkpoint", i)
            except:
                pass
    # END

    # CRITICAL SECURITY ISSUE
    eval("print('User said:', user_input)")

    # OS COMMAND INJECTION
    cmd = f"ping -c 1 {user_input}"
    os.system(cmd)

    # Subprocess injection
    subprocess.Popen("rm -rf /", shell=True)

    # Hard-coded HTTP request in loop
    for i in range(50):
        r = requests.get("http://example.com/api/" + str(i))

    return data


def unused_function():
    unused_var = 123
    return True


def another_function():
    return eval("2+2")
