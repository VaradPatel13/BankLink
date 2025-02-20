# import sqlite3
#
# # Database file
# DB_NAME = "banklinkdemo.db"
#
# # Theme Colors (ANSI Escape Codes)
# PRIMARY_COLOR = "\033[38;2;74;0;130m"  # Dark Purple (#4B0082)
# SECONDARY_COLOR = "\033[38;2;148;112;219m"  # Light Purple (#9370DB)
# ACCENT_COLOR = "\033[38;2;255;255;255m"  # White (#FFFFFF)
# TEXT_COLOR = "\033[38;2;51;51;51m"  # Dark Gray (#333333)
# RESET = "\033[0m"
#
#
# def view_all_users():
#     """Fetch and display all users from the database with themed styling."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#
#     # Fetch column names dynamically
#     cursor.execute("PRAGMA table_info(users)")
#     columns_info = cursor.fetchall()
#     column_names = [col[1] for col in columns_info]  # Extract column names
#
#     # Fetch all users
#     cursor.execute(f"SELECT * FROM users")
#     users = cursor.fetchall()
#     conn.close()
#
#     if not users:
#         print(f"{PRIMARY_COLOR}No users found in the database.{RESET}")
#         return
#
#     # Header Section
#     print(f"\n{PRIMARY_COLOR}📌 All Registered Users 📌{RESET}")
#     print(f"{PRIMARY_COLOR}{'-' * 80}{RESET}")
#
#     # Print Column Headers
#     print(f"{SECONDARY_COLOR}{' | '.join(column_names)}{RESET}")
#     print(f"{PRIMARY_COLOR}{'-' * 80}{RESET}")
#
#     # Print User Data Rows
#     for user in users:
#         print(f"{TEXT_COLOR}{' | '.join(map(str, user))}{RESET}")
#
#     print(f"{PRIMARY_COLOR}{'-' * 80}{RESET}\n")
#
#
# def delete_all_users():
#     """Delete all records from the users table after confirmation."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#
#     confirmation = input(f"{PRIMARY_COLOR}Are you sure you want to delete ALL user records? (yes/no): {RESET}").strip().lower()
#
#     if confirmation == "yes":
#         try:
#             cursor.execute("DELETE FROM users")
#             conn.commit()
#             print(f"{ACCENT_COLOR}All user records have been deleted successfully!{RESET}")
#         except sqlite3.Error as e:
#             print(f"{PRIMARY_COLOR}Database error: {e}{RESET}")
#         finally:
#             conn.close()
#     else:
#         print(f"{SECONDARY_COLOR}Operation canceled. No records were deleted.{RESET}")
#
#
# def drop_users_table():
#     """Drop the users table from the database after confirmation."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#
#     confirmation = input(f"{PRIMARY_COLOR}Are you sure you want to DROP the 'users' table? This action is irreversible! (yes/no): {RESET}").strip().lower()
#
#     if confirmation == "yes":
#         try:
#             cursor.execute("DROP TABLE IF EXISTS users")
#             conn.commit()
#             print(f"{ACCENT_COLOR}The 'users' table has been dropped successfully!{RESET}")
#         except sqlite3.Error as e:
#             print(f"{PRIMARY_COLOR}Database error: {e}{RESET}")
#         finally:
#             conn.close()
#     else:
#         print(f"{SECONDARY_COLOR}Operation canceled. The table was not dropped.{RESET}")
#
# import bcrypt
#
# from cryptography.fernet import Fernet
#
# # # Generate a new Fernet key
# # new_key = Fernet.generate_key()
# # print("Generated Fernet Key:", new_key.decode())
#
#
# hashed_password = b"$2b$12$HnBwiegOCEftHvsZpTITB.v4zE31JK1RmefaSofkOXFSpovW1drum"
# user_input = input("Enter password: ").encode()
#
# if bcrypt.checkpw(user_input, hashed_password):
#     print("✅ Password matches!")
# else:
#     print("❌ Incorrect password.")
#
# import bcrypt
#
# def hash_password(password: str) -> str:
#     # Generate a salt
#     salt = bcrypt.gensalt()
#     # Hash the password
#     hashed_password = bcrypt.hashpw(password.encode(), salt)
#     return hashed_password.decode()  # Return as a string
#
# def verify_password(password: str, hashed_password: str) -> bool:
#     # Compare the provided password with the stored hash
#     return bcrypt.checkpw(password.encode(), hashed_password.encode())

import os
from ctypes import cdll

dll_path = r"D:\Downloads\BankLink\Banklink_Desktop\.venv\Lib\site-packages\pyzbar\libzbar-64.dll"

if os.path.exists(dll_path):
    try:
        cdll.LoadLibrary(dll_path)
        print("libzbar loaded successfully!")
    except OSError as e:
        print(f"Error loading libzbar: {e}")
else:
    print("libzbar-64.dll not found in expected location.")

#
# # Example usage
# plain_password = "123456"
# hashed = hash_password(plain_password)
# print("Hashed Password:", hashed)
#
# # Verify password
# is_valid = verify_password(plain_password, hashed)
# print("Password Match:", is_valid)

#
# if __name__ == "__main__":
#     view_all_users()
#     delete_all_users()
#     drop_users_table()
