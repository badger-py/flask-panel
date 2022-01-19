import sqlite3


class UsersController:
    def __init__(self):
        pass
    

    def _get_database(self):
        self.connection = sqlite3.connect('users.sqlite')
        self.cursor = self.connection.cursor()
    
    def _close_database(self):
        self.cursor.close()
        self.connection.close()
    # @staticmethod
    # def use_db(func):
    #     def wrapper(self):
    #         self._get_database()
    #         func()
    #         self._close_database()

    #     return wrapper

    # @use_db
    def get_user(self, id):
        self._get_database()
        self.cursor.execute('SELECT * FROM users WHERE id=?',(int(id),))
        return User(*self.cursor.fetchone())

    # @use_db
    def login_user(self, login, password):
        self._get_database()
        self.cursor.execute('SELECT * FROM users WHERE username=? AND password_hash=?', (login, password))
        user = self.cursor.fetchone()
        if not user:
            return None
        self._close_database()
        return User(*user)
    
    # @use_db
    def create_user(self, role, username, password):
        pass

    
    # @use_db
    def _create_databse(self):
        self._get_database()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY
                                UNIQUE
                                NOT NULL,
            role          INTEGER NOT NULL
                                DEFAULT (1),
            username      STRING  UNIQUE
                                NOT NULL,
            password_hash TEXT    NOT NULL
        )""")
        self.connection.commit()
        self._close_database()

class User:
    def __init__(self, id, role, username, password):
        self.id = id
        self.role = role
        self.username = username
        self.password = password
    
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)
    def get_user(self):
        return str(self.id)