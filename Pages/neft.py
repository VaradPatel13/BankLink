from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class NEFTScreen(Screen):
    def __init__(self, **kwargs):
        super(NEFTScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Input Fields
        self.account_input = TextInput(
            hint_text="Beneficiary Account Number",
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
        self.remarks_input = TextInput(
            hint_text="Remarks",
            multiline=False,
            size_hint=(1, None),
            height=50
        )

        # Submit Button
        submit_button = Button(
            text="Send via NEFT",
            size_hint=(1, None),
            height=50,
            background_color=(0.29, 0.0, 0.51, 1),  # Dark Purple
            color=(1, 1, 1, 1)  # White
        )
        submit_button.bind(on_press=self.process_neft)

        # Add widgets to layout
        layout.add_widget(Label(text="NEFT Transfer", font_size=24))
        layout.add_widget(self.account_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(self.remarks_input)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def process_neft(self, instance):
        account = self.account_input.text
        amount = self.amount_input.text
        remarks = self.remarks_input.text
        print(f"NEFT Transfer: {amount} to {account} (Remarks: {remarks})")
        # Add your logic here (e.g., API call to process NEFT)