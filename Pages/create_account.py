from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
import random
import time
import re
import bcrypt
from cryptography.fernet import Fernet
from services.firebase_config import register_user, store_user_details

# Font
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Then load your font:
font_path = resource_path(os.path.join("Pages", "assets", "Fonts", "Poppins-Bold.ttf"))

# Define theme colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
ACCENT_COLOR = (1, 1, 1, 1)  # White
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray
BUTTON_COLOR = PRIMARY_COLOR  # Uniform Button Color

# Encryption Key
ENCRYPTION_KEY = b'fTvxVcDZNOYAmt1D33OUwkFBdibYi_F0tN6Y_lOQTAk='
cipher_suite = Fernet(ENCRYPTION_KEY)


class CreateAccountScreen(Screen):
    def __init__(self, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.otp = None
        self.otp_sent_time = None
        self.create_layout()

    def create_layout(self):
        layout = FloatLayout()

        # Background Color
        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            layout.bind(size=self.update_rect, pos=self.update_rect)

        # Input fields container
        input_layout = BoxLayout(
            orientation='vertical',
            spacing=14,
            padding=25,
            size_hint=(0.9, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Title Label
        title_label = Label(
            text="Create New Account",
            font_size=26,
            font_name="Poppins",
            bold=True,
            color=PRIMARY_COLOR,
            size_hint=(1, None),
            height=50
        )
        input_layout.add_widget(title_label)

        # Input Fields
        self.name_input = self.create_text_input("Full Name")
        self.mobile_input = self.create_text_input("Mobile Number")
        self.email_input = self.create_text_input("Email")
        self.address_input = self.create_text_input("Address")
        self.otp_input = self.create_text_input("Enter OTP")
        self.password_input = self.create_text_input("Password", password=True)
        self.confirm_password_input = self.create_text_input("Confirm Password", password=True)

        input_layout.add_widget(self.name_input)
        input_layout.add_widget(self.mobile_input)
        input_layout.add_widget(self.email_input)
        input_layout.add_widget(self.address_input)
        input_layout.add_widget(self.otp_input)

        # Send OTP Button
        send_otp_button = self.create_button("Send OTP")
        send_otp_button.bind(on_press=self.send_otp)
        input_layout.add_widget(send_otp_button)

        input_layout.add_widget(self.password_input)
        input_layout.add_widget(self.confirm_password_input)

        # Create Account Button
        create_button = self.create_button("Create Account")
        create_button.bind(on_press=self.create_account)
        input_layout.add_widget(create_button)

        # Back Button
        back_button = self.create_button("Back to Login")
        back_button.bind(on_press=self.go_to_login)
        input_layout.add_widget(back_button)

        layout.add_widget(input_layout)
        self.add_widget(layout)

    def create_text_input(self, hint_text, password=False):
        """Creates a styled text input field."""
        return TextInput(
            hint_text=hint_text,
            size_hint=(1, None),
            height=55,
            font_size=17,
            font_name="Poppins",
            password=password,
            background_active='',
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=TEXT_COLOR,
            padding=(12, 12),
            cursor_color=PRIMARY_COLOR
        )

    def create_button(self, text):
        """Creates a styled button with the same color."""
        return Button(
            text=text,
            size_hint=(1, None),
            height=55,
            font_size=18,
            font_name="Poppins",
            background_normal='',
            background_color=BUTTON_COLOR,
            color=ACCENT_COLOR,
            bold=True
        )

    def send_otp(self, instance):
        """Generates and sends OTP to the user's mobile number."""
        mobile = self.mobile_input.text.strip()
        if not re.match(r'^\d{10}$', mobile):
            self.show_popup("Error", "Enter a valid 10-digit mobile number.")
            return

        self.otp = str(random.randint(100000, 999999))
        self.otp_sent_time = time.time()
        print(f"OTP sent to {mobile}: {self.otp}")
        self.show_popup("OTP Sent", f"OTP has been sent to {mobile}")

    def create_account(self, instance):
        """Handles account creation with validation and Firebase integration."""
        name = self.name_input.text.strip()
        mobile = self.mobile_input.text.strip()
        email = self.email_input.text.strip()
        address = self.address_input.text.strip()
        otp = self.otp_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        # Field Validations
        if not name:
            self.show_popup("Error", "Please enter your full name.")
            return
        if not re.match(r'^\d{10}$', mobile):
            self.show_popup("Error", "Enter a valid 10-digit mobile number.")
            return
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            self.show_popup("Error", "Enter a valid email address.")
            return
        if not address:
            self.show_popup("Error", "Please enter your address.")
            return
        if otp != self.otp or time.time() - self.otp_sent_time > 900:
            self.show_popup("Error", "Invalid or expired OTP.")
            return
        if len(password) < 6:
            self.show_popup("Error", "Password must be at least 6 characters.")
            return
        if password != confirm_password:
            self.show_popup("Error", "Passwords do not match.")
            return

        # Encrypt mobile number & Generate encrypted account number
        encrypted_mobile = cipher_suite.encrypt(mobile.encode()).decode()
        account_number = str(random.randint(1000000000, 9999999999))
        encrypted_account = cipher_suite.encrypt(account_number.encode()).decode()

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Register user in Firebase
        uid = register_user(email, hashed_password)
        if not uid:
            self.show_popup("Error", "User already exists or registration failed.")
            return

        # Store user details in Firebase
        success = store_user_details(uid, email, name, address, mobile, 1000.0, account_number, hashed_password)

        if success:
            self.show_popup("Success", f"Account created!\nYour Account Number: {account_number}")
            self.manager.current = 'login'
        else:
            self.show_popup("Error", "Failed to store user details. Try again.")

    def go_to_login(self, instance):
        """Navigates back to the Login screen."""
        self.manager.current = 'login'

    def show_popup(self, title, message):
        """Displays a popup with a message."""
        popup = Popup(
            title=title,
            content=Label(text=message, font_name="Poppins", color=TEXT_COLOR),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def update_rect(self, instance, value):
        """Updates background size when the window resizes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
