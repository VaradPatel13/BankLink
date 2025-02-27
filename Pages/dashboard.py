# DashBoard Screen

import os
import pyqrcode
import firebase_admin
from firebase_admin import db
from services.authentication import decrypt_value
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import  MDFillRoundFlatButton, MDFloatingActionButtonSpeedDial, MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.core.text import LabelBase


import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Then load your font:
font_path = resource_path(os.path.join("Pages", "assets", "Fonts", "Poppins-Bold.ttf"))

# Color Theme
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)
ACCENT_COLOR = (1, 1, 1, 1)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)
WHITE_COLOR = (1, 1, 1, 1)

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.user_id = None
        self.user_data = None
        self.qr_code_path = ""
        self.qr_code_directory = r"D:\\Downloads\\BankLink\\Banklink_Desktop\\Pages\\assets\\qr_codes"

    def on_enter(self):
        if self.user_id:
            self.fetch_user_data()
        else:
            self.manager.current = "login"

    def fetch_user_data(self):
        try:
            user_ref = db.reference(f"users/{self.user_id}")
            self.user_data = user_ref.get() or {"name": "Guest", "account_number": "000000"}
            self.user_data["account_number"] = decrypt_value(self.user_data["account_number"])
            self.qr_code_path = os.path.join(self.qr_code_directory, f"{self.user_data['account_number']}_qrcode.png")
            self.generate_qr_code()
            self.build_ui()
        except Exception:
            self.user_data = {"name": "Guest", "account_number": "000000"}
            self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDFloatLayout(md_bg_color=ACCENT_COLOR)

        # TOP BAR
        top_bar = MDBoxLayout(orientation="horizontal", size_hint=(1, 0.12), padding=[20, 10], spacing=10,
                              pos_hint={"top": 1})

        icon = MDFillRoundFlatIconButton(
            text="Profile",
            icon="account-circle",
            theme_icon_color="Custom",
            icon_color=PRIMARY_COLOR,
            text_color=PRIMARY_COLOR,
            line_color=PRIMARY_COLOR,
            md_bg_color=ACCENT_COLOR,
            size_hint=(None, None),
            width=180,
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        icon.bind(on_press=self.open_user_info)

        title = MDLabel(
            text=f"Welcome {self.user_data['name']} !",
            font_style="H5",
            halign="left",
            font_name="Poppins",
            theme_text_color="Custom",
            text_color=TEXT_COLOR,
            size_hint_x=0.8,
            valign="center",
            markup=True
        )

        top_bar.add_widget(icon)
        top_bar.add_widget(title)
        layout.add_widget(top_bar)

        # ACTION BUTTONS GRID
        actions_grid = MDGridLayout(cols=2, spacing=15, size_hint=(0.9, None), height=150,
                                    pos_hint={"center_x": 0.5, "top": 0.75})

        buttons = [
            ("To Mobile", "cellphone", "mobile_payment"),
            ("To Bank", "bank", "account_payment"),
            ("Check Balance", "cash", "Check_Balance"),
            ("Update Info", "account-edit", "update_user_info")
        ]
        for text, icon_name, screen in buttons:
            btn = MDFillRoundFlatIconButton(
                text=text,
                icon=icon_name,
                size_hint=(1, None),
                height=50,
                theme_text_color="Custom",
                text_color=WHITE_COLOR,
                icon_color=WHITE_COLOR,
                md_bg_color=PRIMARY_COLOR
            )
            btn.bind(on_press=lambda x, s=screen: self.switch_screen(s, self.user_id))

            actions_grid.add_widget(btn)

        layout.add_widget(actions_grid)

        # QR CODE BUTTON
        qr_button = MDFillRoundFlatButton(
            text=f"{self.user_data['account_number']}@banklink",
            size_hint=(0.7, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.52},
            md_bg_color=SECONDARY_COLOR,
            text_color=ACCENT_COLOR,
        )
        qr_button.bind(on_press=self.show_qr_code)
        layout.add_widget(qr_button)

        # Rewards, Offers, and Referrals Buttons
        extra_buttons_grid = MDGridLayout(cols=3, spacing=10, size_hint=(0.9, None), height=50,
                                          pos_hint={"center_x": 0.5, "top": 0.39})

        extra_buttons = [
            ("Rewards", "gift", self.show_rewards),
            ("Offers", "tag", self.show_offers),
            ("Referrals", "account-multiple", self.show_referrals)
        ]

        for text, icon_name, callback in extra_buttons:
            btn = MDFillRoundFlatIconButton(
                text=text,
                icon=icon_name,
                size_hint=(1, None),
                height=50,
                theme_text_color="Custom",
                text_color=WHITE_COLOR,
                icon_color=WHITE_COLOR,
                md_bg_color=PRIMARY_COLOR
            )
            btn.bind(on_press=callback)
            extra_buttons_grid.add_widget(btn)

        layout.add_widget(extra_buttons_grid)

        # PAYMENT METHODS GRID
        payment_grid = MDGridLayout(cols=2, spacing=15, size_hint=(0.9, None), height=150,
                                    pos_hint={"center_x": 0.5, "bottom": 2})

        payments = [
            ("NEFT", "credit-card-fast", "fund_transfer"),
            ("RTGS", "bank-transfer", "fund_transfer"),
            ("IMPS", "transfer", "fund_transfer"),
            ("UPI", "barcode", "mobile_payment")
        ]

        for text, icon_name, screen in payments:
            btn = MDFillRoundFlatIconButton(
                text=text,
                icon=icon_name,
                size_hint=(1, None),
                height=50,
                theme_text_color="Custom",
                text_color=WHITE_COLOR,
                icon_color=WHITE_COLOR,
                md_bg_color=PRIMARY_COLOR
            )
            btn.bind(on_press=lambda x, s=screen: self.switch_screen(s, self.user_id))
            payment_grid.add_widget(btn)

        layout.add_widget(payment_grid)

        # BOTTOM NAVIGATION
        bottom_nav = MDBottomNavigation()
        bottom_nav.text_color_active = PRIMARY_COLOR  # Active tab color
        bottom_nav.text_color_normal = (0.6, 0.6, 0.6, 1)  # Inactive tab color

        # HOME TAB
        home_tab = MDBottomNavigationItem(
            name="home", text="Home", icon="home",
            on_tab_press=lambda instance: self.switch_screen("dashboard", self.user_id)
        )
        home_tab.theme_text_color = "Custom"
        home_tab.text_color = PRIMARY_COLOR
        home_tab.add_widget(layout)  # Attach main layout to home tab

        # SCAN TAB
        scan_tab = MDBottomNavigationItem(
            name="scan", text="Scan", icon="qrcode-scan",
            on_tab_press=lambda instance: self.switch_screen("QR_Scanner", self.user_id),
        )
        scan_tab.theme_text_color = "Custom"
        scan_tab.text_color = PRIMARY_COLOR

        # HISTORY TAB
        history_tab = MDBottomNavigationItem(
            name="history", text="History", icon="history",
            on_tab_press=lambda instance: self.switch_screen("transaction_history", self.user_id),
        )
        history_tab.theme_text_color = "Custom"
        history_tab.text_color = PRIMARY_COLOR

        # ADDING TABS
        bottom_nav.add_widget(home_tab)
        bottom_nav.add_widget(scan_tab)
        bottom_nav.add_widget(history_tab)

        self.add_widget(bottom_nav)

    # def switch_screen_main(self, screen_name):
    #     """ Switch screens when a navigation button is clicked. """
    #     if screen_name in self.manager.screen_names:
    #         print(f"Switching to {screen_name}")
    #         self.manager.current = screen_name
    #     else:
    #         print(f"Screen '{screen_name}' not found!")

    def show_qr_code(self, instance):
        self.generate_qr_code()

        # Extract last 4 digits of account number
        last_four_digits = self.user_data["account_number"][-4:]
        account_text = f"BankLink@{last_four_digits}"

        # Create a layout for the popup
        popup_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
            md_bg_color=(1, 1, 1, 1)
        )

        # QR Code Image
        qr_image = Image(source=self.qr_code_path, size_hint=(1, 1))

        # Label for account number
        acc_label = MDLabel(
            text=account_text,
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.2, 0.2, 0.2, 1)
        )

        # Close button
        close_button = MDRaisedButton(
            text="Close",
            size_hint=(1, None),
            height=40,
            md_bg_color=(0.29, 0.0, 0.51, 1)
        )

        # Add widgets to layout
        popup_layout.add_widget(qr_image)
        popup_layout.add_widget(acc_label)
        popup_layout.add_widget(close_button)

        # Create the popup with a white background
        popup = Popup(
            title="Your QR Code",
            content=popup_layout,
            size_hint=(0.8, 0.6),
            background="assets/white_bg.png",
            separator_color=(0.8, 0.8, 0.8, 1)
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def generate_qr_code(self):
        if not os.path.exists(self.qr_code_path):
            qr = pyqrcode.create(self.user_data["account_number"])
            qr.png(self.qr_code_path, scale=6)

    def open_user_info(self, instance):
        if self.user_id:
            user_info_screen = self.manager.get_screen('user_info')
            user_info_screen.set_user_id(self.user_id)
            self.manager.current = "user_info"
        else:
            print("User ID not found! Redirecting to login.")
            self.manager.current = "login"

    def open_more_options(self, instance):
        """ Function for handling Extended FAB click """
        print("More options clicked!")

    def show_rewards(self, instance):
        """ Function to display rewards page or popup """
        print("Showing Rewards")

    def show_offers(self, instance):
        """ Function to display offers page or popup """
        print("Showing Offers")

    def show_referrals(self, instance):
        """ Function to display referrals page or popup """
        print("Showing Referrals")

    def switch_screen(self, screen_name, user_id):
        print("Switching to screen: ", screen_name)
        # print(f"Switching to {screen_name} with User ID: {user_id}")
        if screen_name in self.manager.screen_names:
            # print("user_id: ", user_id)
            target_screen = self.manager.get_screen(screen_name)
            if hasattr(target_screen, "set_user_id"):
                target_screen.set_user_id(user_id)
            self.manager.current = screen_name
        else:
            print(f"Screen '{screen_name}' not found!")





