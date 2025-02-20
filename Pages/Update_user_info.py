PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)  # Light Purple
ACCENT_COLOR = (1, 1, 1, 1)  # White
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray

from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image, CoreImage
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class UpdateUserInfoScreen(MDScreen):
    def __init__(self, user_data=None, **kwargs):
        super().__init__(**kwargs)
        self.user_data = user_data
        self.account_number = None

        # Main layout
        self.layout = RelativeLayout()

        logo = Image(
            source='Pages/assets/Bank.png',
            size_hint=(None, None),
            size=(400, 400),
            allow_stretch=True,
            keep_ratio=False,
            pos_hint={'center_x': 0.5 , 'top': 1}
        )
        self.layout.add_widget(logo)


        # Phone/Mobile Row
        self.changepasswordlayout = MDBoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.5}
        )
        self.changepasswordlayout.add_widget(MDRaisedButton(
            text="Change Password",
            md_bg_color=PRIMARY_COLOR,
            text_color=ACCENT_COLOR,
            on_release=self.go_to_user_info
        ))
        self.changepasswordlayout.add_widget(MDRaisedButton(
            text=" Change Mobile ",
            md_bg_color=PRIMARY_COLOR,
            text_color=ACCENT_COLOR,
            on_release=self.go_to_user_info
        ))
        self.layout.add_widget(self.changepasswordlayout)

        # Name/Address Row
        self.name_address_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.4}
        )
        self.name_address_layout.add_widget(MDRaisedButton(
            text="   Change Name    ",
            md_bg_color=PRIMARY_COLOR,
            text_color=ACCENT_COLOR,
            on_release=self.go_to_user_info
        ))
        self.name_address_layout.add_widget(MDRaisedButton(
            text="Change Address",
            md_bg_color=PRIMARY_COLOR,
            text_color=ACCENT_COLOR,
            on_release=self.go_to_user_info
        ))
        self.layout.add_widget(self.name_address_layout)

        # Back Button
        self.back_btn = MDRaisedButton(
            text="Back",
            md_bg_color=PRIMARY_COLOR,
            text_color=ACCENT_COLOR,
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.3}
        )
        self.back_btn.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_btn)

        self.add_widget(self.layout)

    def set_account_number(self, account_number):
        """Sets the account number for the screen."""
        self.account_number = account_number
        print(f"Account number set to: {self.account_number}")

    def go_to_user_info(self, instance):
        self.manager.current = "user_info"

    def go_back(self, instance):
        self.manager.current = "dashboard"
