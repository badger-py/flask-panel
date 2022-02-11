import sys
sys.path.append("..")
from models import models_list



class BadConnector(Exception):
    pass


class SQLTables:
    def __init__(self, connector) -> None:
        self.connector = connector
        connector = dir(self.connector)
        for i in ['open_connection', 'execute_sql', 'close_connectoin']:
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
        if not models_list:
            raise BadConnector('Models list can not be empty')

        for model in models_list:
            columns = list(dict(model.__dict__)['__annotations__'].keys())
            if len(columns) == 0:
                raise BadConnector('Table needs to have 1 or more columns')
            if columns[0] != 'id':
                raise BadConnector('All tables needs to have an id column')
        return models_list
    
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