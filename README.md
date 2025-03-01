# 🏦 BankLink - Secure Banking Management System

![BankLink Logo](https://github.com/VaradPatel13/BankLink/blob/main/Pages/assets/Images/logo.PNG)

**BankLink** is a secure and feature-rich banking management application that allows users to manage their accounts, transfer funds, and make QR-based payments.
The system is built using **Kivy** for the frontend and **Firebase** for authentication and real-time database management.
## 🚀 Features

- **🔒 Secure Authentication** (Mobile Number & Account Number)
- **📈 Real-time Balance Check**
- **💳 Money Transfers** (Mobile Number & Account Number)
- **🗃️ QR Code Payment System**
- **💵 NEFT, RTGS, IMPS Payment Support**
- **🔄 Update User Information**
- **📃 Transaction History & Notifications**
- **🎨 Modern & User-Friendly UI** (Built with Kivy & Material Design)
- **💪 Firebase Integration** (Authentication & Database)

---

## 🛠️ Installation & Setup

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/BankLink.git
cd BankLink
```

### 2. **Install Dependencies**
Ensure you have **Python 3.8+** installed, then install the required modules:
```bash
pip install -r requirements.txt
```

### 3. **Setup Firebase**
1. Go to [Firebase Console]
2. Create a new project and enable **Authentication** & **Realtime Database**.
3. Download the `crendential.json` file and place it inside `services/` directory.
4. Ensure `firebase_config.json` is correctly configured.

### 4. **Run the Application**
```bash
python main.py
```

## 🔧 Build as an Executable (Windows)
To package the app into an **EXE file** using PyInstaller:
```bash
pyinstaller --onefile --add-data "services/crendential.json;services" --hidden-import "kivymd" main.py
```
This will generate an `exe` file inside the `dist/` folder.

---
📜 Project Flow & Details – BankLink
1️⃣ Overview
BankLink is a secure banking management system that allows users to manage accounts, send/receive money, and make QR-based payments. 
It is designed with Kivy (frontend) and Firebase (backend), ensuring a smooth and modern user experience.

2️⃣ Project Workflow & Navigation Flow
🔹 Authentication Flow
User opens the app → Lands on the Login Screen.
User → Log in using Mobile Number or Account Number.
Firebase Authentication verifies user credentials.
If valid → Redirects to the Dashboard.
If invalid → Displays an error message.

🔹 Dashboard Flow
After login, users see the Dashboard with multiple options:
Check Balance
Send Money
QR Code Payment
Transaction History
Update Profile

🔹 Sending Money Flow
User selects "Send Money".
Chooses recipient type:
Mobile Number (Phone-based transfer)
Account Number (Bank transfer)
Selects Payment Mode:
NEFT, RTGS, IMPS → Standard banking transfers.
QR Code → Scans and sends payment.
Transaction is processed and saved in Firebase.
User receives a confirmation notification.

 🔹 Checking Balance Flow
User taps "Check Balance".
The app fetches real-time balance from Firebase.
UI displays:
✅ Green Checkmark for success.
🏦 Masked Account Number (e.g., BankLink-1234).
💰 Current Balance.

🔹 QR Code Payment Flow
User chooses "QR Code Payment".
Two options:
Generate QR Code → Displays user’s payment QR.
Scan QR Code → Opens camera to scan another user’s QR.
If scanning:
Extracts recipient details.
Confirms & processes payment.
If generating:
Displays user’s own QR code to receive payments.

🔹 Transaction History Flow
User selects "Transaction History".
The app fetches all past transactions from Database.
Displays a list with details:
✅ Status (Success/Failed)
📅 Date & Time
🔄 Transaction Type (NEFT, RTGS, IMPS, QR)
💵 Amount Sent/Received

🔹 Updating User Profile
User selects "Update Profile".
Modifies personal details (Name, Address, Mobile).
Updates password (encrypted).
Saves changes to Firebase Realtime.

5️⃣ Security & Data Privacy
🔐 Security Measures:
Passwords are hashed.
Sensitive data  is encrypted.
Firebase Rules prevent unauthorized data access.

6️⃣ Additional Features to Consider
💡 Enhancements you can add:
Push Notifications for real-time transaction alerts.
Auto-Saving Beneficiaries for quick money transfers.



## 📞 Contact
👉 **Developer:** [Varad](https://github.com/VaradPatel13)  
👉 **Email:** varadp216@gmail.com.
👉 **GitHub:** [https://github.com/VaradPatel13/BankLink](https://github.com/VaradPatel13/BankLink) 
👉 **Figma Design:** https://www.figma.com/design/qSZMCnnXdu9zmhhzAhHbZj/Banklink?node-id=0-1&t=l9hcDDmn7o07lgoW-1
👉 **LinkedIn:** [www.linkedin.com/in/varad-patel](www.linkedin.com/in/varad-patel)  

