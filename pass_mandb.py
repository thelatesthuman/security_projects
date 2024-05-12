#! python3
# pass_man.py - Creates and stores username, encrypted password, and key in pass_man postgres db, then
# authenticates user login with account in shadow file
import pyinputplus
import sys
import hashlib
import os
import psycopg2

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
        # Ask user for username and confirm username is not already in use by opening pass_man db and checking usernames
        username = pyinputplus.inputStr("Please enter your username: ",timeout=60)
        conn = psycopg2.connect(database = 'pass_man',
                user = "",
                host = 'localhost',
                password = '',
                port = '5432'
                )
        cur = conn.cursor()
        cur.execute(f"SELECT username FROM accounts WHERE username='{username}';")
        usernames = cur.fetchall()
        conn.commit()
        conn.close()
        
        if usernames == []:
            # call password_input function and encrypt
            salt = os.urandom(32)
            encPassword = hashlib.pbkdf2_hmac(
                    'sha512', 
                    PassMan.create_password_input().encode(), 
                    salt, 
                    100000)
            
            # Open pass_man db then add username, password, and salt
            conn = psycopg2.connect(database = 'pass_man',
                    user = "",
                    host = 'localhost',
                    password = '',
                    port = '5432'
                    )
            cur = conn.cursor()
            cur.execute(f"INSERT INTO accounts VALUES ('{username}','{encPassword.hex()}','{salt.hex()}')");
            conn.commit()
            cur.close()
            conn.close()
            print("Account created!")
        else:
            PassMan.create_password_input()
            print("Username or password not valid!")


    def authenticate():
        # Ask user for username and password
        username = pyinputplus.inputStr("Please enter your username: ",timeout=60)
        password = pyinputplus.inputPassword(prompt="Enter your password: ")
        try:
            # Open pass_man db and extract password and salt from 
            # accounts table
            conn = psycopg2.connect(database = 'pass_man',
                    user = "",
                    host = 'localhost',
                    password = '',
                    port = '5432'
                    )
            cur = conn.cursor() 
            cur.execute(f"SELECT password,salt FROM accounts WHERE username='{username}';")
            conn.commit()
            pass_salt = cur.fetchall()
            cur.close()
            conn.close()
            
            # Encrypt authentication password with salt and compare 
            # with original password
            originEncPass = bytes.fromhex(pass_salt[0][0])
            salt = bytes.fromhex(pass_salt[0][1])
            authEncPass = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)
            if authEncPass == originEncPass: 
                return "Login successful!"
            else:
                return "Login failed!"
        except:
            return "Login failed!"

# Call functions based on user input
def main(): 
    try:
        if sys.argv[1] == 'create_account':
            PassMan.create_account()
        elif sys.argv[1] == 'authenticate':
            print(PassMan.authenticate())
        elif sys.argv[1] == 'help':    
            print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
        else:
            print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help")
    except OSError as e:
        print("Options are 'create_account' for New account, 'authenticate' for Login, and 'help' for Help") 
        #print(f"Error is {e}")


if __name__ == "__main__":
    main()
