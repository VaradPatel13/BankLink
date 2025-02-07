from kivymd.app import MDApp  # ✅ Use MDApp instead of App
from kivy.uix.screenmanager import ScreenManager
from Pages.login import LoginScreen
from Pages.create_account import CreateAccountScreen
from Pages.dashboard import DashboardScreen
from Pages.payment import PaymentScreen
from Pages.user_info import UserInfoScreen
from Pages.forgot_password_screen import ForgotPasswordScreen

class BankLinkApp(MDApp):  # ✅ Change App to MDApp
    def build(self):
        screen_manager = ScreenManager()

        # Sample user data (Replace with actual user details)
        user_data = {
            "name": "John Doe",
            "address": "123 Street, City",
            "mobile": "9876543210",
            "account_number": "123456789"
        }

        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(CreateAccountScreen(name='create_account'))
        screen_manager.add_widget(DashboardScreen(name='dashboard', user_data=user_data))  # ✅ FIXED
        screen_manager.add_widget(PaymentScreen(name='payment'))
        screen_manager.add_widget(UserInfoScreen(name='user_info'))
        screen_manager.add_widget(ForgotPasswordScreen(name='forgot_password'))

        return screen_manager

if __name__ == '__main__':
    BankLinkApp().run()
