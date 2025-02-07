from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class TransactionsScreen(Screen):
    def __init__(self, **kwargs):
        super(TransactionsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Transaction History"))
        self.add_widget(layout)