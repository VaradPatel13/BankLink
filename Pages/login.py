import hashlib
import firebase_admin
from firebase_admin import auth, credentials
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from services.authentication import verify_user_credentials

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("./services/crendential.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://banklink-2025-default-rtdb.firebaseio.com/"
    })

# Set the app window size
Window.size = (360, 640)

# Define theme colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)
ACCENT_COLOR = (1, 1, 1, 1)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)

def hash_sha256(value):
    """Hashes the given value using SHA-256."""
    return hashlib.sha256(value.encode()).hexdigest()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        # Background Image
        background = Image(source='background.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Input fields container
        input_layout = BoxLayout(orientation='vertical', spacing=15, padding=30, size_hint=(0.9, 0.6),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Logo
        logo = Image(
            source='Pages/assets/Images/Bank.png',
            size_hint=(None, None),
            size=(400, 400),
            allow_stretch=True,
            keep_ratio=False,
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
        self.login_button = Button(
            text="Login",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=PRIMARY_COLOR,
            color=ACCENT_COLOR,
            font_size=18,
            bold=True
        )
        self.login_button.bind(on_press=self.login)
        input_layout.add_widget(self.login_button)

        # Loader
        self.loader = MDProgressBar(size_hint_x=0.9, pos_hint={'center_x': 0.5}, opacity=0)
        layout.add_widget(self.loader)

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

    def switch_to_forgot_password(self, instance):
        self.manager.current = 'forgot_password'

    def login(self, instance):
        """Handles user login with Firebase Authentication"""
        user_input = self.account_input.text.strip()
        password = self.password_input.text.strip()

        if not user_input or not password:
            self.show_error_dialog("Error", "Please fill in all fields.")
            return

        self.login_button.text = "Logging in..."
        self.login_button.disabled = True
        self.loader.opacity = 1

        # Call authenticate_user after a small delay to simulate loading
        Clock.schedule_once(lambda dt: self.authenticate_user(user_input, password), 1)

    def authenticate_user(self, user_input, password):
        """Handles login authentication with Firebase and error handling."""
        try:
            result = verify_user_credentials(user_input, password)

            if result["success"]:
                # print(f" Login successful! User ID: {result['uid']}")
                self.login_success(result['uid'], 'customer')
                self.go_to_dashboard(result["uid"])
            else:
                self.handle_firebase_errors(result["message"])
                self.enable_login_button()

        except firebase_admin.auth.AuthError as e:
            self.handle_firebase_errors(str(e))
            self.enable_login_button()

    def handle_firebase_errors(self, error_message):
        error_messages = {
            "auth/invalid-email": "Invalid email format. Please enter a valid email.",
            "auth/user-disabled": "Your account has been disabled. Contact support.",
            "auth/user-not-found": "User not found. Please check your credentials.",
            "auth/wrong-password": "Incorrect password. Try again.",
            "auth/too-many-requests": "Too many failed attempts. Try again later.",
            "auth/network-request-failed": "Network error. Check your internet connection.",
            "auth/invalid-credential": "Invalid login credentials.",
            "auth/missing-password": "Password field cannot be empty.",
            "auth/operation-not-allowed": "Login method not enabled. Contact admin.",
        }

        user_friendly_message = error_messages.get(error_message, "Login failed. Please try again.")
        self.show_error_dialog("Login Error", user_friendly_message)

    def login_success(self, user_id, role):
        """Call this function after successful authentication."""
        from services.session_manager import start_session
        start_session(user_id, role)
        print("User logged in and session started.")

    def enable_login_button(self):
        """Re-enables the login button and hides the loader."""
        self.login_button.text = "Login"
        self.login_button.disabled = False
        self.loader.opacity = 0

    def go_to_dashboard(self, uid):
        """Navigates to the dashboard screen with user details."""
        from Pages.dashboard import DashboardScreen

        if not self.manager.has_screen('dashboard'):
            dashboard = DashboardScreen(name='dashboard')
            self.manager.add_widget(dashboard)

        dashboard = self.manager.get_screen('dashboard')
        dashboard.user_id = uid
        self.manager.current = 'dashboard'

    def show_error_dialog(self, title, message):
        """Displays an error dialog with the given title and message."""
        dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, None),
            buttons=[
                Button(text="OK", on_press=lambda x: dialog.dismiss(), size_hint=(1, 0.5), background_color=(0.8, 0, 0, 1))
            ]
        )
        dialog.open()
