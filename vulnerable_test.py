import os
import sqlite3
import hashlib
import pickle

# 🚨 VULNERABILITY 1: Hardcoded AWS Secret Key (Secret Leak)
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# 🚨 VULNERABILITY 2: Weak Cryptographic Hashing (MD5 is broken)
def hash_user_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# 🚨 VULNERABILITY 3: SQL Injection (Unsanitized user string concatenation)
def fetch_user_data(username, user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

# 🚨 VULNERABILITY 4: Remote Code Execution (RCE) / Command Injection
def ping_server(server_ip):
    os.system("ping " + server_ip)

# 🚨 VULNERABILITY 5: Insecure Deserialization (Pickle allows arbitrary code execution)
def load_session_cookie(raw_cookie):
    return pickle.loads(raw_cookie.encode())
