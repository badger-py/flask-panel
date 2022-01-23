import sqlite3


class Connector:
    def __init__(self):
        pass
    def open_connection(self):
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()
    def execute_sql(self, query, params=None, commit=False):
        if not params:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        if commit:
            self.connection.commit()
        else:
            return self.cursor.fetchall()
    def close_connectoin(self):
        self.cursor.close()
        self.connection.close()
    def get_tables(self):
        # you don't need to setup or close connection
        return self.execute_sql("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
