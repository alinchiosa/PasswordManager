import mysql.connector

def getUsers():
    users = []
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='password_manager',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM password_manager.users;")
    cursor.execute(query)

    for (user_id, first_name, last_name, username, password) in cursor:
        user = {'user_id':user_id, 'first_name':first_name, 'last_name':last_name, 'username':username, 'password':password}
        users.append(user)
    cursor.close()
    cnx.close()
    return users


def addUser(first_name, last_name, username, password):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='password_manager',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO password_manager.users "
               "(first_name, last_name, username, password) "
               "VALUES (%s, %s, %s, %s)")
    data_post = (first_name, last_name, username, password)
    cursor.execute(query, data_post)
    cnx.commit()
    cursor.close()
    cnx.close()

def addPassword(account_from, username, password, nonce, user_id):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='password_manager',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO password_manager.passwords "
             "(account_from, username, password, nonce,  user_id) "
             "VALUES (%s, %s, %s, %s, %s)")
    data_post = (account_from, username, password, nonce, user_id)
    cursor.execute(query, data_post)
    cnx.commit()
    cursor.close()
    cnx.close()

def getPasswords(user_id_fct):
    passwords = []
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='password_manager',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * from passwords")
    cursor.execute(query)
    for (password_id, account_from, username, password, nonce, user_id) in cursor:
        if user_id == user_id_fct:
            password_dict = {'password_id' : password_id, 'account_from': account_from, 'username': username, 'password': password, 'nonce': nonce, 'user_id': user_id}
            passwords.append(password_dict)
    cursor.close()
    cnx.close()
    return passwords

def editPassword(username, password, nonce, password_id):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='password_manager',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("UPDATE password_manager.passwords SET username=%s, password=%s, nonce=%s WHERE password_id=%s")
    data_edit = (username, password, nonce, password_id)
    cursor.execute(query, data_edit)
    cnx.commit()
    cursor.close()
    cnx.close()

def deletePassword(password_id):
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='password_manager',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("DELETE FROM password_manager.passwords WHERE password_id= %s ")
    cursor.execute(query, (password_id,))
    cnx.commit()
    cnx.close()
    cursor.close()





