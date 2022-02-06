import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class BadConnector(Exception):
    pass


class UsersController:
    def __init__(self):
        pass
    

    def _get_database(self):
        self.connection = sqlite3.connect('users.sqlite')
        self.cursor = self.connection.cursor()
    
    def _close_database(self):
        self.connection.close()
    # @staticmethod
    # def use_db(func, **args):
    #     def wrapper(self):#self):
    #         print(self)
    #         self._get_database()
    #         func(self, *args)
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
        self.cursor.execute('SELECT * FROM users WHERE username=?', (login,))
        user = self.cursor.fetchone()
        if not user:
            self._close_database()
            return None
        if not check_password_hash(user[-1], password):
            self._close_database()
            return None

        self._close_database()
        return User(*user)
    
    # @use_db
    def create_user(self, username, password):
        self._get_database()
        self.cursor.execute('INSERT INTO users(username, password_hash) VALUES(?, ?)', (username, generate_password_hash(password)))
        self.connection.commit()
        self._close_database()
    
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

class SQLTables:
    def __init__(self, connector):
        self.connector = connector
        connector = dir(self.connector)
        for i in ['open_connection', 'execute_sql', 'close_connectoin', 'get_tables']:
            if i not in connector:
                raise BadConnector(f'Connector need to has function {i}')

    @staticmethod
    def check_query(query:str):
        # return Flase if sql injection in query
        query = query.lower()
        for operation in ['select', 'update', 'insert', 'delete', 'drop', 'or']:
            if operation in query:
                return False
        return True
    
    def get_tables(self):
        data = self.connector.get_tables()

        if not data:
            raise BadConnector('Tables list can not be empty')
        for table in data:
            if len(table.columns) == 0:
                raise BadConnector('Table needs to have 1 or more columns')
            if table.columns[0] != 'id':
                raise BadConnector('All tables needs to have an id column')
        return data
    
    def get_data_from_table(self, table_name, limit=None, offset=0):
        self.connector.open_connection()
        if not SQLTables.check_query(table_name):
            return []
        if limit != None:
            data = self.connector.execute_sql(f'SELECT * FROM {table_name} LIMIT ? OFFSET ?', (limit, offset))
        else:
            data = self.connector.execute_sql(f'SELECT * FROM {table_name} OFFSET {offset}')
        self.connector.close_connectoin()
        return data


if __name__ == '__main__':
    from sqlite_db_connector import Connector
    obj = SQLTables(Connector('/home/yan/Desktop/test_database.db'))
    print(obj.get_data_from_table('posotions'))