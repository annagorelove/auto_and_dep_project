from psycopg2 import connect
import os 
import configparser

dirname = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))


class Database:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port 
        self.database = database
        self.user = user 
        self.password = password

        self.connection = connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True
    
    def post(self, query, args=()):
        try:
            self.cursor.execute(query, args)
        except Exception as err:
            print(repr(err))

        