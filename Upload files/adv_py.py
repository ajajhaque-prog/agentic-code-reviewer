# Advanced Python: async misuse, JWT, SQL injection, wrong locking
import asyncio, threading, jwt, sqlite3

SECRET = "ADV_SECRET_ABC"

def dangerous_sql(user_input):
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    q = "SELECT * FROM accounts WHERE name = '%s'" % user_input
    cur.execute(q)
    return cur.fetchall()

async def bad_async():
    # creating tasks but not awaiting results correctly
    tasks = [asyncio.create_task(asyncio.sleep(i)) for i in range(5)]
    for t in tasks:
        pass  # forgot await

def jwt_verify(token):
    # naive decode without verification
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload

lock = threading.Lock()
shared = 0
def race():
    global shared
    for i in range(1000):
        shared += 1  # missing lock acquisition
