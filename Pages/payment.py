from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import hashlib

class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.layout.add_widget(Label(text="Enter Secure Password", font_size=20))

        self.password_input = TextInput(password=True, multiline=False, font_size=18)
        self.layout.add_widget(self.password_input)

        submit_btn = Button(text="Submit", size_hint=(1, 0.2))
        submit_btn.bind(on_press=self.verify_password)
        self.layout.add_widget(submit_btn)

        self.add_widget(self.layout)

    def verify_password(self, instance):
        user_input = self.password_input.text
        hashed_password = self.hash_password("1234")  # Replace with actual stored hashed password

        if self.hash_password(user_input) == hashed_password:
            self.show_popup("Access Granted", "Payment Functionality Unlocked.")
        else:
            self.show_popup("Access Denied", "Incorrect Password.")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()
