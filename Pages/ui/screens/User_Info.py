from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivymd.uix.button import MDIconButton, MDRaisedButton
from firebase_admin import db
from services.authentication import decrypt_value
from kivy.core.text import LabelBase
import os
from services.session_manager import clear_session

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray
ACCENT_COLOR = (1, 1, 1, 1)  # White
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

class UserInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(UserInfoScreen, self).__init__(**kwargs)
        self.user_id = None  # Will be set later
        self.user_data = {}

        layout = FloatLayout()

        # Background
        with layout.canvas.before:
            Color(*ACCENT_COLOR)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect)

        # Back Button
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=PRIMARY_COLOR,
            pos_hint={'x': 0.02, 'top': 0.98},
            size_hint=(None, None),
            size=(48, 48)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # User Icon Image
        self.user_icon = Image(
            source='Pages/assets/Images/icons.png',
            size_hint=(None, None),
            size=(180, 180),
            allow_stretch=True,
            keep_ratio=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )
        layout.add_widget(self.user_icon)

        # User Info Layout
        self.info_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=[40, 20, 40, 20],
            size_hint=(0.9, 0.35),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        layout.add_widget(self.info_layout)

        # Logout Button
        logout_btn = MDRaisedButton(
            text="LOGOUT",
            size_hint=(0.6, None),
            height=50,
            md_bg_color=PRIMARY_COLOR,
            pos_hint={'center_x': 0.5, 'y': 0.05},
            font_size='18sp',
            elevation=2
        )
        logout_btn.bind(on_press=self.logout)
        layout.add_widget(logout_btn)

        self.add_widget(layout)

    def set_user_id(self, user_id):
        """Set user ID dynamically and fetch data."""
        self.user_id = user_id
        self.fetch_user_data()

    def fetch_user_data(self):
        """Fetch user data from Firebase and update UI."""
        if not self.user_id:
            print("User ID not set.")
            return

        try:
            user_ref = db.reference(f'users/{self.user_id}')
            user_data = user_ref.get()

            if user_data:
                # Decrypt sensitive fields
                user_data["mobile"] = decrypt_value(user_data.get("mobile", "N/A"))
                user_data["account_number"] = decrypt_value(user_data.get("account_number", "N/A"))

                self.user_data = user_data
                self.update_user_info()
            else:
                print("User data not found.")
        except Exception as e:
            print(f"Error fetching user data: {e}")

    def update_user_info(self):
        """Update UI elements with user data."""
        self.info_layout.clear_widgets()

        fields = [
            ("UserName", self.user_data.get('name', 'N/A')),
            ("Mobile No", self.user_data.get('mobile', 'N/A')),
            ("Account No", self.user_data.get('account_number', 'N/A')),
            ("Address", self.user_data.get('address', 'N/A'))
        ]

        for label, value in fields:
            self.info_layout.add_widget(Label(
                text=f"[b]{label}:[/b] {value}",
                markup=True,
                font_size='18sp',
                font_name= font_path,  # Apply Poppins font
                color=TEXT_COLOR,
                halign='left',
                valign='middle',
                size_hint_y=None,
                height=40
            ))

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        """Navigate back to the dashboard screen."""
        self.manager.current = 'dashboard'

    def logout(self, instance):
        """Handle logout and terminate session."""

        login_screen = self.manager.get_screen("login")
        login_screen.enable_login_button()

        # Clear session data
        clear_session()
        print("Logged out successfully.")

        self.manager.current = "login"
