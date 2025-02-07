import sqlite3
import random
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle  # Add this import for Color

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple (#4B0082)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)  # Light Purple (#9370DB)
ACCENT_COLOR = (1, 1, 1, 1)  # White (#FFFFFF)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray (#333333)


class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super(ForgotPasswordScreen, self).__init__(**kwargs)

        # Set up background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout using AnchorLayout to center content
        main_layout = AnchorLayout(anchor_x='center', anchor_y='center')

        # Content container
        content = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(300, 250),  # Width, Height
            spacing=15,
            padding=20
        )

        # Title Label
        title = Label(
            text="Reset Password",
            font_size=24,
            color=PRIMARY_COLOR,  # Dark Purple
            bold=True,
            size_hint=(1, None),
            height=40
        )

        # Input Fields Container
        input_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, None),
            height=90
        )

        # TextInput styling
        input_style = {
            'size_hint': (1, None),
            'height': 40,
            'font_size': 14,
            'padding': 8,
            'background_color': (0.95, 0.95, 0.95, 1),
            'hint_text_color': (0.6, 0.6, 0.6, 1),
            'foreground_color': TEXT_COLOR,
            'multiline': False,
            'background_normal': '',
            'background_active': '',
            'cursor_color': PRIMARY_COLOR
        }

        self.account_input = TextInput(
            hint_text="Account Number",
            **input_style
        )

        self.mobile_input = TextInput(
            hint_text="Registered Mobile Number",
            **input_style
        )

        # Submit Button
        submit_button = Button(
            text="Verify",
            size_hint=(1, None),
            height=45,
            background_color=PRIMARY_COLOR,  # Dark Purple
            color=ACCENT_COLOR,
            bold=True,
            font_size=16,
            background_normal=''
        )
        submit_button.bind(on_press=self.verify_user)

        # Assemble UI components
        input_layout.add_widget(self.account_input)
        input_layout.add_widget(self.mobile_input)

        content.add_widget(title)
        content.add_widget(input_layout)
        content.add_widget(submit_button)

        main_layout.add_widget(content)
        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size



    def verify_user(self, instance):
        """Verify the user before resetting password."""
        account = self.account_input.text.strip()
        mobile = self.mobile_input.text.strip()

        if not account or not mobile:
            self.show_popup("Error", "Please fill in all fields.", (1, 0, 0, 1))
            return

        conn = sqlite3.connect("banklink.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE account_number = ? AND mobile = ?", (account, mobile))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.show_otp_popup()
        else:
            self.show_popup("Error", "Account not found. Check details.", (1, 0, 0, 1))

    def show_otp_popup(self):
        """OTP verification popup"""
        self.otp_code = str(random.randint(1000, 9999))

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.background_color = PRIMARY_COLOR

        otp_label = Label(
            text=f"Enter OTP [Simulated: {self.otp_code}]",
            color=ACCENT_COLOR,
            font_size=14
        )

        self.otp_input = TextInput(
            hint_text="Enter OTP",
            hint_text_color=SECONDARY_COLOR,
            foreground_color=TEXT_COLOR,
            background_color=SECONDARY_COLOR
        )

        self.new_password_input = TextInput(
            hint_text="New Password",
            hint_text_color=SECONDARY_COLOR,
            foreground_color=TEXT_COLOR,
            background_color=SECONDARY_COLOR,
            password=True
        )

        submit_button = Button(
            text="Reset Password",
            background_color=SECONDARY_COLOR,
            color=ACCENT_COLOR,
            size_hint_y=None,
            height=40
        )
        submit_button.bind(on_press=self.reset_password)

        layout.add_widget(otp_label)
        layout.add_widget(self.otp_input)
        layout.add_widget(self.new_password_input)
        layout.add_widget(submit_button)

        self.popup = Popup(
            title="OTP Verification",
            title_color=ACCENT_COLOR,
            title_align='center',
            content=layout,
            size_hint=(0.8, 0.5),
            background_color=PRIMARY_COLOR,
            separator_color=SECONDARY_COLOR
        )
        self.popup.open()

    def reset_password(self, instance):
        """Verify OTP and reset password"""
        if self.otp_input.text == self.otp_code:
            account = self.account_input.text.strip()
            new_password = self.new_password_input.text.strip()

            conn = sqlite3.connect("banklink.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE account_number = ?", (new_password, account))
            conn.commit()
            conn.close()

            self.popup.dismiss()
            self.show_popup("Success", "Password reset successfully! "
                                       "You can now log in.", (0, 0.7, 0, 1))
            self.manager.current = 'login'
        else:
            self.show_popup("Error", "Incorrect OTP. Try again.", (1, 0, 0, 1))

    def show_popup(self, title, message, color):
        """Styled popup message"""
        popup_content = Label(
            text=message,
            color=ACCENT_COLOR,
            halign='center'
        )

        popup = Popup(
            title=title,
            title_color=ACCENT_COLOR,
            content=popup_content,
            size_hint=(1, 0.5),
            background_color=PRIMARY_COLOR,
            separator_color=SECONDARY_COLOR,
            title_align='center'
        )

        # Set title background color
        if title == "Error":
            popup.title_color = (1, 0, 0, 1)
        elif title == "Success":
            popup.title_color = (0, 1, 0, 1)

        popup.open()