import mysql.connector
import json
import time

from os import urandom
from mysql.connector import errorcode


def inst():
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
        unix = round(time.time())
        cursor.execute(f"CREATE TABLE napp_login (username varchar(255), password varchar(255))")
        cursor.execute(f'INSERT INTO napp_login (username, password) VALUES ("admin", "Sample1234")')
        cursor.execute(f"CREATE TABLE napp_news (newsid varchar(255), newstxt TEXT(65535))")
        cursor.execute(f'INSERT INTO napp_news (newsid, newstxt) VALUES ("1", "This is the news of the Day!")')
        cursor.execute(f'INSERT INTO napp_news (newsid, newstxt) VALUES ("2", "This is the news of the Week!")')
        cursor.execute(f"CREATE TABLE napp_config (configkey varchar(255), configvalue varchar(255))")
        cursor.execute(f'INSERT INTO napp_config (configkey, configvalue) VALUES ("code", "333666")')
        cursor.execute(f'INSERT INTO napp_config (configkey, configvalue) VALUES ("unixtime", "{unix}")')
        cnx.commit()
        cnx.close()
        key = urandom(64)
        return "Installing Data Completed! NOTE: DELETE THE FILE install.py OR SOMEONE CAN RERUN THE INSTALLATION <br> <br> NOTE: COPY THE BIG TEXT UNDER THIS TEXT AND REPLACE IT WITH THE 'app.secret_key' FIELD IN THE FILE " \
               f"""app.py: <br> <br> <h3>app.secret_key = {key}</h3> <br> <br> and restart it ;)"""
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"ERROR: {e}")
            return f"Error: Access denied to User {json_file['user']}. Maybe Password not correct..."
        elif e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print(f"ERROR: {e}")
            return 'Error: One table already exist! Can\'t proceed the install. Make sure, that the tables "Login" and ' \
                   '"News" doesn\'t exist! '
        elif e.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
            print(f"ERROR: {e}")
            return f"Error: User {json_file['user']} has no Permission to access the Database {json_file['database']}"
        else:
            print(f"ERROR: {e}")
            return "Error: Some error happened. Check the Logs."
