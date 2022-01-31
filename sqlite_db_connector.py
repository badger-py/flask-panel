import sqlite3

class Table:
    def __init__(self, name:str, columns:list, validators={}):
        self.name = name
        self.columns = columns
        self.validators = validators

class Connector:
    def __init__(self, file_name:str, tables:list):
        self.file_name = file_name
        self.tables = tables
    
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
            self.close_connectoin()
            return self.cursor.fetchall()
        self.close_connectoin()

    def get_tables(self):
        # you don't need to setup or close connection
        # data = self.execute_sql("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        # data = [i[0] for i in data]
        return self.tables