import sqlite3
import sqlalchemy
import pandas as pd
from decouple import config


class SQLLite:
    

    NAME = config('SQLITE_DATABASE_NAME', default='db.sqlite3')


    def __init__(self):
        self.table = 'news'
        self.engine = sqlalchemy.create_engine(f'sqlite:///{self.NAME}')
        self.connection = sqlite3.connect(self.NAME)
        self.__create__()

    def __create__(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(512),
            url VARCHAR(256),
            timestamp DATETIME)
        """
        cursor = self.connection.cursor()
        cursor.execute(query)

    def to_db(self, dataframe):
        dataframe.to_sql(self.table, self.engine, index=False, if_exists='append')
        self.connection.close()

    def get_table(self):
        return pd.read_sql(self.table, self.engine, 
            columns=['title', 'url', 'timestamp'], parse_dates=['timestamp'])
