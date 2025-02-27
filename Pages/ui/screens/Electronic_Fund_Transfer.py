from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import random
import firebase_admin
from firebase_admin import db, credentials
from services.authentication import decrypt_value

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("../../../services/crendential.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://banklink-2025-default-rtdb.firebaseio.com/'})

TRANSFER_MODES = ["NEFT", "RTGS", "IMPS"]

class FundTransferScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_mode = "NEFT"
        self.create_ui()
        self.user_id = None
        self.user_data = None
        self.transaction_details = None

    def create_ui(self):
        self.toolbar = MDTopAppBar(
            title="Fund Transfer",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=2,
            md_bg_color=(0.29, 0.0, 0.51, 1),
            specific_text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(56),
            pos_hint={"top": 1}
        )

        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(10),
            size_hint_y=1
        )

        transfer_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(400),
            elevation=2,
            radius=dp(20),
            padding=dp(25),
            spacing=dp(15),
            md_bg_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
        )

        self.account_input = MDTextField(hint_text="Recipient Account Number", mode="fill")
        self.ifsc_input = MDTextField(hint_text="IFSC Code", mode="fill")
        self.amount_input = MDTextField(hint_text="Amount (₹)", mode="fill", input_filter="float")
        self.note_input = MDTextField(hint_text="Remarks (Optional)", mode="fill")

        mode_selection = MDBoxLayout(orientation="horizontal", spacing=dp(15))
        for mode in TRANSFER_MODES:
            checkbox = MDCheckbox(group="transfer_mode", active=(mode == "NEFT"),
                                  on_release=lambda chk, m=mode: self.set_transfer_mode(chk, m))
            mode_selection.add_widget(checkbox)
            mode_selection.add_widget(MDLabel(text=mode))

        self.pay_button = MDFillRoundFlatButton(
            text="Proceed to Pay",
            md_bg_color=(0.29, 0.0, 0.51, 1),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="16sp",
            on_press=self.animate_button,
            on_release=self.process_payment,
        )

        transfer_card.add_widget(self.account_input)
        transfer_card.add_widget(self.ifsc_input)
        transfer_card.add_widget(self.amount_input)
        transfer_card.add_widget(self.note_input)
        transfer_card.add_widget(mode_selection)
        transfer_card.add_widget(self.pay_button)

        # Add the toolbar first to ensure it's at the top
        self.add_widget(self.toolbar)
        main_layout.add_widget(transfer_card)

        self.add_widget(main_layout)

    def set_transfer_mode(self, checkbox, mode):
        if checkbox.active:
            self.selected_mode = mode

    def animate_button(self, instance):
        anim = Animation(md_bg_color=(0.58, 0.44, 0.86, 1), d=0.1) + Animation(md_bg_color=(0.29, 0.0, 0.51, 1), d=0.1)
        anim.start(instance)

    def set_user_id(self, user_id):
        self.user_id = user_id
        print(f"✅ User ID set: {self.user_id}")

    def process_payment(self, instance):
        recipient_account = self.account_input.text.strip()
        amount = self.amount_input.text.strip()

        if not recipient_account or not amount:
            self.show_error("Please enter all required details.")
            return

        users_ref = db.reference("users").get()
        recipient_data = None
        for user_id, user_info in users_ref.items():
            decrypted_mobile = decrypt_value(user_info.get("account_number", ""))
            if decrypted_mobile == recipient_account:
                recipient_data = user_info
                recipient_data["user_id"] = user_id
                break

        if recipient_data:
            self.send_otp(recipient_data, amount)
        else:
            self.show_error("Recipient not found.")

    def send_otp(self, recipient_data, amount):
        self.otp = random.randint(100000, 999999)
        print(f"OTP sent: {self.otp}")
        self.show_otp_dialog(recipient_data, amount)

    def show_otp_dialog(self, recipient_data, amount):
        self.otp_input = MDTextField(hint_text="Enter OTP", mode="fill")
        dialog = MDDialog(
            title="OTP Verification",
            text="An OTP has been sent. Enter it to proceed.",
            type="custom",
            content_cls=self.otp_input,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDFlatButton(text="Verify", on_release=lambda x: self.verify_otp(recipient_data, amount, dialog)),
            ],
        )
        dialog.open()

    def close_dialog(self, dialog):
        """Closes an open dialog."""
        dialog.dismiss()

    def verify_otp(self, recipient_data, amount, dialog):
        entered_otp = self.otp_input.text.strip()
        if entered_otp == str(self.otp):
            print(f"✅ User ID set: {self.user_id}")
            self.store_transaction(recipient_data, amount, dialog)
            dialog.dismiss()
        else:
            self.show_error("Invalid OTP. Try again.")

    def store_transaction(self, recipient_data, amount, dialog):
        """Stores transaction details and updates balances in Firebase."""
        if not self.user_id:
            self.show_error("User ID not found. Please log in again.")
            return

        try:
            sender_ref = db.reference(f"users/{self.user_id}")
            recipient_ref = db.reference(f"users/{recipient_data['user_id']}")
            transaction_ref = db.reference("transactions").push()

            # Fetch sender balance
            sender_balance = sender_ref.child("balance").get() or 0.0
            if float(sender_balance) < float(amount):
                self.show_error("Insufficient balance!")
                return

            # Deduct from sender
            new_sender_balance = float(sender_balance) - float(amount)
            sender_ref.update({"balance": new_sender_balance})

            # Add to recipient
            recipient_balance = recipient_ref.child("balance").get() or 0.0
            new_recipient_balance = float(recipient_balance) + float(amount)
            recipient_ref.update({"balance": new_recipient_balance})

            # Store transaction details
            transaction_details = {
                "sender_id": self.user_id,
                "recipient_id": recipient_data["user_id"],
                "amount": float(amount),
                "status": "Completed",
            }
            transaction_ref.set(transaction_details)

            # print(f" Transaction successful: {transaction_details}")
            self.show_success("Transaction successful!")

            self.close_dialog(dialog)
            self.manager.current = "dashboard"

        except Exception as e:
            self.show_error(f"Error storing transaction: {str(e)}")

    def show_success(self, message):
        MDDialog(title="Success", text=message, buttons=[MDFlatButton(text="OK")]).open()

    def show_error(self, message):
        MDDialog(title="Error", text=message, buttons=[MDFlatButton(text="OK")]).open()

    def go_back(self):
        self.manager.current = "dashboard"

    def set_user_id(self, user_id):
        """Receives and stores the user ID"""
        self.user_id = user_id
        # print(f"User ID set in {self.name}: {self.user_id}")


class ElectronicFundTransferScreen(MDApp):
    def build(self):
        self.screen = FundTransferScreen()
        return self.screen

if __name__ == "__main__":
    ElectronicFundTransferScreen().run()

