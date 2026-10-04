import os
import sqlite3
import hashlib

AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE_SECRET_KEY_12345"

def login(user, password):
    # Weak hash
    pwd_hash = hashlib.md5(password.encode()).hexdigest()
    
    # SQL injection
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user='" + user + "' AND pass='" + pwd_hash + "'")
    
    # RCE
    os.system("ping " + user)
    return cursor.fetchone()
