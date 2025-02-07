from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class RTGSScreen(Screen):
    def __init__(self, **kwargs):
        super(RTGSScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Input Fields
        self.account_input = TextInput(
            hint_text="Beneficiary Account Number",
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        self.amount_input = TextInput(
            hint_text="Amount (Minimum ₹2,00,000)",
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        self.ifsc_input = TextInput(
            hint_text="IFSC Code",
            multiline=False,
            size_hint=(1, None),
            height=50
        )

        # Submit Button
        submit_button = Button(
            text="Send via RTGS",
            size_hint=(1, None),
            height=50,
            background_color=(0.29, 0.0, 0.51, 1),  # Dark Purple
            color=(1, 1, 1, 1)  # White
        )
        submit_button.bind(on_press=self.process_rtgs)

        # Add widgets to layout
        layout.add_widget(Label(text="RTGS Transfer", font_size=24))
        layout.add_widget(self.account_input)
        layout.add_widget(self.ifsc_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def process_rtgs(self, instance):
        account = self.account_input.text
        amount = self.amount_input.text
        ifsc = self.ifsc_input.text
        print(f"RTGS Transfer: {amount} to {account} (IFSC: {ifsc})")
        # Add your logic here