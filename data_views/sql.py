


class BadConnector(Exception):
    pass


class SQLTables:
    def __init__(self, connector) -> None:
        self.connector = connector
        connector = dir(self.connector)
        for i in ['open_connection', 'execute_sql', 'close_connectoin', 'get_tables']:
            if i not in connector:
                raise BadConnector(f'Connector need to has function {i}')

    @staticmethod
    def check_query(query:str) -> bool:
        # return Flase if sql injection in query
        query = query.lower()
        for operation in ['select', 'update', 'insert', 'delete', 'drop', 'or']:
            if operation in query:
                return False
        return True
    
    def get_tables(self) -> list:
        data = self.connector.get_tables()

        if not data:
            raise BadConnector('Tables list can not be empty')
        for table in data:
            if len(table.columns) == 0:
                raise BadConnector('Table needs to have 1 or more columns')
            if table.columns[0] != 'id':
                raise BadConnector('All tables needs to have an id column')
        return data
    
    def get_data_from_table(self, table_name: str, limit: int=None, offset: int=0) -> list:
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