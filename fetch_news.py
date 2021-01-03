import mysql.connector
import json

from mysql.connector import errorcode


def get_news():
    with open("config.json") as file:
        json_file = json.load(file)
    try:
        cnx = mysql.connector.connect(
            host=json_file["host"],
            port=json_file["port"],
            user=json_file["user"],
            password=json_file["password"],
            database=json_file["database"]
        )
        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM news WHERE newsid = "1"')
        news1 = cursor.fetchall()
        cursor.execute('SELECT * FROM news WHERE newsid = "2"')
        news2 = cursor.fetchall()
        return news1, news2
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
