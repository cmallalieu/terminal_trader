
def user_menu():
    print(
"""Welcome to Terminal Trader!

1) Login
2) Create Account
3) Quit
""")

def main_menu(user):
    print(
f"""Welcome to Terminal Trader, {user.realname}

Balance: ${user.balance:.2f}

1) See positions
2) Look up stock price
3) Buy
4) Sell
5) See trade history
6) See trade history for one stock
7) Deposit money
8) Look up ticker symbol
9) See API Key
10) Logout

""")

def get_choice():
    return input("  What is your selection: ")

def error_bad_input():
    print(
""" Did not recognize that input.
""")

def goodbye():
    print("""
Goodbye!""")
