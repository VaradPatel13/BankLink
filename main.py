from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Pages.login import LoginScreen
from Pages.create_account import CreateAccountScreen
from Pages.dashboard import DashboardScreen
from Pages.ui.screens.Update_user_info import UpdateUserInfoScreen
from Pages.forgot_password_screen import ForgotPasswordScreen
from Pages.ui.screens.To_Mobile import MobilePaymentScreen
from Pages.ui.screens.User_Info import UserInfoScreen
from Pages.ui.screens.qr_scanner_screen import QRScannerScreen
from Pages.ui.screens.PinScreen import PinEntryScreen
from Pages.ui.screens.SuccessScreen import SuccessScreen
from Pages.ui.screens.check_balance import CheckBalanceScreen
from Pages.ui.screens.Account_Payment import AccountPaymentScreen
from Pages.ui.screens.Electronic_Fund_Transfer import FundTransferScreen
from Pages.ui.screens.transcation import TransactionScreen


class BankLinkApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(CreateAccountScreen(name='create_account'))
        screen_manager.add_widget(DashboardScreen(name='dashboard'))
        screen_manager.add_widget(UserInfoScreen(name='user_info'))
        screen_manager.add_widget(UpdateUserInfoScreen(name='update_user_info'))
        screen_manager.add_widget(ForgotPasswordScreen(name='forgot_password'))
        screen_manager.add_widget(MobilePaymentScreen(name='mobile_payment'))
        screen_manager.add_widget(CheckBalanceScreen(name='Check_Balance'))
        screen_manager.add_widget(QRScannerScreen(name='QR_Scanner'))
        screen_manager.add_widget(SuccessScreen(name='success_screen'))
        screen_manager.add_widget(PinEntryScreen(name='pin_entry_screen'))
        screen_manager.add_widget(AccountPaymentScreen(name='account_payment'))
        screen_manager.add_widget(FundTransferScreen(name='fund_transfer'))
        screen_manager.add_widget(TransactionScreen(name='transaction_history'))

        return screen_manager

if __name__ == '__main__':
    BankLinkApp().run()
