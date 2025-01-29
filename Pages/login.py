from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

# Set the app window size (optional, for testing)
Window.size = (360, 640)

# Define theme colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple (#4B0082)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)  # Light Purple (#9370DB)
ACCENT_COLOR = (1, 1, 1, 1)  # White (#FFFFFF)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray (#333333)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Main layout
        layout = FloatLayout()

        # Background Image
        background = Image(source='background.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Overlay for better readability
        overlay = Image(source='assets/bank.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(overlay)

        # Input fields container
        input_layout = BoxLayout(orientation='vertical', spacing=15, padding=30, size_hint=(0.9, 0.6),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Logo above the Account Number input
        logo = Image(source='Pages/assets/Bank.png', size=(200, 200), pos_hint={'center_x': 0.5})
        input_layout.add_widget(logo)

        logo = Image(
            source='Pages/assets/Bank.png',
            size_hint=(None, None),  # Disable size_hint
            size=(400, 400),  # Set absolute size
            allow_stretch=True,  # Allow stretching
            keep_ratio=False,  # Disable aspect ratio
            pos_hint={'center_x': 0.5}
        )
        input_layout.add_widget(logo)
        # Account Number Input
        self.account_input = TextInput(
            hint_text="Account Number",
            multiline=False,
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_active='',
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.account_input)

        # Password Input
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_active='',
            background_color=ACCENT_COLOR,
            foreground_color=TEXT_COLOR,
            padding=10,
            font_size=16
        )
        input_layout.add_widget(self.password_input)

        # Login Button
        login_button = Button(
            text="Login",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=PRIMARY_COLOR,
            color=ACCENT_COLOR,
            font_size=18,
            bold=True
        )
        login_button.bind(on_press=self.login)
        input_layout.add_widget(login_button)

        # Forgot Password and Create Account Links
        links_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=30,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.1})

        forgot_password = Button(
            text="Forgot Password?",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=SECONDARY_COLOR,
            font_size=14
        )
        forgot_password.bind(on_press=self.show_forgot_password_popup)

        create_account = Button(
            text="Create New Account",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=SECONDARY_COLOR,
            font_size=14
        )
        create_account.bind(on_press=self.show_create_account_popup)

        links_layout.add_widget(forgot_password)
        links_layout.add_widget(create_account)

        layout.add_widget(input_layout)
        layout.add_widget(links_layout)

        self.add_widget(layout)

    def login(self, instance):
        # Validate inputs
        account_number = self.account_input.text
        password = self.password_input.text

        if not account_number or not password:
            self.show_error_popup("Error", "Please fill in all fields.")
        else:
            print("Login successful!")
            # Add your login logic here (e.g., Firebase authentication)

    def show_error_popup(self, title, message):
        popup = Popup(
            title=title,
            size_hint=(0.8, 0.4),
            content=Label(text=message, font_size=16, color=TEXT_COLOR),
            separator_height=0,
            background_color=SECONDARY_COLOR
        )
        popup.open()

    def show_forgot_password_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        email_input = TextInput(hint_text="Enter your email", multiline=False, size_hint=(1, None), height=40,
                                background_color=ACCENT_COLOR, foreground_color=TEXT_COLOR)
        submit_button = Button(text="Submit", size_hint=(1, None), height=40, background_color=PRIMARY_COLOR,
                               color=ACCENT_COLOR)
        content.add_widget(email_input)
        content.add_widget(submit_button)

        popup = Popup(
            title="Forgot Password",
            size_hint=(0.8, 0.4),
            content=content,
            separator_height=0,
            background_color=SECONDARY_COLOR
        )
        submit_button.bind(on_press=lambda x: self.reset_password(email_input.text, popup))
        popup.open()

    def reset_password(self, email, popup):
        if email:
            print(f"Password reset link sent to {email}")
            popup.dismiss()
        else:
            self.show_error_popup("Error", "Please enter a valid email.")

    def show_create_account_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        email_input = TextInput(hint_text="Enter your email", multiline=False, size_hint=(1, None), height=40,
                                background_color=ACCENT_COLOR, foreground_color=TEXT_COLOR)
        password_input = TextInput(hint_text="Create a password", multiline=False, password=True, size_hint=(1, None),
                                   height=40, background_color=ACCENT_COLOR, foreground_color=TEXT_COLOR)
        submit_button = Button(text="Create Account", size_hint=(1, None), height=40, background_color=PRIMARY_COLOR,
                               color=ACCENT_COLOR)
        content.add_widget(email_input)
        content.add_widget(password_input)
        content.add_widget(submit_button)

        popup = Popup(
            title="Create New Account",
            size_hint=(0.8, 0.5),
            content=content,
            separator_height=0,
            background_color=SECONDARY_COLOR
        )
        submit_button.bind(on_press=lambda x: self.create_account(email_input.text, password_input.text, popup))
        popup.open()

    def create_account(self, email, password, popup):
        if email and password:
            print(f"Account created for {email}")
            popup.dismiss()
        else:
            self.show_error_popup("Error", "Please fill in all fields.")