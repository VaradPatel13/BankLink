from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class UserInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(UserInfoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Name: John Doe"))
        layout.add_widget(Label(text="Mobile: 1234567890"))
        layout.add_widget(Label(text="Address: 123 Main St"))
        layout.add_widget(Label(text="Account Number: 123456789"))
        layout.add_widget(Label(text="QR Code: [QR Code Image]"))
        self.add_widget(layout)