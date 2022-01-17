import sqlite3 as sl
import os
from markupsafe import escape

class Auth():
    def __init__(self):
        if os.path.exists(".data/users.db"):
            self.db = sl.connect(".data/users.db")
        else:
            if not os.path.exists(".data/"):
                os.mkdir(".data/")
            self.db = sl.connect(".data/users.db")
            self.db.execute("""
                    CREATE TABLE USERS (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        password TEXT,
                        permissions INTEGER
                    );""")
            self.db.close()
    def is_valid(user,password):
        self.db = sl.connect(".data/users.db")
        cur = self.db.execute("SELECT * FROM USERS WHERE (user == '%s',password == '%s')" % (user,password))
        cur.close()
        return cur.arraysize > 0

    def has_user(user):
        f = open(".data/users.props")
        for line in f:
            line = line.split("=")
            if line[0] == user:
                f.close()
                return True
        if not f.closed: 
            f.close()
        return False

    def add_user(user, password):
        db.execute("INSERT INTO USERS (name, password, permissions) values(?, ?, ?)",[(user,password,0)])
