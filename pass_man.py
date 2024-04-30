#! python3
# pass_man.py - asks user for password then encrypts password
import maskpass
import sys
from cryptography.fernet import Fernet
from pathlib import Path


def create_shadow_file():
    shadow_file_path = (Path.cwd() / Path('shadow'))
    if shadow_file_path.exists() == False:
        shadow_file = open('shadow', 'w')
        shadow_file.close()
        print(shadow_file_path)


def create_password_input():
    # Ask user to create password
    for attempt in range(3):
        password = maskpass.askpass(prompt='Please create a new password: ',mask='') 
        password_confirm = maskpass.askpass(prompt='Please confirm your password: ',mask='')
        if password == password_confirm:
            return password
        else:
            print("Passwords do not match.")
            continue


def create_account():
    # Ask user for username and confirm username is not already in use
    username = input('Please enter your username: ')
    
    usernames = []
    shadow_file = open('shadow', 'r')
    f = shadow_file.read()
    shadow_list = f.split()
    for account in shadow_list:
        usernames.append(account.split(':')[0])
    shadow_file.close()
    print(usernames)

    if username not in usernames:
        # Generate Fernet key
        key= Fernet.generate_key()
        fernet = Fernet(key)

        # call password_input function and encrypt
        encPassword = fernet.encrypt(create_password_input().encode())

        # Write key and password to respective files
        shadow_file = open('shadow', 'a')
        shadow_file.write(username + ':' + str(encPassword) + ':' + str(key) + '\n')
        shadow_file.close()
        print("Account created!")
    else:
        print("Username unavailable")


def authenticate():
    # Ask user for username and password
    username = input('Please enter your username: ')
    password = maskpass.askpass(prompt='Enter your password: ',mask='')


# Call functions based on user input
try:
    if sys.argv[1] == 'create_account':
        try:
            create_shadow_file()
            create_account()
        except:
            print("Username or password not valid.")
    elif sys.argv[1] == 'authenticate':
        authenticate()
    elif sys.argv[1] == 'help':    
        print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
    else:
        print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
except:
        print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")

