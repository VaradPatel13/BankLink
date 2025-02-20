import firebase_admin
from firebase_admin import auth, db
import bcrypt
from cryptography.fernet import Fernet
import re  # To check if input is an email

# 🔹 Ensure you use the same encryption key as when storing the data!
FERNET_KEY = b'fTvxVcDZNOYAmt1D33OUwkFBdibYi_F0tN6Y_lOQTAk='  # Replace with your actual Fernet key
cipher_suite = Fernet(FERNET_KEY)

def decrypt_value(encrypted_value):
    """Decrypts an encrypted value using Fernet."""
    try:
        decrypted = cipher_suite.decrypt(encrypted_value.encode()).decode()
        return decrypted
    except Exception as e:
        print(f"🔴 Decryption Error: {e}")  # Debugging print
        return None  # Return None if decryption fails

def is_email(user_input):
    """Checks if the input is a valid email address."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", user_input))

def verify_user_credentials(user_input, password):
    """Authenticates user using Firebase Authentication & Realtime Database."""
    uid = None  # Initialize UID

    if is_email(user_input):
        try:
            user = auth.get_user_by_email(user_input)
            uid = user.uid
        except auth.UserNotFoundError:
            pass  # Continue if email lookup fails

    if not uid:
        try:
            # 🔹 Step 2: Search in Realtime Database using decrypted values
            users_ref = db.reference('/users').get()
            if not users_ref:
                return {"success": False, "message": "🔥 No users found in database."}

            for key, user_data in users_ref.items():
                encrypted_mobile = user_data.get('mobile', '')
                encrypted_account = user_data.get('account_number', '')

                # 🔹 Decrypt stored values
                decrypted_mobile = decrypt_value(encrypted_mobile)
                decrypted_account = decrypt_value(encrypted_account)

                # 🔹 Debugging Prints
                print(f"👀 Checking User: {key}")
                print(f"   Encrypted Mobile: {encrypted_mobile}")
                print(f"   Decrypted Mobile: {decrypted_mobile}")
                print(f"   Encrypted Account: {encrypted_account}")
                print(f"   Decrypted Account: {decrypted_account}")

                if decrypted_mobile == user_input or decrypted_account == user_input:
                    uid = key
                    break

            if not uid:
                return {"success": False, "message": "❌ User not found (after decryption check)."}

        except Exception as e:
            return {"success": False, "message": f"🔥 Database Error: {e}"}

    # 🔹 Step 3: Retrieve user details from Firebase Database
    user_data = db.reference(f'/users/{uid}').get()
    if not user_data:
        return {"success": False, "message": "⚠️ User details not found."}

    # 🔹 Step 4: Debug Password Verification
    stored_hashed_password = user_data.get("password")

    if not stored_hashed_password:
        print(f"⚠️ No password found in database for user {uid}.")
        return {"success": False, "message": "⚠️ No password found in database."}

    # 🔍 Debugging: Print passwords for comparison (DO NOT KEEP IN PRODUCTION)
    print(f"🔍 Input Password: {password}")
    print(f"🔍 Hashed Password from Firebase: {stored_hashed_password}")

    # Convert stored password to bytes if it's not already
    if isinstance(stored_hashed_password, str):
        stored_hashed_password = stored_hashed_password.encode()

    # 🔍 Check if the password matches
    if bcrypt.checkpw(password.encode(), stored_hashed_password):
        print("✅ Password Matched!")
        return {"success": True, "uid": uid, "message": "✅ Login successful."}
    else:
        print("❌ Incorrect Password!")
        return {"success": False, "message": "❌ Incorrect password."}
