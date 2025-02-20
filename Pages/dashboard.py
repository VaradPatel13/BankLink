from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.uix.image import Image
from kivy.uix.popup import Popup
import pyqrcode
import os
from kivy.core.text import LabelBase
import firebase_admin
from firebase_admin import db
from services.authentication import decrypt_value
FONT_PATH = "D:\\Downloads\\BankLink\\Banklink_Desktop\\Pages\\assets\\Poppins-Bold.ttf"
LabelBase.register(name="Poppins", fn_regular=FONT_PATH)


# Color Theme
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)
ACCENT_COLOR = (1, 1, 1, 1)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.user_id = None
        self.user_data = None
        self.qr_code_path = ""

    def on_enter(self):
        if self.user_id:
            self.fetch_user_data()
        else:
            self.manager.current = "login"

    def fetch_user_data(self):
        try:
            user_ref = db.reference(f"users/{self.user_id}")
            self.user_data = user_ref.get() or {"name": "Guest", "account_number": "000000"}

            # Decrypt the account number using authentication module
            self.user_data["account_number"] = decrypt_value(self.user_data["account_number"])

            self.qr_code_path = f"{self.user_data['account_number']}_qrcode.png"
            self.generate_qr_code()
            self.build_ui()
        except Exception:
            self.user_data = {"name": "Guest", "account_number": "000000"}
            self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDFloatLayout(md_bg_color=ACCENT_COLOR)


        # 🔹 **Top Bar**
        top_bar = MDBoxLayout(orientation="horizontal", size_hint=(1, 0.12), padding=[20, 10], spacing=10, pos_hint={"top": 1})
        icon = MDIconButton(icon="account-circle", icon_size="56sp", theme_text_color="Custom", text_color=PRIMARY_COLOR, size_hint_x=None, width=60, pos_hint={"center_y": 0.5})
        icon.bind(on_press=self.open_user_info)
        title = MDLabel(text=f"Welcome {self.user_data['name']} 👋! ", font_style="H5", halign="left", font_name="Poppins", theme_text_color="Custom", text_color=TEXT_COLOR, size_hint_x=0.8, valign="center")
        top_bar.add_widget(icon)
        top_bar.add_widget(title)
        layout.add_widget(top_bar)

        # 🔹 **Quick Actions Grid**
        actions_grid = MDGridLayout(cols=2, spacing=15, size_hint=(0.9, None), height=150,
                                    pos_hint={"center_x": 0.5, "top": 0.75})

        buttons = [
            ("To Mobile", "cellphone", "to_mobile"),
            ("To Bank", "bank", "to_bank"),
            ("Check Balance", "cash", "check_balance"),
            ("Update Info", "account-edit", "update_info")
        ]

        for text, icon_name, screen in buttons:
            btn = MDRectangleFlatIconButton(
                text=text,
                icon=icon_name,
                size_hint=(1, None),
                height=50,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                icon_color=(1, 1, 1, 1),
                md_bg_color=PRIMARY_COLOR  # Keep the same background color
            )
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, "current", s))
            actions_grid.add_widget(btn)

        layout.add_widget(actions_grid)

        # 🔹 **QR Code Button**
        qr_button = MDRaisedButton(
            icon="bank",
            text=f"{self.user_data['account_number']}@banklink",
            size_hint=(0.7, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.55},
            md_bg_color=SECONDARY_COLOR,
            text_color=ACCENT_COLOR,
        )
        qr_button.bind(on_press=self.show_qr_code)
        layout.add_widget(qr_button)

        # 🔹 **Payment Methods**
        payment_grid = MDGridLayout(cols=2, spacing=15, size_hint=(0.9, None), height=150,
                                    pos_hint={"center_x": 0.5, "top": 0.4})

        payments = [
            ("NEFT", "credit-card-fast", "neft"),
            ("RTGS", "bank-transfer", "rtgs"),
            ("IMPS", "transfer", "imps"),
            ("UPI", "barcode", "upi")
        ]

        for text, icon_name, screen in payments:
            btn = MDRectangleFlatIconButton(
                text=text,
                icon=icon_name,
                size_hint=(1, None),
                height=50,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),  # White text color for better contrast
                icon_color=(1, 1, 1, 1),  # White icon color
                md_bg_color=PRIMARY_COLOR  # Background color
            )
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, "current", s))
            payment_grid.add_widget(btn)

        layout.add_widget(payment_grid)

        # 🔹 **Bottom Buttons (Scan & History)**
        bottom_buttons = MDBoxLayout(size_hint=(1, 0.15), spacing=20, padding=[20, 10], pos_hint={"bottom": 3})
        scan_btn = MDRaisedButton(
            text="Scan",
            size_hint=(0.4, None),
            height=50,
            md_bg_color=PRIMARY_COLOR,
            icon="qrcode-scan"
        )
        scan_btn.bind(on_press=self.scan_qr_code)

        history_btn = MDRaisedButton(
            text="History",
            size_hint=(0.4, None),
            height=50,
            md_bg_color=PRIMARY_COLOR,
            icon="history"
        )
        history_btn.bind(on_press=self.open_transaction_history)

        bottom_buttons.add_widget(scan_btn)
        bottom_buttons.add_widget(history_btn)
        layout.add_widget(bottom_buttons)

        self.add_widget(layout)

    def scan_qr_code(self, instance):
        """ Open QR Code Scanner """
        self.manager.current = "QR_Scanner"

    def open_transaction_history(self, instance):
        """ Open Transaction History Screen """
        self.manager.current = "transaction_history"

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
            md_bg_color=(1, 1, 1, 1)  # White background
        )

        # QR Code Image
        qr_image = Image(source=self.qr_code_path, size_hint=(1, 1))

        # Label for account number
        acc_label = MDLabel(
            text=account_text,
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.2, 0.2, 0.2, 1)  # Dark text for contrast
        )

        # Close button
        close_button = MDRaisedButton(
            text="Close",
            size_hint=(1, None),
            height=40,
            md_bg_color=(0.29, 0.0, 0.51, 1)  # Primary color
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
            background="assets/white_bg.png",  # A plain white background image (optional)
            separator_color=(0.8, 0.8, 0.8, 1)  # Light grey separator
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


