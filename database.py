import sqlite3
import os
from datetime import datetime
import hashlib

# sqlite is the easiest for local storage
DB_FILE = "expense_tracker.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # expenses table linked to user
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def _hash_password(password: str) -> str:
    # simple hashing for passwords
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                       (username, _hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # username taken
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", 
                   (username, _hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def add_expense(user_id, amount, description, category):
    conn = get_connection()
    cursor = conn.cursor()
    
    # get current timestamp for the expense
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO expenses (user_id, amount, description, category, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, amount, description, category, date_str))
    
    conn.commit()
    conn.close()

def get_expenses(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # fetch user's expenses sorted by newest first
    cursor.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(ix) for ix in rows]
