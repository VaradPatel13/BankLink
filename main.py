from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Pages.login import LoginScreen
from Pages.create_account import CreateAccountScreen
from Pages.dashboard import DashboardScreen
from Pages.payment import PaymentScreen
from Pages.Update_user_info import UpdateUserInfoScreen
from Pages.forgot_password_screen import ForgotPasswordScreen
from Pages.To_Mobile import MobilePaymentScreen
from Pages.check_balance import CheckBalanceScreen
from Pages.User_Info import UserInfoScreen
from Pages.ui.screens.qr_scanner_screen import QRScannerScreen


class BankLinkApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()

        # Sample user data (Replace with actual user details)
        user_id = "user_unique_id"

        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(CreateAccountScreen(name='create_account'))
        screen_manager.add_widget(DashboardScreen(name='dashboard'))
        # screen_manager.add_widget(PaymentScreen(name='payment'))
        screen_manager.add_widget(UserInfoScreen(name='user_info'))
        screen_manager.add_widget(UpdateUserInfoScreen(name='update_user_info'))
        screen_manager.add_widget(ForgotPasswordScreen(name='forgot_password'))
        # screen_manager.add_widget(MobilePaymentScreen(name='mobile_payment'))
        # screen_manager.add_widget(CheckBalanceScreen(name='Check_Balance', user_id = user_id))
        screen_manager.add_widget(QRScannerScreen(name='QR_Scanner'))

        return screen_manager

if __name__ == '__main__':
    BankLinkApp().run()
