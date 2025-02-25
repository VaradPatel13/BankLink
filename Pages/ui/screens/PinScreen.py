from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.font_definitions import LabelBase
from kivymd.uix.boxlayout import MDBoxLayout
import firebase_admin
from firebase_admin import credentials, db
import bcrypt
import os

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("D:\\Downloads\\BankLink\\Banklink_Desktop\\services\\crendential.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://banklink-2025-default-rtdb.firebaseio.com/'
    })

# Set Window Size
Window.size = (360, 640)

# Font
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets", "Fonts", "Poppins-Bold.ttf"))
if os.path.exists(FONT_PATH):
    LabelBase.register(name="Poppins", fn_regular=FONT_PATH)
else:
    raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
ACCENT_COLOR = (1, 1, 1, 1)  # White
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray


# Screen
class PinEntryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entered_pin = []
        self.transaction_details = None
        self.user_id = None


        # Main Layout
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Bank Header
        header = BoxLayout(orientation="vertical", spacing=0)
        header.add_widget(MDLabel(
            text="BankLink",
            font_name="Poppins",
            halign="center",
            font_size="20sp",
            bold=True
        ))

        # PIN Prompt
        pin_prompt = MDLabel(
            text="ENTER 6-DIGIT UPI PIN",
            font_name="Poppins",
            halign="center",
            font_size="18sp",
            theme_text_color="Primary"
        )

        # PIN Display
        self.pin_display = GridLayout(cols=6, spacing=8, size_hint=(1, None), height=50)
        self.pin_fields = []
        for _ in range(6):
            field = BoxLayout(orientation="vertical")
            lbl = Label(text="_", font_name="Poppins", font_size="24sp", color=(0, 0, 0, 1))
            underline = MDBoxLayout(size_hint_y=None, height=2, md_bg_color=(0.5, 0.5, 0.5, 1))
            field.add_widget(lbl)
            field.add_widget(underline)
            self.pin_fields.append(lbl)
            self.pin_display.add_widget(field)

        # Security Warning
        warning = MDCard(
            size_hint=(0.95, None),
            height=70,
            padding=10,
            radius=[5],
            md_bg_color=(1, 0.96, 0.76, 1),
            line_color=(0.9, 0.9, 0.9, 1)
        )
        warn_layout = BoxLayout(spacing=10)
        warn_layout.add_widget(MDIconButton(
            icon="alert-circle-outline",
            icon_size="24sp",
            theme_text_color="Custom",
            text_color=(1, 0.6, 0, 1)
        ))
        warn_layout.add_widget(MDLabel(
            text="PIN will keep your account secure from unauthorized access.\nDo not share this PIN with anyone.",
            font_name="Poppins",
            font_size="12sp",
            theme_text_color="Secondary"
        ))
        warning.add_widget(warn_layout)

        # Numeric Keypad
        keypad = GridLayout(cols=3, spacing=10, size_hint=(1, None), height=300, padding=10)

        # Number buttons
        keypad = GridLayout(cols=3, spacing=10, size_hint=(1, None), height=300, padding=(80, 20, 0, 10))
        for i in range(1, 10):
            btn = MDRaisedButton(text=str(i), font_name="Poppins", font_size="24sp" , md_bg_color= PRIMARY_COLOR )
            btn.bind(on_press=self.on_key_press)
            keypad.add_widget(btn)

        back_btn = MDIconButton(icon="backspace-outline" )
        back_btn.bind(on_press=self.on_backspace)

        zero_btn = MDRaisedButton(text="0", font_name="Poppins", font_size="24sp" , md_bg_color= PRIMARY_COLOR)
        zero_btn.bind(on_press=self.on_key_press)

        checkmark_btn = MDIconButton(icon="check-bold"  )
        checkmark_btn.bind(on_press=self.on_submit)

        keypad.add_widget(back_btn)
        keypad.add_widget(zero_btn)
        keypad.add_widget(checkmark_btn)

        # Assemble layout
        self.layout.add_widget(header)
        self.layout.add_widget(pin_prompt)
        self.layout.add_widget(self.pin_display)
        self.layout.add_widget(warning)
        self.layout.add_widget(keypad)
        self.add_widget(self.layout)


    def set_transaction_details(self, transaction_details, user_id):
        """Sets transaction details and user ID."""
        self.transaction_details = transaction_details
        self.user_id = user_id
        print(f"✅ Transaction details set in PinEntryScreen: {self.transaction_details}")

    def on_key_press(self, instance):
        if len(self.entered_pin) < 6:
            self.entered_pin.append(instance.text)
            self.pin_fields[len(self.entered_pin) - 1].text = "●"

    def on_backspace(self, instance):
        if self.entered_pin:
            self.pin_fields[len(self.entered_pin) - 1].text = "_"
            self.entered_pin.pop()

    def on_submit(self, instance):
        if len(self.entered_pin) == 6:
            self.verify_pin()

    def verify_pin(self):
        if not self.user_id:
            print("❌ User ID not found.")
            return

        user_ref = db.reference(f'users/{self.user_id}/password')
        stored_hash = user_ref.get()
        entered_pin_str = "".join(self.entered_pin)

        if stored_hash and bcrypt.checkpw(entered_pin_str.encode(), stored_hash.encode()):
            print("✅ PIN verified! Navigating to SuccessScreen...")
            self.manager.get_screen("success_screen").display_transaction_details(self.transaction_details)
            self.manager.current = "success_screen"
        else:
            print("❌ Incorrect PIN. Returning to MobilePaymentScreen.")
            self.manager.current = "mobile_payment"

# Start App Screen
class PinApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return PinEntryScreen()

if __name__ == "__main__":
    PinApp().run()