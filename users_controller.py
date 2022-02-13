from functools import wraps
from typing import Optional
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """"
    Class user
    using 
        in flask-login
        as class with user to work comfortable with it
    has arguments
        id: int - user's id
        role: int - users's role (to controll acess to DB)
        username: str
        password: str - password cache
    """

    def __init__(self, id: int, role: int, username: str, password: str):
        self.id = id
        self.role = role
        self.username = username
        self.password = password

    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)

    def get_user(self) -> str:
        return str(self.id)


class UsersController:
    """
    Class to
        login user
        get user
        create user
    And create DB
    """

    def __init__(self) -> None:
        pass

    def _open_database(self) -> None:
        """Open connection to DB"""
        self.connection = sqlite3.connect('users.sqlite')
        self.cursor = self.connection.cursor()

    def _close_database(self) -> None:
        """Close connection to DB"""
        self.cursor.close()
        self.connection.close()

    def use_db(func):
        """Decorator to
            open and close connection
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self._open_database()
            res = func(self, *args, **kwargs)
            self._close_database()
            return res
        return wrapper

    @use_db
    def get_user(self, id: int) -> Optional[User]:
        """Get user by ID, None if not found"""
        self.cursor.execute('SELECT * FROM users WHERE id=?', (int(id),))
        data = self.cursor.fetchall()
        if not data:
            return data
        return User(*data)

    @use_db
    def login_user(self, login: str, password: str):
        self.cursor.execute('SELECT * FROM users WHERE username=?', (login,))
        user = self.cursor.fetchone()
        if not user:
            return None
        if not check_password_hash(user[-1], password):
            return None
        return User(*user)

    @use_db
    def create_user(self, username: str, password: str):
        self.cursor.execute('INSERT INTO users(username, password_hash) VALUES(?, ?)',
                            (username, generate_password_hash(password)))
        self.connection.commit()

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
            password_hash TEXT    NOT NULL
        )""")
        self.connection.commit()
