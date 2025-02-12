from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Ellipse
from kivymd.uix.button import MDIconButton
import sqlite3

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
TEXT_COLOR = (0, 0, 0, 1)  # Black

class CheckBalanceScreen(Screen):
    def __init__(self, user_data, **kwargs):
        super(CheckBalanceScreen, self).__init__(**kwargs)
        self.user_data = user_data
        self.account_number = self.user_data["account_number"]
        self.balance = self.get_balance()  # Fetch balance from database

        # Main Layout
        layout = BoxLayout(orientation='vertical', padding=[20, 40], spacing=15)

        # Back Button (Top-Left)
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

        # Checkmark Container with Purple Circle
        checkmark_container = RelativeLayout(size_hint=(None, None), size=(200, 200), pos_hint={"center_x": 0.5})

        with checkmark_container.canvas.before:
            Color(*PRIMARY_COLOR)
            self.circle = Ellipse(pos=checkmark_container.pos, size=checkmark_container.size)

        checkmark_image = Image(
            source="Pages/assets/checkmark.png",
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
            halign="center",
            height=50
        )
        layout.add_widget(success_label)

        # Account Number Display
        last_4_digits = self.account_number[-4:]  # Extract last 4 digits
        account_label = Label(
            text=f"BankLink-{last_4_digits}",
            font_size=16,
            color=TEXT_COLOR,
            halign="center",
            height= 30
        )
        layout.add_widget(account_label)

        # Balance Section
        balance_layout = BoxLayout(orientation="vertical", spacing=1, size_hint=(None, None), size=(200, 80), pos_hint={"center_x": 0.5 , 'top':0.5})

        balance_label = Label(
            text="Available Balance",
            font_size=14,
            color=TEXT_COLOR,
            halign="center",
            height=20
        )
        balance_amount = Label(
            text=f"₹{int(self.balance):,}",  # Format to match bold INR style
            font_size=42,
            color=TEXT_COLOR,
            bold=True,
            halign="center",
            height = 20
        )

        balance_layout.add_widget(balance_label)
        balance_layout.add_widget(balance_amount)
        layout.add_widget(balance_layout)

        self.add_widget(layout)

    def get_balance(self):
        """Fetch balance from the database using account number."""
        conn = sqlite3.connect("banklinkdemo.db")
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE account_number=?", (self.account_number,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0.0  # Default to 0 if no balance found

    def go_back(self, instance):
        self.manager.current = "dashboard"
