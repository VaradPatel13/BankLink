from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class QRScannerScreen(Screen):
    def __init__(self, **kwargs):
        super(QRScannerScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="QR Scanner"))
        self.add_widget(layout)