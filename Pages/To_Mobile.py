from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.toast import toast
from firebase_admin import db

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
ACCENT_COLOR = (1, 1, 1, 1)  # White
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray

class MobilePaymentScreen(MDScreen):
    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id  # Logged-in user ID
        self.md_bg_color = ACCENT_COLOR  # White background

        # Top Navigation Bar
        self.toolbar = MDTopAppBar(
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=0,
            md_bg_color=ACCENT_COLOR,
            specific_text_color=(0, 0, 0, 1)
        )
        self.add_widget(self.toolbar)

        # Form Layout
        form_layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint=(0.9, None),
            height="200dp",
            pos_hint={"center_x": 0.5}
        )

        self.mobile_input = MDTextField(
            hint_text="Enter Recipient Mobile Number",
            mode="rectangle",
            size_hint_x=1,
            font_size="18sp",
            text_color_normal=TEXT_COLOR,
            text_color_focus=TEXT_COLOR,
            line_color_focus=PRIMARY_COLOR
        )

        self.amount_input = MDTextField(
            hint_text="Enter Amount",
            mode="rectangle",
            size_hint_x=1,
            font_size="18sp",
            text_color_normal=PRIMARY_COLOR,
            text_color_focus=TEXT_COLOR,
            line_color_focus=PRIMARY_COLOR,
            input_filter="float"
        )

        self.pay_button = MDRaisedButton(
            text="Pay",
            md_bg_color=PRIMARY_COLOR,
            size_hint_x=1,
            font_size="18sp",
            theme_text_color="Custom",
            text_color=ACCENT_COLOR,
            on_press=self.process_payment
        )

        # Add widgets to layout
        form_layout.add_widget(self.mobile_input)
        form_layout.add_widget(self.amount_input)
        form_layout.add_widget(self.pay_button)

        # Centering everything inside an AnchorLayout
        anchor_layout = MDAnchorLayout(anchor_y="center")
        anchor_layout.add_widget(form_layout)

        self.add_widget(anchor_layout)

    def process_payment(self, instance):
        """Handles mobile number validation and money transfer."""
        recipient_mobile = self.mobile_input.text.strip()
        amount_text = self.amount_input.text.strip()

        if not recipient_mobile or not amount_text:
            toast("Please fill all fields")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                toast("Invalid amount")
                return
        except ValueError:
            toast("Enter a valid amount")
            return

        sender_ref = db.reference(f'users/{self.user_id}')
        sender_data = sender_ref.get()

        if not sender_data:
            toast("Sender account not found")
            return

        sender_balance = sender_data.get('balance', 0)
        if sender_balance < amount:
            toast("Insufficient balance")
            return

        recipient_ref = db.reference("users").order_by_child("mobile").equal_to(recipient_mobile).get()
        if not recipient_ref:
            toast("Recipient not found")
            return

        recipient_id = list(recipient_ref.keys())[0]
        recipient_data = recipient_ref[recipient_id]

        # Perform transaction
        sender_ref.update({"balance": sender_balance - amount})
        db.reference(f'users/{recipient_id}').update({"balance": recipient_data['balance'] + amount})

        toast("Payment successful!")

    def go_back(self):
        self.manager.current = "dashboard"
