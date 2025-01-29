from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from database import add_user

# Theme colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)
ACCENT_COLOR = (1, 1, 1, 1)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)

class CreateAccountScreen(Screen):
    def __init__(self, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.create_layout()

    def create_layout(self):
        layout = FloatLayout()

        # Background Image
        background = Image(source='assets/background.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Input fields container
        input_layout = BoxLayout(orientation='vertical', spacing=15, padding=30,
                                 size_hint=(0.9, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Full Name Input
        self.name_input = TextInput(
            hint_text="Full Name",
            size_hint=(1, None),
            height=50,
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.name_input)

        # Address Input
        self.address_input = TextInput(
            hint_text="Address",
            size_hint=(1, None),
            height=50,
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.address_input)

        # Mobile Number Input
        self.mobile_input = TextInput(
            hint_text="Mobile Number",
            size_hint=(1, None),
            height=50,
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.mobile_input)

        # Password Input
        self.password_input = TextInput(
            hint_text="Password",
            size_hint=(1, None),
            height=50,
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16,
            password=True
        )
        input_layout.add_widget(self.password_input)

        # Initial Amount Input
        self.amount_input = TextInput(
            hint_text="Initial Amount",
            size_hint=(1, None),
            height=50,
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.amount_input)

        # Create Account Button
        create_button = Button(
            text="Create Account",
            size_hint=(1, None),
            height=50,
            background_color=PRIMARY_COLOR,
            color=ACCENT_COLOR,
            font_size=18,
            bold=True
        )
        create_button.bind(on_press=self.create_account)
        input_layout.add_widget(create_button)

        layout.add_widget(input_layout)
        self.add_widget(layout)

    def create_account(self, instance):
        name = self.name_input.text
        address = self.address_input.text
        mobile = self.mobile_input.text
        password = self.password_input.text
        initial_amount = float(self.amount_input.text)

        if name and address and mobile and password and initial_amount:
            account_number = add_user(name, address, mobile, password, initial_amount)
            print(f"Account created successfully! Account Number: {account_number}")
            self.manager.current = 'login'
        else:
            self.show_error_popup("Error", "Please fill in all fields.")

    def show_error_popup(self, title, message):
        popup = Popup(
            title=title,
            size_hint=(0.8, 0.4),
            content=Label(text=message, font_size=16, color=TEXT_COLOR),
            separator_height=0,
            background_color=SECONDARY_COLOR
        )
        popup.open()