from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp
import sqlite3

class UpdateUserInfoScreen(Screen):
    account_number = StringProperty("")  # Store user's account number

    def set_account_number(self, account_number):
        """Set the current user's account number when navigating to this screen."""
        self.account_number = account_number

    def update_user_info(self, field, new_value):
        """Update user information in the database."""
        if not self.account_number:
            self.ids.status_label.text = "Account number not set!"
            return

        with sqlite3.connect("banklink.db") as conn:
            cursor = conn.cursor()
            query = f"UPDATE users SET {field} = ? WHERE account_number = ?"
            cursor.execute(query, (new_value, self.account_number))
            conn.commit()
            self.ids.status_label.text = f"{field.replace('_', ' ').title()} updated successfully!"

    def change_pin(self, new_pin):
        """Change user's PIN."""
        if len(new_pin) != 4 or not new_pin.isdigit():
            self.ids.status_label.text = "Invalid PIN! Must be 4 digits."
            return
        self.update_user_info("pin", new_pin)

    def change_mobile(self, new_mobile):
        """Change user's mobile number."""
        if len(new_mobile) != 10 or not new_mobile.isdigit():
            self.ids.status_label.text = "Invalid mobile number! Must be 10 digits."
            return
        self.update_user_info("mobile_number", new_mobile)

    def change_name(self, new_name):
        """Change user's name."""
        if not new_name.strip():
            self.ids.status_label.text = "Name cannot be empty!"
            return
        self.update_user_info("name", new_name)

    def change_address(self, new_address):
        """Change user's address."""
        if not new_address.strip():
            self.ids.status_label.text = "Address cannot be empty!"
            return
        self.update_user_info("address", new_address)
