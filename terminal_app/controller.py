from . import view
from model.user import User
from model.util import get_price, get_ticker

def run():
    # when user logs in, go to the main menu, when menu is exited, return to
    # login
    while True:
        user = login_loop()
        if user is None:
            break
        main_loop(user)

def login_loop():
    """ Presents the user with an interactive menu to log into the system,
    create an account, or quit. Returns a User object on successful login or
    None on quit """

    while True:
        view.user_menu()
        choice = view.get_choice()

        if choice.strip() == "3":
            # quit
            view.goodbye()
            return None
        
        elif choice.strip() == "1":
            user = user_password_attempt()
            if user is not None:
                return main_loop(user)
            else:
                print("\nEither Username or password is incorrect...Please try again \n")
                continue
        
        elif choice.strip() == "2":
            create_user()
        else:
            view.error_bad_input()
            continue

def create_user():
    username = input('Enter a username: ')
    password = input('Enter a password: ')
    realname = input('Enter a realname: ')
    balance = input("Enter a starting balance: ")
    new_user = User(username= username, password= password, realname= realname, balance=balance)
    new_user.hash_password(password)
    new_user.generate_api_key()
    new_user.save()
    login_loop()




def main_loop(user):
    while True:
        view.main_menu(user)
        choice = view.get_choice()
        if choice.strip() == "10":
            return login_loop()
        if choice.strip()== "9":
            print(user.api_key)
            main_loop(user)        
        if choice.strip() == "8":
            company_name = input("Enter company name: ")
            print(get_ticker(company_name))
            main_loop(user)        
        if choice.strip() == "7":
            new_deposit = int(input("Enter deposit amount: $"))
            user.balance +=new_deposit
            user.save()
            main_loop(user)
        if choice.strip()== "6":
            ticker = input("Enter ticker symbol: ")
            print(user.trades_for(ticker))
            main_loop(user)
        if choice.strip()== "5":
            print(user.all_trades())
            main_loop(user)
        if choice.strip()== "4":
            ticker = input("Enter ticker symbol: ")
            amount = int(input("Enter amount of shares you want to sell: "))
            user.sell(ticker,amount)
            main_loop(user)
        if choice.strip() =='3':
            ticker = input("Enter ticker symbol: ")
            amount = int(input("Enter amount of shares you want to buy: "))
            user.buy(ticker,amount)
            main_loop(user)
        if choice.strip()=="2":
            ticker = input("Enter ticker symbol: ")
            print(get_price(ticker))
            main_loop(user)
        if choice.strip()=="1":
            print(user.all_positions())
            main_loop(user)
        else:
            view.error_bad_input()
            continue

def user_password_attempt():
    """ input username and password, on successful login, return the user object
    on a failed login return none """
    username = input('enter username: ')
    password = input('enter password: ')
    return User.login(username,password)

