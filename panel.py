import sqlite3


class UsersController:
    def __init__(self):
        pass
    
    @use_db
    def get_user(self, id):
        self.cursor.execute('SELECT * FROM users WHERE id=?',int(id))
        return User(*self.cursor.fetcone())
    
    def create_user(self, role, username, password):
        pass

    def _get_database(self):
        self.connection = sqlite3.connect('users.sqlite')
        self.cursor = self.connection.cursor()
    
    def _close_database(self):
        self.cursor.close()
        self.connection.close()
    
    def use_db(self, func):
        def wrapper():
            self._get_database()
            func()
            self._close_database()

        return wrapper
    
    @use_db
    def _create_databse(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY
                                UNIQUE
                                NOT NULL,
            role          INTEGER NOT NULL
                                DEFAULT (1),
            username      STRING  UNIQUE
                                NOT NULL,
            password_cash TEXT    NOT NULL
        )""")
        self.connection.commit()

class User:
    def __init__(self, id, role, username, password):
        self.id = id
        self.role = role
        self.username = username
        self.password = password