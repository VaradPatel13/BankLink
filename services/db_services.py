import firebase_admin
from firebase_admin import credentials, db

# Path to your Firebase service account key JSON file
CREDENTIAL_FILE_PATH = "D:\Downloads\BankLink\Banklink_Desktop\services\crendential.json"  # Update this to your credential file path

# Firebase Realtime Database URL
DATABASE_URL = "https://banklink2025-default-rtdb.asia-southeast1.firebasedatabase.app/"  # Update this with your database URL

def connect_to_firebase():
    """
    Connect to Firebase Realtime Database.
    """
    try:
        # Initialize the Firebase Admin SDK
        cred = credentials.Certificate(CREDENTIAL_FILE_PATH)
        firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
        print("Connected to Firebase Realtime Database!")
    except Exception as e:
        print(f"Error connecting to Firebase: {e}")

if __name__ == "__main__":
    # Connect to Firebase
    connect_to_firebase()
