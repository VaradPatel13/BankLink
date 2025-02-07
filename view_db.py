import sqlite3

# Database file
DB_NAME = "banklink.db"

# Theme Colors (ANSI Escape Codes)
PRIMARY_COLOR = "\033[38;2;74;0;130m"  # Dark Purple (#4B0082)
SECONDARY_COLOR = "\033[38;2;148;112;219m"  # Light Purple (#9370DB)
ACCENT_COLOR = "\033[38;2;255;255;255m"  # White (#FFFFFF)
TEXT_COLOR = "\033[38;2;51;51;51m"  # Dark Gray (#333333)
RESET = "\033[0m"


def view_all_users():
    """Fetch and display all users from the database with themed styling."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    if not users:
        print(f"{PRIMARY_COLOR}No users found in the database.{RESET}")
        return

    # Header Section
    print(f"\n{PRIMARY_COLOR}📌 All Registered Users 📌{RESET}")
    print(f"{PRIMARY_COLOR}{'-' * 60}{RESET}")

    # Column Headers
    print(f"{SECONDARY_COLOR}{'{:<15} {:<20} {:<15} {:<10} {:<10}'.format(
        'Account No.', 'Name', 'Mobile', 'Balance', 'Address')}{RESET}")

    print(f"{PRIMARY_COLOR}{'-' * 60}{RESET}")

    # Data Rows
    for user in users:
        account_number, name, address, mobile, password, balance = user
        row = (
            f"{TEXT_COLOR}{account_number:<15} {name:<20} {mobile:<15} "
            f"{ACCENT_COLOR}{balance:<10.2f}{TEXT_COLOR} {address:<10}{RESET}"
        )
        print(row)


if __name__ == "__main__":
    view_all_users()