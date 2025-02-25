from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from firebase_admin import db
from kivymd.app import MDApp
from kivymd.font_definitions import LabelBase
from kivymd.uix.label import MDIcon
from kivy.clock import Clock
from services.authentication import decrypt_value
import os


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

class AccountPaymentScreen(MDScreen):
    dialog = None
    user_id = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui()

    def create_ui(self):
        # Modern Top App Bar
        self.toolbar = MDTopAppBar(
            title="Account Payment",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=2,
            md_bg_color=PRIMARY_COLOR,
            specific_text_color=ACCENT_COLOR,
            size_hint_y=None,
            height=dp(56),
        )

        # Payment Card (Centered)
        payment_card = MDCard(
            orientation="vertical",
            size_hint=(0.8, None),
            size=(dp(320), dp(340)),  # Fixed size for responsiveness
            elevation=2,
            radius=dp(20),
            padding=dp(25),
            spacing=dp(15),
            md_bg_color="#FAF7F0",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # Header
        payment_header = MDLabel(
            text="Transfer Funds",
            font_name="Poppins",
            font_size="22sp",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=PRIMARY_COLOR,
        )

        # Account Number Input
        account_container = MDBoxLayout(orientation="vertical", spacing=dp(5))
        account_container.add_widget(
            MDLabel(
                text="Recipient Account Number",
                font_name="Poppins",
                font_size="14sp",
                theme_text_color="Secondary",
            )
        )
        self.account_input = MDTextField(
            mode="fill",
            fill_color_normal=(0.95, 0.95, 0.95, 1),
            radius=[dp(10), dp(10), dp(10), dp(10)],
            line_color_normal=PRIMARY_COLOR,
            line_color_focus=PRIMARY_COLOR,
            font_size="16sp",
            hint_text="Enter account number",
            text_color_focus=TEXT_COLOR,
            icon_left="credit-card-outline",
        )
        account_container.add_widget(self.account_input)

        # Amount Input
        amount_container = MDBoxLayout(orientation="vertical", spacing=dp(5))
        amount_container.add_widget(
            MDLabel(
                text="Transfer Amount",
                font_name="Poppins",
                font_size="14sp",
                theme_text_color="Secondary",
            )
        )
        self.amount_input = MDTextField(
            mode="fill",
            fill_color_normal=(0.95, 0.95, 0.95, 1),
            radius=[dp(10), dp(10), dp(10), dp(10)],
            line_color_normal=PRIMARY_COLOR,
            line_color_focus=PRIMARY_COLOR,
            font_size="16sp",
            hint_text="₹0.00",
            input_filter="float",
            text_color_focus=TEXT_COLOR,
            icon_left="currency-inr",
        )
        amount_container.add_widget(self.amount_input)

        # Pay Button with Animation
        self.pay_button = MDFillRoundFlatIconButton(
            text="Initiate Transfer",
            icon="bank-transfer",
            md_bg_color=PRIMARY_COLOR,
            theme_text_color="Custom",
            text_color=ACCENT_COLOR,
            font_size="16sp",
            padding=dp(15),
            on_press=self.animate_button,
            on_release=self.process_payment,
        )

        # Assemble Card
        payment_card.add_widget(payment_header)
        payment_card.add_widget(account_container)
        payment_card.add_widget(amount_container)
        payment_card.add_widget(self.pay_button)

        # Wrapper layout to center the card
        card_wrapper = MDBoxLayout(
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        card_wrapper.add_widget(payment_card)

        # Main layout with top bar and centered card
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
        )
        main_layout.add_widget(self.toolbar)  # Toolbar at the top
        main_layout.add_widget(card_wrapper)  # Card below the toolbar

        self.add_widget(main_layout)  # Add the entire layout to the screen

    def animate_button(self, instance):
        anim = Animation(
            md_bg_color=SECONDARY_COLOR,
            font_size=instance.font_size * 1.1,
            t="out_quad",
            d=0.1
        ) + Animation(
            md_bg_color=PRIMARY_COLOR,
            font_size=instance.font_size,
            t="out_quad",
            d=0.1
        )
        anim.start(instance)



    def process_payment(self, instance):
        instance.disabled = True
        Clock.schedule_once(lambda dt: setattr(instance, "disabled", False), 2)

        account_number = self.account_input.text.replace(" ", "").strip()
        amount = self.amount_input.text.strip()

        if not account_number or not amount:
            self.show_error("Please fill all fields")
            return

        if len(account_number) != 10:  # Ensure proper length
            self.show_error("Invalid account number (10 digits required)")
            return

        try:
            users_ref = db.reference("users").get()
            recipient_data = None

            # Search through stored encrypted account numbers
            for user_id, user_info in users_ref.items():
                encrypted_account = user_info.get("account_number")  # Encrypted value
                decrypted_account = decrypt_value(encrypted_account)  # Decrypt account number

                if decrypted_account == account_number:
                    recipient_data = user_info
                    recipient_data["user_id"] = user_id
                    break

            if recipient_data:
                self.confirm_transaction(recipient_data, amount)
            else:
                self.show_error("Account not found")

        except Exception as e:
            self.show_error(f"Payment Error: {str(e)}")

    def go_back(self):
        self.manager.current = "dashboard"

    def set_user_id(self, user_id):
        self.user_id = user_id

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

    def close_dialog(self, dialog):
        """Closes an open dialog."""
        dialog.dismiss()

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
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ],
            )
        else:
            self.dialog.text = message  # Update message

        self.dialog.open()


class AccountApp(MDApp):
    def build(self):
        screen = AccountPaymentScreen()
        screen.set_user_id("user_id")
        return screen


if __name__ == "__main__":
    AccountApp().run()
