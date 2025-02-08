import sqlite3
import random
import qrcode
import os
from PIL import Image

# Database file
DB_NAME = "banklinkdemo.db"
QR_CODE_FOLDER = "qr_codes"

def initialize_database():
    """Creates the users table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            address TEXT,
            mobile TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL NOT NULL,
            qr_code TEXT  -- Stores the file path
        )
    ''')

    conn.commit()
    conn.close()

    # Ensure the QR code directory exists
    if not os.path.exists(QR_CODE_FOLDER):
        os.makedirs(QR_CODE_FOLDER)

def generate_account_number():
    """Generates a unique 10-digit account number."""
    return str(random.randint(1000000000, 9999999999))

def generate_qr_code(account_number, mobile):
    """Generate and save a QR code containing the account number and mobile number."""
    qr_data = f"Account: {account_number}, Mobile: {mobile}"
    qr = qrcode.make(qr_data)

    # Define the file path with correct syntax
    file_path = os.path.join(r"D:\Downloads\BankLink\Banklink_Desktop\Pages\assets\qr_codes", f"{account_number}.png")

    # Save the QR code as an image file
    qr.save(file_path, format="PNG")

    return file_path  # Return the file path instead of binary data

def add_user(name, address, mobile, password, initial_balance):
    """Adds a new user to the database and returns the account number."""
    initialize_database()  # Ensure table exists

    account_number = generate_account_number()
    qr_code_path = generate_qr_code(account_number, mobile)  # Generate QR Code and save as file

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (account_number, name, address, mobile, password, balance, qr_code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (account_number, name, address, mobile, password, initial_balance, qr_code_path))

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

def get_qr_code(account_number):
    """Retrieve the QR code file path for a given account number and display it."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT qr_code FROM users WHERE account_number = ?", (account_number,))
    row = cursor.fetchone()

    conn.close()

    if row and row[0]:  # If QR code exists
        qr_image = Image.open(row[0])  # Open QR code from file path
        qr_image.show()  # Show QR code image
    else:
        print("QR Code not found!")
5