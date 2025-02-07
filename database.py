import sqlite3
import random

# Database file
DB_NAME = "banklink.db"


def initialize_database():
    """Creates the users table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            mobile TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def generate_account_number():
    """Generates a unique 10-digit account number."""
    return str(random.randint(1000000000, 9999999999))


def add_user(name, address, mobile, password, initial_balance):
    """Adds a new user to the database and returns the account number."""
    initialize_database()  # Ensure table exists

    account_number = generate_account_number()

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (account_number, name, address, mobile, password, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (account_number, name, address, mobile, password, initial_balance))

        conn.commit()
        conn.close()

        return account_number  # Return generated account number
    except sqlite3.IntegrityError:
        return None  # Mobile number already exists


def get_user(account_number):
    """Retrieves a user's details from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE account_number = ?", (account_number,))
    user = cursor.fetchone()

    conn.close()
    return user
