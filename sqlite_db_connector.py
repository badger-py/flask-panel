import sqlite3

class Table:
    def __init__(self, name:str, columns:list):
        self.name = name
        self.columns = columns

class Connector:
    def __init__(self, file_name):
        self.file_name = file_name
    def open_connection(self):
        self.connection = sqlite3.connect(self.file_name)
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
        self.connection.close()
    def get_tables(self):
        # you don't need to setup or close connection
        # data = self.execute_sql("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        # data = [i[0] for i in data]
        tables = [
            Table(
                name = "positions",
                columns = ['id', 'name', 'price']
            ),
            Table(
                name = "photos",
                columns = ['id', 'url', 'positions_id']
            )
        ]
        return tables