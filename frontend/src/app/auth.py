import os
import json
import hashlib
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "users.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f).get("users", [])

def save_user(user):
    users = load_users()
    users.append(user)
    with open(DATA_FILE, "w") as f:
        json.dump({"users": users}, f, indent=4)

def user_exists(username, email):
    return any(u["username"] == username or u["email"] == email for u in load_users())

def verify_credentials(identifier, password):
    password = hash_password(password)
    users = load_users()
    print(f"🔍 Buscando: {identifier} con password hash {password}")
    for u in users:
        print(f"👤 Revisando: {u['username']} / {u['email']}")
        if (u["username"] == identifier or u["email"] == identifier) and u["password"] == password:
            print("✅ Login válido")
            return True
    print("❌ Login inválido")
    return False

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    return (
        8 <= len(password) <= 12 and
        any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password) and
        '@' in password
    )

def get_user_by_identifier(identifier):
    passwordless = lambda u: {k: u[k] for k in u if k != "password"}
    for u in load_users():
        if u["username"] == identifier or u["email"] == identifier:
            return passwordless(u)
    return None
