import firebase_admin
from firebase_admin import auth, credentials, db, exceptions
import bcrypt
import qrcode
import io
import base64
from cryptography.fernet import Fernet
from services.authentication import decrypt_value
import os
import sys

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("/crendential.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://banklink-2025-default-rtdb.firebaseio.com/'
    })

# Encryption Key Setup
ENCRYPTION_KEY_PATH = "/encryption_key.key"

def generate_encryption_key():
    """Generates a new encryption key and saves it to a file if it doesn't exist."""
    if not os.path.exists(ENCRYPTION_KEY_PATH):
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_PATH, "wb") as key_file:
            key_file.write(key)
    else:
        with open(ENCRYPTION_KEY_PATH, "rb") as key_file:
            key = key_file.read()
    return key

# Load or generate encryption key
ENCRYPTION_KEY = generate_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_sensitive_data(data):
    """Encrypts sensitive data like mobile and account numbers."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data):
    """Decrypts sensitive data."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

def register_user(email, password):
    """Registers a user in Firebase Authentication and returns UID."""
    try:
        # Check if user already exists
        existing_user = auth.get_user_by_email(email)
        print(f" User with email {email} already exists.")
        return existing_user.uid  # Return only UID, not password

    except auth.UserNotFoundError:
        # Create new user
        try:
            user = auth.create_user(email=email, password=password)
            return user.uid  #  Return only UID
        except Exception as e:
            print(f" Error registering user: {e}")
            return None

    except Exception as e:
        print(f" Firebase Authentication Error: {e}")
        return None



def store_user_details(uid, email, name, address, mobile, balance, account_number, password):
    """Stores encrypted user details in Firebase Realtime Database."""
    if uid is None:
        print(" Invalid UID. User data will not be stored.")
        return False

    try:
        encrypted_mobile = encrypt_sensitive_data(mobile)
        encrypted_account = encrypt_sensitive_data(account_number)
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Generate QR Code
        qr_data = f"Account: {account_number}\nMobile: {mobile}"
        qr = qrcode.make(qr_data)

        # Convert QR code to Base64
        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode("utf-8")

        # Ensure only UID is used in the database path
        ref = db.reference(f'/users/{uid}')
        ref.set({
            'name': name,
            'address': address,
            'email': email,
            'mobile': encrypted_mobile,
            'balance': balance,
            'account_number': encrypted_account,
            'password': hashed_password,
            'qr_code': qr_base64
        })

        print("User details stored successfully in Firebase.")
        return True

    except Exception as e:
        print(f" Error storing user details: {e}")
        return False

def authenticate_user(user_input, password):
    """Authenticates user by checking Firebase Authentication and Realtime Database."""
    try:
        #  Retrieve user from Firebase Authentication
        user = auth.get_user_by_email(user_input)
        uid = user.uid

        #  Retrieve user details from Realtime Database
        users_ref = db.reference(f'/users/{uid}')
        user_data = users_ref.get()

        if not user_data:
            print(" User data not found in database.")
            return None

        # Verify hashed password
        stored_hashed_password = user_data.get("password")
        if not bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
            print(" Incorrect password.")
            return None

        print("Authentication successful.")
        return {"uid": uid, "email": user_data.get("email")}

    except auth.UserNotFoundError:
        print(" User not found in Firebase Authentication.")
        return None

    except Exception as e:
        print(f" Firebase Authentication Error: {e}")
        return None


def reset_password(email):
    """Sends a password reset email to the user."""
    try:
        auth.generate_password_reset_link(email)
        print(f"Password reset email sent to {email}")
        return True
    except exceptions.FirebaseError as e:
        print(f"Error sending password reset email: {e}")
        return False

def get_account_number(user_id):
    """Fetches the account number for a given user ID from Firebase."""
    try:
        ref = db.reference(f"/users/{user_id}/account_number")
        encrypt_account_number = ref.get()
        account_number = decrypt_value(encrypt_account_number)
        return account_number if account_number else None
    except Exception as e:
        print(f" Firebase Error: {e}")
        return None

def resource_path(relative_path):
    """ Get absolute path to resource, works for development and PyInstaller EXE """
    try:
        base_path = sys._MEIPASS  # Temporary folder used by PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Normal development mode

    return os.path.join(base_path, relative_path)
