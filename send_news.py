import mysql.connector
import json

from mysql.connector import errorcode


def send_news(notd, notw):
    with open("config.json") as file:
        json_file = json.load(file)
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
        cursor.execute("""UPDATE news SET newstxt = %s WHERE newsid = '1'""", (notd,))
        cursor.execute("""UPDATE news SET newstxt = %s WHERE newsid = '2'""", (notw,))
        cnx.commit()
        return "done"
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"ERROR: {e}")
            return f"Error: Access denied to database user. Maybe password not correct..."
        elif e.errno == 1146:
            print(f"ERROR: {e}")
            return 'Error: Unable to access News Table (Table doesn\'t exist!). Please contact the administrator.'
        elif e.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
            print(f"ERROR: {e}")
            return f"Error: Database user has no permission to access the database"
        else:
            print(f"ERROR: {e}")
            return "Error: Some error happened. Please contact the administrator."
