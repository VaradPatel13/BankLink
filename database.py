import sqlite3
import random


# Database setup
def create_database():
    conn = sqlite3.connect('banklink.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    account_number TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    mobile TEXT NOT NULL,
                    password TEXT NOT NULL,
                    balance REAL NOT NULL
                )''')
    conn.commit()
    conn.close()


# Generate a unique 8-digit account number
def generate_account_number():
    return str(random.randint(10000000, 99999999))


# Add a new user to the database
def add_user(name, address, mobile, password, initial_amount):
    account_number = generate_account_number()
    conn = sqlite3.connect('banklink.db')
    c = conn.cursor()

    c.execute('''INSERT INTO users (account_number, name, address, mobile, password, balance)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (account_number, name, address, mobile, password, initial_amount))

    conn.commit()
    conn.close()
    return account_number


# Fetch user details for login
def get_user(account_number, password):
    conn = sqlite3.connect('banklink.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM users WHERE account_number = ? AND password = ?''',
              (account_number, password))
    user = c.fetchone()

    conn.close()
    return user


# Initialize the database when the app starts
create_database()