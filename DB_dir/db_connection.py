import psycopg2 as sql
import psycopg2.extras as sql_dict
import os


class DatabaseConnection:
    """
    CREATE SINGLETON CLASS
    GET DATABASE CONFIGS FROM db_configs.txt
    CREATE CONNECTION TO MSSQL
    """
    def __new__(cls,):
        """SINGLETON"""
        if not hasattr(cls, 'uniqueInstance'):
            cls.uniqueInstance = super().__new__(cls)
            return cls.uniqueInstance
        else:
            return cls.uniqueInstance

    def __init__(self,):
        self.__configs = dict()
        self.uniqueInstance.__connection = None

    def __get_database_configs(self):
        """GET CONFIGS FROM db_configs.txt"""
        x = os.getcwd()
        try:
            # with open(x+'/db_configs.txt') as configs:
            #     for line in configs:
            #         key, value = line.strip().split('=')
            #         self.__configs[key] = value
            # print("CONFIGS CREATED")
            self.__configs = dict(
                host='localhost',
                port=5432,
                user='pcassa',
                password=1234,
                database='testing')
        except Exception as e:
            print(f"ERROR {e}")

    def __create_database_connection(self):
        """CREATE CONNECTION TO DATABASE"""
        try:
            self.uniqueInstance.__connection = sql.connect(**self.__configs)
            print("CONNECTION CREATED")
        except Exception as e:
            print(f"ERROR {e}")

    @classmethod
    def __run(cls):
        """RUN ALL FUNCTIONS WITHOUT CREATING INSTANCE OUT OF CLASS"""
        cls()
        cls.uniqueInstance.__get_database_configs()
        cls.uniqueInstance.__create_database_connection()
        return cls.uniqueInstance.__connection

    @classmethod
    def close(cls):
        """CLOSE CONNECTION IF EXISTS"""
        if not cls.uniqueInstance.__connection:
            cls.uniqueInstance.__connection.close()
            print("CONNECTION CLOSED")
        else:
            print("THERE ARE NO CONNECTION")
            return

    @staticmethod
    def create_cursor():
        """Create a cursor and extract as dictionary"""
        return DatabaseConnection.__run().cursor(cursor_factory=sql_dict.RealDictCursor)

    @classmethod
    def commit(cls):
        """TRY TO SAVE CHANGES AFTER MANIPULATING"""
        if cls.uniqueInstance.__connection:
            cls.uniqueInstance.__connection.commit()
            print("CHANGES ARE COMMITED")
            return True
        else:
            print("CANNOT COMMIT")
            return

#DatabaseConnection.create_cursor()