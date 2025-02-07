from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

class IMPSScreen(Screen):
    def __init__(self, **kwargs):
        super(IMPSScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Input Fields
        self.account_input = TextInput(
            hint_text="Beneficiary Account/Mobile Number",
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        self.amount_input = TextInput(
            hint_text="Amount",
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        self.priority_dropdown = DropDown()

        # Priority Selection
        priority_button = Button(
            text="Select Priority",
            size_hint=(1, None),
            height=50,
            background_color=(0.58, 0.44, 0.86, 1)  # Light Purple
        )
        for priority in ["Normal", "Immediate"]:
            btn = Button(
                text=priority,
                size_hint_y=None,
                height=44,
                background_color=(0.29, 0.0, 0.51, 1)
            )
            btn.bind(on_release=lambda btn: self.select_priority(btn.text))
            self.priority_dropdown.add_widget(btn)
        priority_button.bind(on_release=self.priority_dropdown.open)

        # Submit Button
        submit_button = Button(
            text="Send via IMPS",
            size_hint=(1, None),
            height=50,
            background_color=(0.29, 0.0, 0.51, 1),
            color=(1, 1, 1, 1)
        )
        submit_button.bind(on_press=self.process_imps)

        # Add widgets to layout
        layout.add_widget(Label(text="IMPS Transfer", font_size=24))
        layout.add_widget(self.account_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(priority_button)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def select_priority(self, priority):
        print(f"Selected Priority: {priority}")

    def process_imps(self, instance):
        account = self.account_input.text
        amount = self.amount_input.text
        print(f"IMPS Transfer: {amount} to {account}")
        # Add your logic here