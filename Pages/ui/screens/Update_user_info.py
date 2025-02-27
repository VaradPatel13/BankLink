from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineIconListItem, MDList, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from cryptography.fernet import Fernet
import bcrypt
import os
import firebase_admin
from firebase_admin import credentials, db

# 🔹 Firebase Configuration
if not firebase_admin._apps:
    cred = credentials.Certificate("../../../services/crendential.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://banklink-2025-default-rtdb.firebaseio.com/'
    })

# Font
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets", "Fonts", "Poppins-Bold.ttf"))
if os.path.exists(FONT_PATH):
    LabelBase.register(name="Poppins", fn_regular=FONT_PATH)
else:
    raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)
ACCENT_COLOR = (1, 1, 1, 1)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)
WHITE_COLOR = (1, 1, 1, 1)


class UpdateUserInfoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.user_data = {}
        self.main_layout = MDBoxLayout(orientation="vertical")
        self.create_ui()
        self.add_widget(self.main_layout)
        self.fetch_user_data()

    def create_ui(self):
        """ Create UI for settings screen """
        self.main_layout.clear_widgets()

        # 🔹 Top App Bar
        self.top_bar = MDTopAppBar(
            title="Settings",
            elevation=4,
            md_bg_color=PRIMARY_COLOR,
            specific_text_color=ACCENT_COLOR,
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        self.main_layout.add_widget(self.top_bar)

        # 🔹 Scrollable List
        self.scroll_view = MDScrollView()
        self.settings_list = MDList()

        # 🔹 Settings Items
        settings_items = [
            ("lock-outline", "Change Password", self.update_password_ui),
            ("phone-outline", "Change Mobile", self.update_mobile_ui),
            ("account-outline", "Change Name", self.update_name_ui),
            ("home-outline", "Change Address", self.update_address_ui)
        ]

        for icon, text, callback in settings_items:
            item = OneLineIconListItem(text=text, on_release=callback)
            item.add_widget(IconLeftWidget(icon=icon))
            self.settings_list.add_widget(item)

        self.scroll_view.add_widget(self.settings_list)
        self.main_layout.add_widget(self.scroll_view)

    def fetch_user_data(self):
        """ Fetches user data from Firebase """
        ref = db.reference(f"/users/{self.user_id}")
        user_data = ref.get()
        if user_data:
            self.user_data = user_data
            # print("Fetched User Data:", self.user_data)
        else:
            print("User not found!")

    # 🔹 Update Password UI
    def update_password_ui(self, instance):
        self.clear_layout()

        self.old_password = MDTextField(hint_text="Enter Old Password", password=True)
        self.new_password = MDTextField(hint_text="Enter New Password", password=True)
        self.confirm_password = MDTextField(hint_text="Confirm New Password", password=True)

        change_btn = MDRaisedButton(text="Change Password", on_release=self.update_password)
        back_btn = MDRaisedButton(text="Back", on_release=self.reload_settings_screen)

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(self.old_password)
        layout.add_widget(self.new_password)
        layout.add_widget(self.confirm_password)
        layout.add_widget(change_btn)
        layout.add_widget(back_btn)

        self.main_layout.add_widget(layout)

    def update_password(self, instance):
        old_password = self.old_password.text
        new_password = self.new_password.text
        confirm_password = self.confirm_password.text

        ref = db.reference(f"/users/{self.user_id}/password")
        hashed_password = ref.get()

        if not bcrypt.checkpw(old_password.encode(), hashed_password.encode()):

            # print("Old password is incorrect!")
            return

        if new_password != confirm_password:
            # print("Passwords do not match!")
            return

        new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        ref.set(new_hashed_password)

        # print("Password Updated Successfully!")
        self.reload_settings_screen()

    # 🔹 Update Mobile UI
    def update_mobile_ui(self, instance):
        self.clear_layout()

        self.new_mobile = MDTextField(hint_text="Enter New Mobile Number")
        change_btn = MDRaisedButton(text="Change Mobile", md_bg_color=PRIMARY_COLOR ,on_release=self.update_mobile)
        back_btn = MDRaisedButton(text="Back",  md_bg_color=SECONDARY_COLOR ,on_release=self.reload_settings_screen)

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(self.new_mobile)
        layout.add_widget(change_btn)
        layout.add_widget(back_btn)

        self.main_layout.add_widget(layout)

    def update_mobile(self, instance):
        new_mobile = self.new_mobile.text
        key = b'fTvxVcDZNOYAmt1D33OUwkFBdibYi_F0tN6Y_lOQTAk='  # Replace with actual key
        cipher_suite = Fernet(key)
        encrypted_mobile = cipher_suite.encrypt(new_mobile.encode()).decode()

        ref = db.reference(f"/users/{self.user_id}/mobile")
        ref.set(encrypted_mobile)

        print("Mobile Updated Successfully!")
        self.reload_settings_screen()

    def update_name_ui(self, instance):
        self.clear_layout()

        self.new_name = MDTextField(hint_text="Enter New Name")
        change_btn = MDRaisedButton(text="Change Name", on_release=self.update_name)
        back_btn = MDRaisedButton(text="Back", on_release=self.reload_settings_screen)

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(self.new_name)
        layout.add_widget(change_btn)
        layout.add_widget(back_btn)

        self.main_layout.add_widget(layout)

    def update_name(self, instance):
        new_name = self.new_name.text
        ref = db.reference(f"/users/{self.user_id}/name")
        ref.set(new_name)

        print("Name Updated Successfully!")
        self.reload_settings_screen()

    def update_address_ui(self, instance):
        self.clear_layout()

        self.new_address = MDTextField(hint_text="Enter New Address")
        change_btn = MDRaisedButton(text="Change Address", on_release=self.update_address)
        back_btn = MDRaisedButton(text="Back", on_release=self.reload_settings_screen)

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(self.new_address)
        layout.add_widget(change_btn)
        layout.add_widget(back_btn)

        self.main_layout.add_widget(layout)

    def update_address(self, instance):
        new_address = self.new_address.text.strip()
        ref = db.reference(f"/users/{self.user_id}/address")
        ref.set(new_address)

        print("Address Updated Successfully!")
        self.reload_settings_screen()

    def clear_layout(self):
        """ Reset the main layout before switching screens. """
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.top_bar)  # Ensure top bar remains

    def reload_settings_screen(self, *args):
        """ Completely reload the settings screen to fix UI overlapping issues """
        self.create_ui()

    def go_back(self):
        self.manager.current = "dashboard"

    def set_user_id(self, user_id):
        """Receives and stores the user ID"""
        self.user_id = user_id
        print(f"✅ User ID set in {self.name}: {self.user_id}")


class UpdateAPP(MDApp):
    def build(self):
        return UpdateUserInfoScreen(user_id="sd")


if __name__ == "__main__":
    UpdateAPP().run()
