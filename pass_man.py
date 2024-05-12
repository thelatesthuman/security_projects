#! python3
# pass_man.py - Creates and stores username, encrypted password, and key in shadow file, then
# authenticates user login with account in shadow file
import pyinputplus
import sys
import hashlib
import os


class PassMan:
    def create_password_input():
        # Ask user to create password
        for attempt in range(3):
            password = pyinputplus.inputPassword(prompt='Please create a new password: ') 
            password_confirm = pyinputplus.inputPassword(prompt='Please confirm your password: ')
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
        username = pyinputplus.inputStr("Please enter your username: ",timeout=60)
        try:
            with open('shadow', 'r') as shadow_file:
                f = shadow_file.read()
        except FileNotFoundError:
            with open('shadow', 'w') as shadow_file:
                f = '' 
        shadow_list = f.split('\n')
        usernames = [account.split(':')[0] for account in shadow_list]

        if username not in usernames:
            # call password_input function and encrypt
            salt = os.urandom(32)
            encPassword = hashlib.pbkdf2_hmac(
                    'sha512', 
                    PassMan.create_password_input().encode(), 
                    salt, 
                    100000)

            # Write username, password, and key to shadow file
            with open('shadow', 'a') as shadow_file:
                shadow_file.write(username + ':' + encPassword.hex() + ':' + salt.hex() + '\n')
            print("Account created!")
        else:
            PassMan.create_password_input()    
            print("Username or Password invalid")


    def authenticate():
        # Ask user for username and password
        username = pyinputplus.inputStr("Please enter your username: ",timeout=60)
        password = pyinputplus.inputPassword(prompt="Enter your password: ")
        
        # Open shadow file to compare real password hash with authenticating password hash
        try:
            with open('shadow', 'r') as shadow_file:
                for account in shadow_file:
                    if account.split(':')[0] == username:
                        originEncPass = bytes.fromhex(account.split(':')[1])
                        salt = bytes.fromhex(account.split(':')[2])
                        authEncPass = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)
                        if authEncPass == originEncPass: 
                            return "Login successful!"
                        else:
                            return "Login failed!"
                    else:
                        return "Login failed!"
        except:
            return "Login failed!"

# Call functions based on user input
def main():    
    try:
        if sys.argv[1] == 'create_account':
            try:
                PassMan.create_account()
            except OSError as e:
                #print("Username or password not valid.")
                print(f"Error is {e}")
        elif sys.argv[1] == 'authenticate':
            print(PassMan.authenticate())
        elif sys.argv[1] == 'help':    
            print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
        else:
            print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
    except OSError as e:
            print(f"Error is {e}")


if __name__ == "__main__":
    main()
