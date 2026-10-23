import os
import sqlite3
import hashlib
import pickle
from flask import Flask, request

app = Flask(__name__)

# 🚨 SECURITY FLAW 1: Hardcoded Cloud Credentials & API Secret
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
JWT_SECRET_KEY = "super_secret_jwt_private_key_12345"

# 🚨 SECURITY FLAW 2: Broken Cryptographic Hash Algorithm (MD5)
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# 🚨 SECURITY FLAW 3: SQL Injection Vulnerability
@app.route("/api/login", methods=["POST"])
def user_login():
    username = request.form.get("username")
    password = request.form.get("password")
    pwd_hash = hash_password(password)

    conn = sqlite3.connect("production_users.db")
    cursor = conn.cursor()
    # DANGEROUS: String formatting in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{pwd_hash}'"
    cursor.execute(query)
    user = cursor.fetchone()
    return {"status": "authenticated", "user": user}

# 🚨 SECURITY FLAW 4: Command Injection / Remote Code Execution (RCE)
@app.route("/api/network/ping", methods=["GET"])
def ping_service():
    host = request.args.get("host", "127.0.0.1")
    # DANGEROUS: User input passed directly to OS shell
    os.system(f"ping -c 1 {host}")
    return {"message": "ping completed"}

# 🚨 SECURITY FLAW 5: Insecure Deserialization
@app.route("/api/session/restore", methods=["POST"])
def restore_session():
    cookie_token = request.cookies.get("session_token")
    # DANGEROUS: Unsafe pickle deserialization allows arbitrary code execution
    session_data = pickle.loads(cookie_token.encode())
    return {"session": session_data}

if __name__ == "__main__":
    app.run(port=5000)
