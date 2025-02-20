from services.firebase_config import get_db_reference



def add_user(name, address, mobile, password, initial_amount):
    """Saves user data in Firebase Realtime Database."""
    ref = get_db_reference().child('users')  # Reference to 'users' collection

    # Check if mobile number is already registered
    users = ref.get()
    if users:
        for user_id, user_data in users.items():
            if user_data['mobile'] == mobile:
                return None  # Mobile number already registered

    # Generate account number (random 8-digit)
    account_number = str(random.randint(10000000, 99999999))

    # User data dictionary
    user_data = {
        "name": name,
        "address": address,
        "mobile": mobile,
        "password": password,  # In production, hash this
        "balance": initial_amount,
        "account_number": account_number
    }

    # Save to Firebase
    ref.child(account_number).set(user_data)

    return account_number  # Return the new account number
