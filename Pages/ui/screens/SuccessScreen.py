from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.uix.image import Image
import datetime
import os
import uuid
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.text import LabelBase
import datetime
import firebase_admin
from firebase_admin import db

# Font
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets", "Fonts", "Poppins-Bold.ttf"))
if os.path.exists(FONT_PATH):
    LabelBase.register(name="Poppins", fn_regular=FONT_PATH)
else:
    raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

# Color Theme
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)
ACCENT_COLOR = (1, 1, 1, 1)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)
WHITE_COLOR = (1, 1, 1, 1)

class SuccessScreen(MDScreen):
    def __init__(self, balance=10000, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.98, 0.98, 0.98, 1)  # Light background
        self.balance = balance  # Initial balance
        self.transaction_id = self.generate_transaction_id()
        self.create_ui()

    def generate_transaction_id(self):
        """Generates a unique transaction ID."""
        return f"BankLink-{uuid.uuid4().hex[:12].upper()}"

    def create_ui(self):
        current_date = datetime.datetime.now().strftime("%d %b %Y")

        # Main container
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
        )

        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=PRIMARY_COLOR,
            pos_hint={'x': 0.02, 'top': 0.98},
            size_hint=(None, None),
            size=(48, 48)
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        # Success Header Card
        header_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(250),
            elevation=2,
            radius=[0, 0, dp(20), dp(20)],
            md_bg_color=(0.29, 0.0, 0.51, 1),
            padding=dp(20),
            spacing=dp(15),
        )

        # Success Icon
        icon_container = MDAnchorLayout(anchor_x="center", anchor_y="center")
        icon_container.add_widget(Image(
            source="assets/Images/checkmark.png",
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            allow_stretch=True
        ))

        # Success Text
        success_text = MDLabel(
            text="Transaction Successful",
            font_name="Poppins",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="24sp",
            halign="center",
            bold=True
        )

        # Date
        date_text = MDLabel(
            text=current_date,
            font_name="Poppins",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            font_size="14sp",
            halign="center"
        )

        header_card.add_widget(icon_container)
        header_card.add_widget(success_text)
        header_card.add_widget(date_text)

        # Transaction Details Card
        details_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(250),
            elevation=2,
            radius=dp(20),
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1),
        )

        # Transaction ID Section
        id_layout = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(40))
        id_label = MDLabel(
            text="Transaction ID:",
            font_name="Poppins",
            font_size="16sp",
            bold=True,
        )
        self.transaction_id_label = MDLabel(
            text=self.transaction_id,
            font_name="Poppins",
            font_size="14sp",
            halign="right",
            theme_text_color="Secondary",
        )
        copy_btn = MDIconButton(
            icon="content-copy",
            theme_text_color="Custom",
            text_color=(0.29, 0.0, 0.51, 1),
            on_release=self.copy_transaction_id
        )

        id_layout.add_widget(id_label)
        id_layout.add_widget(self.transaction_id_label)
        id_layout.add_widget(copy_btn)

        # Payment Details
        payment_grid = MDGridLayout(
            cols=2,
            spacing=dp(10),
            row_default_height=dp(40),
            size_hint=(1, None),
            height=dp(120),
        )

        # Paid To Section
        payment_grid.add_widget(MDLabel(
            text="Paid To:",
            font_name="Poppins",
            font_size="16sp",
            bold=True,
        ))
        self.paid_to_value = MDLabel(
            text="xxxxxxx5678\n@BankLink",
            font_name="Poppins",
            font_size="14sp",
            halign="right",
            theme_text_color="Secondary"
        )
        payment_grid.add_widget(self.paid_to_value)

        # Amount Section
        payment_grid.add_widget(MDLabel(
            text="Amount:",
            font_name="Poppins",
            font_size="16sp",
            bold=True,
        ))
        self.paid_to_amount = MDLabel(
            text="₹5000.00",
            font_name="Poppins",
            font_size="18sp",
            halign="right",
            bold=True
        )
        payment_grid.add_widget(self.paid_to_amount)

        # Debited From Section
        payment_grid.add_widget(MDLabel(
            text="Debited From:",
            font_name="Poppins",
            font_size="16sp",
            bold=True,
        ))
        self.debited_from_value = MDLabel(
            text="xxxxxxx9874\n@BankLink",
            font_name="Poppins",
            font_size="14sp",
            halign="right",
            theme_text_color="Secondary"
        )
        payment_grid.add_widget(self.debited_from_value)

        # Assemble Details Card
        details_card.add_widget(id_layout)
        details_card.add_widget(payment_grid)

        # Footer
        footer = MDLabel(
            text="Powered by BankLink",
            font_name="Poppins",
            font_size="12sp",
            halign="center",
            theme_text_color="Secondary"
        )

        main_layout.add_widget(header_card)
        main_layout.add_widget(details_card)
        main_layout.add_widget(footer)
        self.add_widget(main_layout)

    def display_transaction_details(self, transaction_details):
        """Displays transaction details and updates balance in Firebase."""
        recipient_id = transaction_details.get("recipient_id", "Unknown")
        sender_id = transaction_details.get("sender_id", "Unknown")
        amount = float(transaction_details.get("amount", 0.0))

        self.paid_to_value.text = f"xxxxxxx{recipient_id[-4:]}\n@BankLink"
        self.debited_from_value.text = f"xxxxxxx{sender_id[-4:]}\n@BankLink"
        self.paid_to_amount.text = f"₹ {amount:.2f}"

        self.update_user_balances(sender_id, recipient_id, amount)

    def update_user_balances(self, sender_id, recipient_id, amount):
        """Fetch and update sender and recipient balances in Firebase."""
        try:
            # References to user data
            sender_ref = db.reference(f"users/{sender_id}")
            recipient_ref = db.reference(f"users/{recipient_id}")
            sender_data, recipient_data = sender_ref.get(), recipient_ref.get()

            if not sender_data or not recipient_data:
                toast("❌ Error: User data not found")
                return

            # Fetch current balances
            sender_balance = float(sender_data.get("balance", 0.0))
            recipient_balance = float(recipient_data.get("balance", 0.0))

            # Check sufficient balance
            if sender_balance < amount:
                toast("❌ Insufficient Balance")
                return

            # Generate unique transaction ID
            transaction_id = f"BankLink-{uuid.uuid4().hex[:12].upper()}"
            transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Transaction Data
            transaction_data = {
                "transaction_id": transaction_id,
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "amount": amount,
                "date": transaction_time
            }

            # Perform atomic updates to Firebase
            updates = {
                f"users/{sender_id}/balance": sender_balance - amount,
                f"users/{recipient_id}/balance": recipient_balance + amount,
                f"users/{sender_id}/transactions/{transaction_id}": {**transaction_data, "type": "debited"},
                f"users/{recipient_id}/transactions/{transaction_id}": {**transaction_data, "type": "credited"},
                f"transactions/{transaction_id}": transaction_data  # Global transaction record
            }

            db.reference().update(updates)
            toast("✅ Transaction Updated Successfully")

        except Exception as e:
            toast(f"⚠️ Error updating balances: {str(e)}")

    def copy_transaction_id(self, instance):
        """Copies the transaction ID to clipboard."""
        Clipboard.copy(self.transaction_id_label.text)
        toast("📋 Transaction ID Copied")

    def go_back(self, instance):
        """Navigate back to the dashboard screen."""
        self.manager.current = 'dashboard'


class SuccessApp(MDApp):
    def build(self):
        screen = SuccessScreen(balance=20000)
        screen.display_transaction_details({
            "recipient_id": "12345678",
            "sender_id": "87654321",
            "amount": 5000
        })
        return screen


if __name__ == "__main__":
    SuccessApp().run()
