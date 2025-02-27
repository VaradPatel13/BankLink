import datetime
import firebase_admin
from firebase_admin import db
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
import os
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from services.authentication import decrypt_value  # Import decryption function

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
TEXT_COLOR = (0, 0, 0, 1)  # Black



# Image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKMARK_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets", "Images", "checkmark.png"))
if os.path.exists(CHECKMARK_PATH):
    checkmark_image = Image(source=CHECKMARK_PATH)
else:
    raise FileNotFoundError(f"Image file not found: {CHECKMARK_PATH}")


class CheckBalanceScreen(Screen):
    def __init__(self, **kwargs):
        super(CheckBalanceScreen, self).__init__(**kwargs)
        self.user_id = None
        self.account_number = None
        self.balance_ref = None

        # Main Layout
        layout = BoxLayout(orientation='vertical', padding=[20, 40], spacing=15)

        # Back Button
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=TEXT_COLOR,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"x": 0, "top": 1}
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # Checkmark Container
        checkmark_container = RelativeLayout(size_hint=(None, None), size=(200, 200), pos_hint={"center_x": 0.5})
        with checkmark_container.canvas.before:
            Color(*PRIMARY_COLOR)
            self.circle = Ellipse(pos=checkmark_container.pos, size=checkmark_container.size)

        checkmark_image = Image(
            source=CHECKMARK_PATH,
            size_hint=(None, None),
            size=(120, 120),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        checkmark_container.add_widget(checkmark_image)
        layout.add_widget(checkmark_container)

        # Success Message
        success_label = Label(
            text="Bank Account balance fetched\nsuccessfully",
            font_size=20,
            color=TEXT_COLOR,
            bold=True,
            halign="center"
        )
        layout.add_widget(success_label)

        # Account Number Display
        self.account_label = Label(
            text="BankLink-****",
            font_size=16,
            color=TEXT_COLOR,
            halign="center"
        )
        layout.add_widget(self.account_label)

        # Balance Section
        balance_layout = BoxLayout(orientation="vertical", spacing=1, size_hint=(None, None), size=(200, 80), pos_hint={"center_x": 0.5})

        balance_label = Label(
            text="Available Balance",
            font_size=14,
            color=TEXT_COLOR,
            halign="center"
        )
        self.balance_amount_label = Label(
            text="₹0",
            font_size=42,
            color=TEXT_COLOR,
            bold=True,
            halign="center"
        )

        balance_layout.add_widget(balance_label)
        balance_layout.add_widget(self.balance_amount_label)
        layout.add_widget(balance_layout)

        self.add_widget(layout)

    def on_enter(self):
        """Fetch the latest balance from Firebase every time the screen is shown."""
        if self.account_number:
            self.get_balance()

    def get_balance(self):
        """Fetch balance from Firebase in real-time."""
        if not self.account_number:
            return

        # Define balance reference
        self.balance_ref = db.reference(f"users/{self.user_id}/balance")

        def balance_listener(event):
            """Update balance label in real-time."""
            new_balance = event.data
            if new_balance is not None:
                self.balance_amount_label.text = f"₹{int(new_balance):,}"
            else:
                self.balance_amount_label.text = "₹0"

        # Attach a listener for real-time updates
        self.balance_ref.listen(balance_listener)

    def go_back(self, instance):
        """Navigate back to dashboard."""
        self.manager.current = "dashboard"

    def set_user_id(self, user_id):
        """Receives and stores the user ID, then fetches & decrypts the account number from Firebase."""
        self.user_id = user_id
        user_ref = db.reference(f"users/{user_id}")
        user_data = user_ref.get()

        if user_data and "account_number" in user_data:
            encrypted_account_number = user_data["account_number"]
            try:
                # Decrypt account number
                self.account_number = decrypt_value(encrypted_account_number)
                last_4_digits = self.account_number[-4:]
                self.account_label.text = f"BankLink-{last_4_digits}"
                self.get_balance()
            except Exception as e:
                print(f" Decryption Error: {str(e)}")
                self.account_label.text = "BankLink-****"
                self.balance_amount_label.text = "₹0"
        else:
            self.account_label.text = "BankLink-****"
            self.balance_amount_label.text = "₹0"

        # print(f" User ID set: {self.user_id}, Account Number: {self.account_number}")

class chckapp(MDApp):
    def build(self):
        screen = CheckBalanceScreen()
        return screen


if __name__ == "__main__":
    chckapp().run()
