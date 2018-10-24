import DatabaseConnect
import nacl.secret
import nacl.utils
import os
import binascii
import codecs
import nacl.encoding
import nacl.hash

def logIn():
    log_in_decision = 1
    flag = True
    while flag:
        username = input("Username: ")
        users = DatabaseConnect.getUsers()
        for user in users:
            if username == user['username']:
                password = input("Password: ")
                password_in_bytes = password.encode()
                password_hashed = nacl.hash.sha512(password_in_bytes, encoder=nacl.encoding.HexEncoder)
                if password_hashed == user['password'].encode():
                    user_id = user['user_id']
                    log_in_decision = True
                    print("Welcome")
                    print()
                    flag = False
                    break
                else:
                    print("Incorrect password!")
                    print()
                    break
                break
            else:
                log_in_decision = 2
        if log_in_decision == 2:
            print("You are not an user")
            print()
    return user_id

def passMenu():
    input_ans = input("If you want to see your passwords press 1 \n"
                      "If you want to add a password press 2 \n"
                      "If you want to edit a password press 3 \n"
                      "If you want to delete a password press 4 \n"
                      "If you want to exit press anything else \n"  
                      "                  ")
    print()
    if input_ans == "1":
        passwords = DatabaseConnect.getPasswords(user_id)
        users = DatabaseConnect.getUsers()
        for user in users:
            if(user['user_id'] == user_id):
                username = user['username']
        for pas in passwords:
            print("Acoount from: ", pas['account_from'])
            password_to_bytearray = codecs.decode(pas['password'], "hex")
            f = open(username + ".txt", 'rb')
            key = f.read()
            f.close()
            box = nacl.secret.SecretBox(key)
            plain_password = box.decrypt(password_to_bytearray)
            print("Username: ", pas['username'])
            print("Password: ", plain_password.decode())
            print()
        if(len(passwords) == 0):
            print("You don't have any passwords saved!")
            print()
        inp = input("If you want to go back to the Pasword menu press 1 \n"
                    "If you want to exit the app press 2 \n"
                    "                ")
        if inp == '1':
            passMenu()
        elif inp == '2':
            print("             Good bye!")
    elif input_ans == '2':
        account_from = input("The account that the password is used for: ")
        username_pass = input("Username: ")
        password_pass = input("Password: ")
        encoded_password = password_pass.encode()
        nonce = int(os.urandom(24).hex(), 16).to_bytes(24, byteorder="big")
        nonce_db = binascii.hexlify(bytearray(nonce)).decode()
        users = DatabaseConnect.getUsers()
        for user in users:
            if(user['user_id'] == user_id):
                username = user['username']
        f = open(username + ".txt", 'rb')
        key = f.read()
        f.close()
        box = nacl.secret.SecretBox(key)
        encr_password = box.encrypt(encoded_password, nonce)
        password_hex = binascii.hexlify(bytearray(encr_password))
        DatabaseConnect.addPassword(account_from, username_pass, password_hex, nonce_db, user_id)
        print()
        passMenu()
    elif input_ans == '3':
        passwords = DatabaseConnect.getPasswords(user_id)
        for pas in passwords:
            print("Password id: ", pas['password_id'])
            print("Acoount from: ", pas['account_from'])
            print()
        input_edit = input("Type the Password id of the password that you want to edit: ")
        flag = False
        for pas in passwords:
            if int(input_edit) == pas['password_id'] and user_id == pas['user_id']:
                flag = True
        if(flag):
            username_pass = input("Type the new username: ")
            password_pass = input("Type the new password: ")
            encoded_password = password_pass.encode()
            nonce = int(os.urandom(24).hex(), 16).to_bytes(24, byteorder="big")
            nonce_db = binascii.hexlify(bytearray(nonce)).decode()
            users = DatabaseConnect.getUsers()
            for user in users:
                if (user['user_id'] == user_id):
                    username = user['username']
            f = open(username + ".txt", 'rb')
            key = f.read()
            f.close()
            box = nacl.secret.SecretBox(key)
            encr_password = box.encrypt(encoded_password, nonce)
            password_hex = binascii.hexlify(bytearray(encr_password))
            DatabaseConnect.editPassword(username_pass, password_hex, nonce_db, input_edit)
            print("The password was edited!")
            print()
            passMenu()
        else:
            print()
            print("This password id doesn't belong to you!")
            print()
            passMenu()
    elif input_ans == '4':
        passwords = DatabaseConnect.getPasswords(user_id)
        for pas in passwords:
            print("Password id: ", pas['password_id'])
            print("Acoount from: ", pas['account_from'])
            print()
        input_delete = input("Type the Password id of the password that you want to delete: ")
        flag = False
        for pas in passwords:
            if int(input_delete) == pas['password_id'] and user_id == pas['user_id']:
                flag = True
        if flag:
            DatabaseConnect.deletePassword(input_delete)
            print("The password was deleted! ")
            print()
            passMenu()
        else:
            print()
            print("This password id doesn't belong to you!")
            print()
            passMenu()
    else:
        print("Good Bye!!")

log_in_answer = input("For Log in press 1, for Sign up press 2: ")
if log_in_answer == '1':
    user_id = logIn()
    print(user_id)
else:
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    flag = True
    while flag:
        username = input("Enter your username: ")
        users = DatabaseConnect.getUsers()
        if(len(users) > 0):
            for user in users:
                if username == user['username']:
                    print("This username already exists.! Choose a new one!")
                    break
                else:
                    flag = False
        else: flag = False
    password = input("Enter your password: ")
    password_in_bytes = password.encode()
    password_hashed = nacl.hash.sha512(password_in_bytes, encoder=nacl.encoding.HexEncoder)
    DatabaseConnect.addUser(first_name, last_name, username, password_hashed)
    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    f = open(username + '.txt', 'wb')
    f.write(key)
    f.close()
    print("You have been registered!")
    print()
    user_id = logIn()
passMenu()



