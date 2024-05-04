#! python3
# pass_man.py - Creates and stores username and encrypted password in shadow file, then
# authenticates user login with account in shadow file
import maskpass
import sys
import hashlib
import os


def create_password_input():
    # Ask user to create password
    for attempt in range(3):
        password = maskpass.askpass(prompt='Please create a new password: ',mask='') 
        password_confirm = maskpass.askpass(prompt='Please confirm your password: ',mask='')
        if password != password_confirm:
            print("Passwords do not match.")
            continue
        # Validate password and return if valid
        pass_valid = False
        symbols = {'!','@','#','$','%','&','_','-'}
        pass_valid = all([
            any(char.isupper for char in password),
            any(char.islower for char in password),
            any(char.isdigit for char in password),
            any(char in symbols for char in password),
            len(password) >= 14
            ])
        if pass_valid == True:
            return password
        else:
            print("Password invalid.")
            continue


def create_account():
    # Ask user for username and confirm username is not already in use
    username = input("Please enter your username: ")
    
    usernames = []
    shadow_file = open('shadow', 'r')
    f = shadow_file.read()
    print(f)
    shadow_list = f.split()
    for account in shadow_list:
        usernames.append(account.split(':')[0])
    shadow_file.close()
    print(usernames)

    if username not in usernames:

        # call password_input function and encrypt
        salt = os.urandom(32)
        encPassword = hashlib.pbkdf2_hmac('sha512', create_password_input().encode(), salt, 100000)

        # Write key and password to respective files
        shadow_file = open('shadow', 'a')
        shadow_file.write(username + ':' + encPassword.hex() + ':' + salt.hex() + '\n')
        shadow_file.close()
        print("Account created!")
    else:
        print("Username unavailable")


def authenticate():
    # Ask user for username and password
    username = input("Please enter your username: ")
    password = maskpass.askpass(prompt="Enter your password: ",mask='')
    
    # Open shadow file to compare real password hash with authenticating password hash
    shadow_file = open('shadow', 'r')
    for account in shadow_file:
        if account.split(':')[0] == username:
            originEncPass = bytes.fromhex(account.split(':')[1])
            salt = bytes.fromhex(account.split(':')[2])
            authEncPass = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)
            if authEncPass == originEncPass: 
                print("Login successful!")
            else:
                print("Login failed!")
    shadow_file.close()


# Call functions based on user input
def main():    
    try:
        if sys.argv[1] == 'create_account':
            try:
                create_account()
            except:
                print("Username or password not valid.")
        elif sys.argv[1] == 'authenticate':
            authenticate()
        elif sys.argv[1] == 'help':    
            print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
        else:
            print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
    except OSError as e:
            #print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
            print(f"Error is {e}")


if __name__ == "__main__":
    main()
