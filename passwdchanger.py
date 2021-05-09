import mysql.connector
import json

from mysql.connector import errorcode


def passwdchanger(oldpassword, newpassword, newpasswordagain):
    global passwd
    with open("config.json") as file:
        json_file = json.load(file)
    if newpassword != newpasswordagain:
        return "notsame"
    try:
        cnx = mysql.connector.connect(
            host=json_file["host"],
            port=json_file["port"],
            user=json_file["user"],
            password=json_file["password"],
            database=json_file["database"],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM napp_login WHERE username = "admin"')
        result = cursor.fetchall()
        for (username, password) in result:
            if password != oldpassword:
                return "wrongpasswd"
            else:
                cursor.execute("""UPDATE napp_login SET password = %s WHERE username = 'admin'""", (newpassword,))
                cnx.commit()
                return True
        return passwd
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"ERROR: {e}")
            return f"Error: Database user has no Permission to access the database. Please contact the administrator."
        elif e.errno == 2003:
            print(f"ERROR: {e}")
            return "Error: Unable to Connect to the Database. Please contact the administrator."
        elif e.errno == 1146:
            print(f"ERROR: {e}")
            return 'Error: Unable to access News Table (Table doesn\'t exist!). Please contact the administrator.'
        elif e.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
            print(f"ERROR: {e}")
            return f"Error: User has no access to Database. Please contact the administrator."
        else:
            print(f"ERROR: {e}")
            return "Error: Some error happened. Please contact the administrator."