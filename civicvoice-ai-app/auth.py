import csv
import os
import hashlib
import datetime
import json

USERS_CSV = "users.csv"
ADMIN_CONFIG = "admin_config.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    if not os.path.exists(USERS_CSV):
        return False
    with open(USERS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == username:
                return True
    return False

def signup_user(username, password):
    if user_exists(username):
        return False
    hashed = hash_password(password)
    with open(USERS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, hashed])
    return True

def login_user(username, password):
    if not os.path.exists(USERS_CSV):
        return False
    hashed = hash_password(password)
    with open(USERS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == username and row[1] == hashed:
                return True
    return False

def log_login(username):
    with open("login_log.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, datetime.datetime.now().isoformat()])

def get_admin_credentials():
    if not os.path.exists(ADMIN_CONFIG):
        return None, None
    with open(ADMIN_CONFIG, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("username", "admin"), data.get("password_hash", None)

def set_admin_password(password):
    data = {"username": "admin", "password_hash": hash_password(password)}
    with open(ADMIN_CONFIG, "w", encoding="utf-8") as f:
        json.dump(data, f)

def admin_login(password):
    username, password_hash = get_admin_credentials()
    if not password_hash:
        return False
    return hash_password(password) == password_hash 