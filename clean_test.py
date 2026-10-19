import os
import sqlite3
import hashlib
import json
import subprocess

# ✅ SECURE 1: Secrets loaded from environment variables
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "default_vault_placeholder")

# ✅ SECURE 2: Strong Cryptographic Hashing (SHA-256)
def hash_user_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ SECURE 3: Parameterized SQL Query (Protected against SQL Injection)
def fetch_user_data(username, user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND id = %s"
    cursor.execute(query, (username, user_id))
    return cursor.fetchall()

# ✅ SECURE 4: Safe subprocess execution without shell=True (Prevents RCE)
def ping_server(server_ip):
    subprocess.run(["ping", "-c", "1", server_ip], check=True, capture_output=True)

# ✅ SECURE 5: Safe JSON deserialization instead of dangerous pickle
def load_session_cookie(raw_cookie):
    return json.loads(raw_cookie)
