from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Pages.login import LoginScreen
from Pages.create_account import CreateAccountScreen
from Pages.dashboard import DashboardScreen
from Pages.payment import PaymentScreen
from Pages.user_info import UpdateUserInfoScreen
from Pages.forgot_password_screen import ForgotPasswordScreen
from Pages.To_Mobile import MobilePaymentScreen
from Pages.check_balance import CheckBalanceScreen

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
        screen_manager.add_widget(DashboardScreen(name='dashboard', user_data=user_data))
        screen_manager.add_widget(PaymentScreen(name='payment'))
        screen_manager.add_widget(UpdateUserInfoScreen(name='update_user_info'))
        screen_manager.add_widget(ForgotPasswordScreen(name='forgot_password'))
        screen_manager.add_widget(MobilePaymentScreen(name='mobile_payment'))
        screen_manager.add_widget(CheckBalanceScreen(name='Check_Balance', user_data=user_data))

        return screen_manager

if __name__ == '__main__':
    BankLinkApp().run()
