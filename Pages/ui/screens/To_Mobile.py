from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
from firebase_admin import db
from services.authentication import decrypt_value
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.core.text import LabelBase
import os


# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
ACCENT_COLOR = (1, 1, 1, 1)  # White
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray

# Font
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets", "Fonts", "Poppins-Bold.ttf"))
if os.path.exists(FONT_PATH):
    LabelBase.register(name="Poppins", fn_regular=FONT_PATH)
else:
    raise FileNotFoundError(f"Font file not found: {FONT_PATH}")


class MobilePaymentScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.user_data = None
        self.transaction_details = None
        self.md_bg_color = (0.98, 0.98, 0.98, 1)  # Light background

        # Modern Top App Bar with back button
        self.toolbar = MDTopAppBar(
            title="Mobile Payment",
            left_action_items=[["arrow-left", lambda x: self.go_back(instance=x)]],
            elevation=2,
            md_bg_color=PRIMARY_COLOR,
            specific_text_color=ACCENT_COLOR,
            pos_hint={"top": 1},
            radius=[0, 0, dp(10), dp(10)]
        )

        # Main container card
        container = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height=dp(400),
            elevation=2,
            radius=dp(15),
            padding=dp(25),
            spacing=dp(20),
            md_bg_color=ACCENT_COLOR
        )

        # Payment header
        payment_header = MDLabel(
            text="Send Money",
            font_style="H4",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=PRIMARY_COLOR
        )

        # Recipient Input Field
        recipient_container = MDBoxLayout(orientation="vertical", spacing=dp(5))
        recipient_container.add_widget(MDLabel(
            text="Recipient Mobile Number",
            font_style="Body2",
            theme_text_color="Secondary"
        ))
        self.recipient_input = MDTextField(
            mode="fill",
            fill_color_normal=(0.95, 0.95, 0.95, 1),
            radius=[dp(10)],
            line_color_normal=PRIMARY_COLOR,
            line_color_focus=PRIMARY_COLOR,
            font_size="18sp",
            hint_text="+91 00000 00000",
            icon_left="cellphone",
            text_color_focus=TEXT_COLOR
        )
        recipient_container.add_widget(self.recipient_input)

        # Amount Input Field
        amount_container = MDBoxLayout(orientation="vertical", spacing=dp(5))
        amount_container.add_widget(MDLabel(
            text="Amount",
            font_style="Body2",
            theme_text_color="Secondary"
        ))
        self.amount_input = MDTextField(
            mode="fill",
            fill_color_normal=(0.95, 0.95, 0.95, 1),
            radius=[dp(10)],
            line_color_normal=PRIMARY_COLOR,
            line_color_focus=PRIMARY_COLOR,
            font_size="18sp",
            hint_text="₹0.00",
            icon_left="currency-inr",
            input_filter="float",
            text_color_focus=TEXT_COLOR
        )
        amount_container.add_widget(self.amount_input)

        # Modern Pay Button
        self.pay_button = MDFillRoundFlatButton(
            text="Send Payment",
            icon="send",
            md_bg_color=PRIMARY_COLOR,
            theme_text_color="Custom",
            text_color=ACCENT_COLOR,
            font_size="16sp",
            padding=dp(15),
            pos_hint={"center_x": 0.5},
            on_press = self.process_payment
        )

        # Assemble container
        container.add_widget(payment_header)
        container.add_widget(recipient_container)
        container.add_widget(amount_container)
        container.add_widget(self.pay_button)

        # Use MDAnchorLayout to center the card
        card_container = MDAnchorLayout(anchor_x="center", anchor_y="center")
        card_container.add_widget(container)

        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10)
        )
        main_layout.add_widget(self.toolbar)  # Toolbar at the top
        main_layout.add_widget(card_container)  # Centered card

        self.add_widget(main_layout)


    def on_enter(self, *args):
        """Fetch sender user details when the screen is entered."""
        print("uesr_id: ", self.user_id)
        print("🔄 Fetching logged-in user details...")
        self.fetch_logged_in_user()

    def fetch_logged_in_user(self):
        """Fetch sender user details directly from Firebase using user_id path."""
        if not self.user_id:
            print("❌ User ID is missing! Cannot fetch user data.")
            return

        try:
            # Fetch user details using the user ID path
            user_ref = db.reference(f"users/{self.user_id}").get()

            if user_ref:
                self.user_data = user_ref  # Store user data
                print(f"✅ Sender User Data: {self.user_data}")
            else:
                print(f"⚠️ User ID '{self.user_id}' not found in database!")

        except Exception as e:
            print(f"⚠️ Error fetching user data: {str(e)}")

    def process_payment(self, instance):
        recipient_mobile = self.recipient_input.text.strip()
        amount = self.amount_input.text.strip()

        if not recipient_mobile or not amount:
            self.show_error("Please enter all required details.")
            return

        try:
            users_ref = db.reference("users").get()
            if not users_ref:
                self.show_error("No users found in the database.")
                return

            recipient_data = None
            for user_id, user_info in users_ref.items():
                encrypted_mobile = user_info.get("mobile", "")
                decrypted_mobile = decrypt_value(encrypted_mobile)
                if decrypted_mobile == recipient_mobile:
                    recipient_data = user_info
                    recipient_data["user_id"] = user_id  # Store user ID
                    break

            if recipient_data:
                self.confirm_transaction(recipient_data, amount)
            else:
                self.show_error("Recipient not found.")

        except Exception as e:
            self.show_error(f"Error processing payment: {str(e)}")

    def confirm_transaction(self, recipient_data, amount):
        """Show confirmation dialog before proceeding with payment."""
        dialog = MDDialog(
            title="Confirm Payment",
            text=f"Send ₹{amount} to {recipient_data.get('name', 'Unknown')}?",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.close_dialog(dialog)),
                MDFlatButton(text="Proceed",
                             on_release=lambda x: self.store_transaction(recipient_data, amount, dialog)),
            ],
        )
        dialog.open()

    def store_transaction(self, recipient_data, amount, dialog):
        """Stores transaction details and opens PIN verification screen."""
        if not self.user_id:
            self.show_error("User ID not found. Please log in again.")
            return

        transaction_details = {
            "sender_id": self.user_id,
            "recipient_id": recipient_data["user_id"],
            "amount": float(amount)
        }

        print(f"✅ Transaction details stored: {transaction_details}")
        print("🔄 Navigating to PIN verification screen...")

        # Pass transaction details to PinEntryScreen
        pin_screen = self.manager.get_screen("pin_entry_screen")
        pin_screen.set_transaction_details(transaction_details, self.user_id)

        self.manager.current = "pin_entry_screen"
        self.close_dialog(dialog)

    def show_error(self, message):
        """Displays an error message."""
        dialog = MDDialog(title="Error", text=message,
                          buttons=[MDFlatButton(text="OK", on_release=lambda x: self.close_dialog(dialog))])
        dialog.open()

    def close_dialog(self, dialog):
        """Closes an open dialog."""
        dialog.dismiss()


    def go_back(self, instance):
        """Navigate back to the dashboard screen."""
        self.manager.current = 'dashboard'


    def set_user_id(self, user_id):
        """Receives and stores the user ID"""
        self.user_id = user_id
        print(f"✅ User ID set in {self.name}: {self.user_id}")


class MobileApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"  # Change to a valid Material palette
        self.theme_cls.theme_style = "Light"  # Use "Light" instead of "Dark" if needed
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.accent_hue = "500"
        return MobilePaymentScreen()


if __name__ == "__main__":
    MobileApp().run()
