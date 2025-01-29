from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Pages.login import LoginScreen
from Pages.create_account import CreateAccountScreen

class BankLinkApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(CreateAccountScreen(name='create_account'))
        return screen_manager

if __name__ == '__main__':
    BankLinkApp().run()