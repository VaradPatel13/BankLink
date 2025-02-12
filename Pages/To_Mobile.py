from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.anchorlayout import MDAnchorLayout

# Theme Colors
PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)  # Dark Purple (#4B0082)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)  # Light Purple (#9370DB)
ACCENT_COLOR = (1, 1, 1, 1)  # White (#FFFFFF)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)  # Dark Gray (#333333)


class MobilePaymentScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = ACCENT_COLOR  # White background

        # Top Navigation Bar with Back Arrow
        self.toolbar = MDTopAppBar(
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=0,
            md_bg_color=ACCENT_COLOR,  # White background
            specific_text_color=(0, 0, 0, 1)  # Black text color
        )
        self.add_widget(self.toolbar)

        # Centered Layout
        form_layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint=(0.9, None),
            height="200dp",
            pos_hint={"center_x": 0.5}
        )

        self.mobile_input = MDTextField(
            hint_text="Enter Mobile Number",
            mode="rectangle",
            size_hint_x=1,
            font_size="18sp",
            text_color_normal=TEXT_COLOR,
            text_color_focus=TEXT_COLOR,
            line_color_focus=PRIMARY_COLOR
        )

        self.amount_input = MDTextField(
            hint_text="Enter Amount",
            mode="rectangle",
            size_hint_x=1,
            font_size="18sp",
            text_color_normal=PRIMARY_COLOR,
            text_color_focus=TEXT_COLOR,
            line_color_focus=PRIMARY_COLOR
        )

        self.pay_button = MDRaisedButton(
            text="Pay",
            md_bg_color=PRIMARY_COLOR,  # Purple button
            size_hint_x=1,
            font_size="18sp",
            theme_text_color="Custom",
            text_color=ACCENT_COLOR  # White text
        )

        # Add inputs & button to the layout
        form_layout.add_widget(self.mobile_input)
        form_layout.add_widget(self.amount_input)
        form_layout.add_widget(self.pay_button)

        # Centering everything inside an AnchorLayout
        anchor_layout = MDAnchorLayout(anchor_y="center")
        anchor_layout.add_widget(form_layout)

        self.add_widget(anchor_layout)

    def go_back(self):
        print("Back button pressed")