import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from Pages.dashboard import DashboardScreen

# Set the app window size (optional, for testing)
Window.size = (360, 640)

# Define theme colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple (#4B0082)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)  # Light Purple (#9370DB)
ACCENT_COLOR = (1, 1, 1, 1)  # White (#FFFFFF)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray (#333333)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Main layout
        layout = FloatLayout()

        # Background Image
        background = Image(source='background.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Input fields container
        input_layout = BoxLayout(orientation='vertical', spacing=15, padding=30, size_hint=(0.9, 0.6),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Logo
        logo = Image(
            source='Pages/assets/Bank.png',
            size_hint=(None, None),  # Disable size_hint
            size=(400, 400),  # Set absolute size
            allow_stretch=True,  # Allow stretching
            keep_ratio=False,  # Disable aspect ratio
            pos_hint={'center_x': 0.5}
        )
        input_layout.add_widget(logo)

        # Account Number / Mobile Input
        self.account_input = TextInput(
            hint_text="Account Number or Mobile Number",
            multiline=False,
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_active='',
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.account_input)

        # Password Input
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_active='',
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.password_input)

        # Login Button
        login_button = Button(
            text="Login",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=PRIMARY_COLOR,
            color=ACCENT_COLOR,
            font_size=18,
            bold=True
        )
        login_button.bind(on_press=self.login)
        input_layout.add_widget(login_button)

        # Forgot Password and Create Account Links
        links_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=30,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.1})

        forgot_password = Button(
            text="Forgot Password?",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=SECONDARY_COLOR,
            font_size=14
        )
        forgot_password.bind(on_press=self.switch_to_forgot_password)

        create_account = Button(
            text="Create New Account",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=SECONDARY_COLOR,
            font_size=14
        )
        create_account.bind(on_press=self.switch_to_create_account)

        links_layout.add_widget(forgot_password)
        links_layout.add_widget(create_account)

        layout.add_widget(input_layout)
        layout.add_widget(links_layout)

        self.add_widget(layout)

    def switch_to_create_account(self, instance):
        self.manager.current = 'create_account'

    def login(self, instance):
        """Handles user login with SQLite authentication"""
        user_input = self.account_input.text.strip()
        password = self.password_input.text.strip()

        if not user_input or not password:
            self.show_error_popup("Error", "Please fill in all fields.")
            return

        user_data = self.authenticate_user(user_input, password)  # Fetch full user data

        if user_data:  # Ensure user_data is not None
            print("Login successful!")

            # Remove existing dashboard if it already exists
            if self.manager.has_screen('dashboard'):
                self.manager.remove_widget(self.manager.get_screen('dashboard'))

            # Create DashboardScreen with user data
            dashboard_screen = DashboardScreen(user_data=user_data, name='dashboard')
            self.manager.add_widget(dashboard_screen)
            self.manager.current = 'dashboard'
        else:
            self.show_error_popup("Login Failed", "Invalid account number, mobile number, or password.")

    def authenticate_user(self, user_input, password):
        """Authenticate user and return their full details"""
        try:
            conn = sqlite3.connect("banklink.db")  # Connect to the database
            cursor = conn.cursor()

            # Fetch user details where account number or mobile matches and password is correct
            cursor.execute(
                "SELECT account_number, name, address, mobile FROM users WHERE (account_number = ? OR mobile = ?) AND password = ?",
                (user_input, user_input, password)
            )
            result = cursor.fetchone()
            conn.close()

            if result:  # If user exists
                return {
                    "account_number": result[0],
                    "name": result[1],
                    "address": result[2],
                    "mobile": result[3]
                }
            return None  # If no match found, return None
        except sqlite3.Error as e:
            print("Database error:", e)
            return None

    def switch_to_forgot_password(self, instance):
        self.manager.current = 'forgot_password'