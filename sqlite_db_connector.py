import sqlite3


class Connector:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def open_connection(self):
        self.connection = sqlite3.connect(self.file_name)
        self.cursor = self.connection.cursor()

    def close_connectoin(self):
        self.connection.close()

    def execute_sql(self, query, params=None, commit=False):
        self.open_connection()
        if not params:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        if commit:
            self.connection.commit()
        else:
            data = self.cursor.fetchall()
            self.close_connectoin()
            return data
        self.close_connectoin()
