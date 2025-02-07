from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle


Window.size = (360, 640)

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)  # Light Purple
ACCENT_COLOR = (1, 1, 1, 1)  # White
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray


class DashboardScreen(Screen):
    def __init__(self, user_data, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.user_data = user_data
        layout = FloatLayout()

        # White Background
        with layout.canvas.before:
            Color(*ACCENT_COLOR)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect)

        # Top Bar with Logo and User Info
        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15),
            pos_hint={'top': 1},
            padding=[20, 10],
            spacing=15
        )

        # App Logo and Title
        logo_title = BoxLayout(orientation='vertical', spacing=0)
        logo_title.add_widget(Label(
            text="BankLink",
            font_size=24,
            color=PRIMARY_COLOR,
            bold=True,
            halign='left',
            size_hint=(1, None),
            height=30
        ))
        logo_title.add_widget(Label(
            text=f"Welcome, {self.user_data['name']}",
            font_size=16,
            color=TEXT_COLOR,
            halign='left',
            size_hint=(1, None),
            height=25
        ))

        # App Icon
        icon = MDIconButton(
            icon="bank",
            theme_text_color="Custom",
            text_color=PRIMARY_COLOR,
            pos_hint={'center_y': 0.5},
            size_hint=(None, None),
            size=(48, 48),
            on_press = self.switch_to_user_info
        )

        top_bar.add_widget(icon)
        top_bar.add_widget(logo_title)
        layout.add_widget(top_bar)

        # Main Buttons Grid
        buttons_grid = GridLayout(
            cols=2,
            spacing=15,
            padding=[20, 0],
            size_hint=(0.9, 0.4),
            pos_hint={'center_x': 0.5, 'top': 0.7}
        )

        buttons = [
            ("To Mobile", self.open_to_mobile),
            ("To Bank/Account", self.open_to_bank),
            ("Cheque Balance", self.open_cheque_balance),
            ("Update Info", self.open_update_info)
        ]

        for text, callback in buttons:
            btn = Button(
                text=text,
                font_size=16,
                bold=True,
                background_color=PRIMARY_COLOR,
                color=ACCENT_COLOR,
                background_normal='',
                size_hint=(1, None),
                height=70
            )
            btn.bind(on_press=callback)
            buttons_grid.add_widget(btn)

        layout.add_widget(buttons_grid)

        # ID Button
        id_button = Button(
            text=f"{self.user_data['account_number']}@banklink",
            size_hint=(0.7, None),
            height=45,
            pos_hint={'center_x': 0.5, 'top': 0.35},
            background_color=SECONDARY_COLOR,
            color=ACCENT_COLOR,
            font_size=14,
            bold=True,
            background_normal=''
        )
        layout.add_widget(id_button)

        # Transaction Buttons
        transaction_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(0.8, 0.08),
            pos_hint={'center_x': 0.5, 'top': 0.25}
        )

        for text, callback in [("NEFT", self.open_neft), ("RTGS", self.open_rtgs), ("IMPS", self.open_imps)]:
            btn = Button(
                text=text,
                font_size=14,
                bold=True,
                background_color=PRIMARY_COLOR,
                color=ACCENT_COLOR,
                background_normal='',
                size_hint=(0.33, 1)
            )
            btn.bind(on_press=callback)
            transaction_layout.add_widget(btn)

        layout.add_widget(transaction_layout)

        # Bottom Navigation
        nav_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(0.9, 0.1),
            pos_hint={'center_x': 0.5, 'bottom': 0.05}
        )

        for text, callback in [("Home", self.open_dashboard), ("Scan", self.open_qr_scanner),
                               ("History", self.open_transactions)]:
            btn = Button(
                text=text,
                font_size=14,
                bold=True,
                background_color=PRIMARY_COLOR,
                color=ACCENT_COLOR,
                background_normal='',
                size_hint=(0.33, 1),
                border=(25, 25, 25, 25)
            )
            btn.bind(on_press=callback)
            nav_layout.add_widget(btn)

        layout.add_widget(nav_layout)

        self.add_widget(layout)

    def switch_to_user_info(self, instance):
        """Switch to User Info Screen"""
        if self.manager.has_screen('user_info'):
            self.manager.remove_widget(self.manager.get_screen('user_info'))

        user_info_screen = UserInfoScreen(user_data=self.user_data, name='user_info')
        self.manager.add_widget(user_info_screen)
        self.manager.current = 'user_info'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_to_mobile(self, instance):
        print("Navigating to Mobile Transfer...")

    def open_to_bank(self, instance):
        print("Navigating to Bank Transfer...")

    def open_cheque_balance(self, instance):
        print("Checking Cheque Balance...")

    def open_update_info(self, instance):
        print("Opening Update Info...")

    def open_neft(self, instance):
        print("NEFT Transaction...")

    def open_rtgs(self, instance):
        print("RTGS Transaction...")

    def open_imps(self, instance):
        print("IMPS Transaction...")

    def open_dashboard(self, instance):
        print("Going to Dashboard...")

    def open_qr_scanner(self, instance):
        print("Opening QR Scanner...")

    def open_transactions(self, instance):
        print("Showing Transaction History...")


class UserInfoScreen(Screen):
    def __init__(self, user_data, **kwargs):
        super(UserInfoScreen, self).__init__(**kwargs)
        self.user_data = user_data
        layout = FloatLayout()

        # White Background
        with layout.canvas.before:
            Color(*ACCENT_COLOR)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect)

        # Back Button
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=PRIMARY_COLOR,
            pos_hint={'x': 0.02, 'top': 0.98},
            size_hint=(None, None),
            size=(48, 48)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        # User Info
        info_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=30,
            size_hint=(0.9, 0.7),
            pos_hint={'center': (0.5, 0.55)}
        )

        fields = [
            ("Name", self.user_data['name']),
            ("Address", self.user_data['address']),
            ("Mobile", self.user_data['mobile']),
            ("Account", self.user_data['account_number'])
        ]

        for label, value in fields:
            info_layout.add_widget(Label(
                text=f"[b]{label}:[/b] {value}",
                markup=True,
                font_size=18,
                color=TEXT_COLOR,
                halign='left'
            ))

        layout.add_widget(info_layout)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'dashboard'