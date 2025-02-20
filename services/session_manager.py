import os
import json

SESSION_FILE = "session.txt"  # File to store session details

def start_session(user_id, role):
    """Start a session by saving user ID and role to a file."""
    session_data = {
        "user_id": user_id,
        "role": role
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f)
    print(f"Session started for User ID: {user_id}")

def get_session():
    """Retrieve session data if available."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

def clear_session():
    """Clear session data to log out the user."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    print("User logged out. Session cleared.")
