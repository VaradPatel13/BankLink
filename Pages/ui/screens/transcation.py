import firebase_admin
import reportlab
from firebase_admin import credentials, db
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from reportlab.pdfgen import canvas
from kivymd.uix.menu import MDDropdownMenu

PRIMARY_COLOR = (0.29, 0.0, 0.51, 1)
SECONDARY_COLOR = (0.58, 0.44, 0.86, 1)
ACCENT_COLOR = (1, 1, 1, 1)
TEXT_COLOR = (0.2, 0.2, 0.2, 1)
WHITE_COLOR = (1, 1, 1, 1)


FIREBASE_DATABASE_URL = "https://banklink-2025-default-rtdb.firebaseio.com/"

# Initialize Firebase (Ensure the correct path to your Firebase Admin SDK JSON)
if not firebase_admin._apps:
    cred = credentials.Certificate("D:\\Downloads\\BankLink\\Banklink_Desktop\\services\\crendential.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://banklink-2025-default-rtdb.firebaseio.com/'
    })


class TransactionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.transactions = []
        self.dialog = None
        self.layout = BoxLayout(orientation='vertical')

        # Main Layout
        self.layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # **Top App Bar**
        self.app_bar = MDTopAppBar(
            title="Transactions",
            elevation=4,
            md_bg_color=PRIMARY_COLOR,  # Applying Theme
            specific_text_color=WHITE_COLOR
        )
        self.layout.add_widget(self.app_bar)

        # **Search Bar**
        self.search_bar = MDTextField(
            hint_text="Search Transactions",
            size_hint_x=0.9,
            line_color_focus=SECONDARY_COLOR,  # Focused line color
            text_color_normal=TEXT_COLOR,  # Default text color
            text_color_focus=TEXT_COLOR  # Text color when focused
        )
        self.layout.add_widget(self.search_bar)

        # **Buttons (Download & Filter)**
        button_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.download_btn = MDRaisedButton(
            text="Download Statement",
            md_bg_color=PRIMARY_COLOR,
            text_color=WHITE_COLOR,
            on_release=self.download_statement
        )
        self.filter_btn = MDIconButton(
            icon="filter-variant",
            theme_text_color="Custom",
            text_color=PRIMARY_COLOR,
            on_release=self.show_filter_menu
        )
        button_layout.add_widget(self.download_btn)
        button_layout.add_widget(self.filter_btn)
        self.layout.add_widget(button_layout)

        # **Scrollable Transaction List**
        self.scroll_view = MDScrollView()
        self.transaction_list = MDList()
        self.scroll_view.add_widget(self.transaction_list)
        self.layout.add_widget(self.scroll_view)

        # **Bottom Navigation**
        bottom_nav = MDBottomNavigation()
        bottom_nav.text_color_active = PRIMARY_COLOR
        bottom_nav.text_color_normal = (0.6, 0.6, 0.6, 1)  # Gray for inactive

        # **Home Tab**
        home_tab = MDBottomNavigationItem(
            name="home",
            text="Home",
            icon="home",
            on_tab_press=lambda instance: self.switch_screen("dashboard")
        )
        home_tab.theme_text_color = "Custom"
        home_tab.text_color = PRIMARY_COLOR
        home_tab.add_widget(self.layout)  # Attach main layout to Home tab

        # **Scan Tab**
        scan_tab = MDBottomNavigationItem(
            name="scan",
            text="Scan",
            icon="qrcode-scan",
            on_tab_press=lambda instance: self.switch_screen("QR_Scanner")
        )
        scan_tab.theme_text_color = "Custom"
        scan_tab.text_color = PRIMARY_COLOR

        # **History Tab**
        history_tab = MDBottomNavigationItem(
            name="history",
            text="History",
            icon="history",
            on_tab_press=lambda instance: self.switch_screen("transaction_history")
        )
        history_tab.theme_text_color = "Custom"
        history_tab.text_color = PRIMARY_COLOR

        # **Adding Tabs**
        bottom_nav.add_widget(home_tab)
        bottom_nav.add_widget(scan_tab)
        bottom_nav.add_widget(history_tab)

        self.add_widget(bottom_nav)

    def download_statement(self, instance):
        print("Downloading statement...")

    def show_filter_menu(self, instance):
        print("Opening filter options...")

    def switch_screen(self, screen_name):
        print(f"Switching to {screen_name}")  # Debugging
        if screen_name in self.manager.screen_names:
            self.manager.current = screen_name
        else:
            print(f"Screen '{screen_name}' not found!")

    def set_user_id(self, user_id):
        """Set the user ID and fetch transactions."""
        self.user_id = user_id
        print(f"User ID Set: {self.user_id}")  # Debugging output
        self.fetch_transactions()

    def fetch_transactions(self):
        """Fetch transactions from Firebase."""
        ref = db.reference(f'users/{self.user_id}/transactions')
        transactions = ref.get()

        if transactions:
            self.transactions = list(transactions.values())
        else:
            self.transactions = []

        print(f"Fetched {len(self.transactions)} transactions.")  # Debugging print
        self.display_transactions()

    def display_transactions(self):
        # Clear previous transactions
        self.transaction_list.clear_widgets()

        if not self.transactions:
            print("No transactions found!")
            no_data_label = Label(
                text="No transactions available",
                font_size=20,
                color=(1, 1, 1, 1)
            )
            self.transaction_list.add_widget(no_data_label)
            return

        for transaction in self.transactions:
            recipient_id = transaction.get("recipient_id", "Unknown")
            sender_id = transaction.get("sender_id", "Unknown")
            amount = transaction.get("amount", 0)
            date = transaction.get("date", "Unknown")
            transaction_type = "Credit" if self.user_id == recipient_id else "Debit"

            # Fetch user names
            recipient_name = self.fetch_user_name(recipient_id)
            sender_name = self.fetch_user_name(sender_id)

            # Create transaction card
            transaction_card = MDCard(
                orientation="vertical",
                size_hint=(0.9, None),
                height=160,
                padding=15,
                md_bg_color=SECONDARY_COLOR,
                radius=[10, 10, 10, 10],
                elevation=3
            )

            # Box layout inside the card
            card_box = BoxLayout(orientation="vertical", padding=10, spacing=8)
            card_box.add_widget(Label(text=f"Debited From: {sender_name}", font_size=16, color=(1, 1, 1, 1)))
            card_box.add_widget(Label(text=f"Paid To: {recipient_name}", font_size=16, color=(1, 1, 1, 1)))
            card_box.add_widget(Label(text=f"Amount: ₹{amount}", font_size=18,
                                      color=(0, 1, 0, 1) if transaction_type == "Credit" else (1, 0, 0, 1)))
            card_box.add_widget(Label(text=f"Type: {transaction_type}", font_size=14, color=(1, 1, 1, 1)))
            card_box.add_widget(Label(text=f"Date: {date}", font_size=14, color=(0.8, 0.8, 0.8, 1)))

            transaction_card.add_widget(card_box)

            # Debugging print
            print(f"Displaying transaction: {transaction}")

            # Add transaction card to the list
            self.transaction_list.add_widget(transaction_card)

            # Add spacing between cards
            self.transaction_list.add_widget(Widget(size_hint_y=None, height=10))

        # Ensure the layout updates
        self.layout.remove_widget(self.scroll_view)
        self.layout.add_widget(self.scroll_view)

    def fetch_user_name(self, user_id):
        try:
            ref = db.reference(f"users/{user_id}/name")  # Reference to the user's name
            user_name = ref.get()

            if user_name:
                return user_name
            else:
                return "Unknown User"

        except Exception as e:
            print(f"Error fetching user name for {user_id}: {str(e)}")
            return "Unknown User"
    def show_transaction_details(self, transaction):
        """Show transaction details in a dialog."""
        recipient_id = transaction.get("recipient_id", "Unknown")
        sender_id = transaction.get("sender_id", "Unknown")
        amount = transaction.get("amount", 0)
        transaction_id = transaction.get("transaction_id", "N/A")
        transaction_type = "Credit" if self.user_id == recipient_id else "Debit"

        dialog_content = f"""
        Transaction ID: {transaction_id}
        Paid to: {recipient_id}
        Debit from: {sender_id}
        Amount: ₹{amount}
        Type: {transaction_type}
        """

        self.dialog = MDDialog(title="Transaction Details", text=dialog_content, size_hint=(0.9, 0.4))
        self.dialog.open()

    def show_filter_menu(self, instance):
        """Show filter menu for sorting transactions."""
        menu_items = [
            {"text": "Date", "on_release": lambda: self.filter_transactions("date")},
            {"text": "Successful", "on_release": lambda: self.filter_transactions("success")},
            {"text": "Failed", "on_release": lambda: self.filter_transactions("failed")},
            {"text": "Credited", "on_release": lambda: self.filter_transactions("credit")},
            {"text": "Debited", "on_release": lambda: self.filter_transactions("debit")},
        ]
        self.filter_menu = MDDropdownMenu(caller=instance, items=menu_items, width_mult=4)
        self.filter_menu.open()

    def filter_transactions(self, filter_type):
        """Filter transactions based on type."""
        if filter_type == "date":
            self.transactions.sort(key=lambda x: x.get("date", ""), reverse=True)
        elif filter_type == "success":
            self.transactions = [t for t in self.transactions if t.get("status") == "success"]
        elif filter_type == "failed":
            self.transactions = [t for t in self.transactions if t.get("status") == "failed"]
        elif filter_type == "credit":
            self.transactions = [t for t in self.transactions if t.get("recipient_id") == self.user_id]
        elif filter_type == "debit":
            self.transactions = [t for t in self.transactions if t.get("sender_id") == self.user_id]

        self.display_transactions()
        self.filter_menu.dismiss()

    def download_statement(self, instance=None):  # Accept extra argument
        pdf_file = "transactions.pdf"
        c = canvas.Canvas(pdf_file)

        c.setFont("Helvetica", 12)
        c.drawString(100, 800, "Transaction Statement")

        # Example transaction data
        transactions = [
            {"date": "2025-02-25", "amount": "$100", "type": "Debit"},
            {"date": "2025-02-24", "amount": "$250", "type": "Credit"},
            {"date": "2025-02-23", "amount": "$50", "type": "Debit"}
        ]

        y = 780  # Start position
        for tx in transactions:
            c.drawString(100, y, f"{tx['date']} - {tx['type']} - {tx['amount']}")
            y -= 20  # Move down for next entry

        c.save()
        print(f"PDF saved as {pdf_file}")

#
# class BankLinkApp(MDApp):
#     def build(self):
#         screen = TransactionScreen()
#         screen.set_user_id("9kUAijuHmdgKHGl5AwTuS77R28f1")  # Example user ID
#         return screen
#
# if __name__ == "__main__":
#     BankLinkApp().run()
