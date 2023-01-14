import psycopg2 as sql
import psycopg2.extras as sql_dict
import configparser


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

        try:
            conf = configparser.ConfigParser()
            conf.read('DB_dir/DB_CONFIG.ini')
            db_host = conf.get('DATABASE', 'host')
            port = conf.getint('DATABASE', 'port')
            user = conf.get('DATABASE', 'user')
            password = conf.get('DATABASE', 'password')
            database = conf.get('DATABASE', 'database')
            self.__configs = dict(
                    host=db_host,
                    port=port,
                    user=user,
                    password=password,
                    database=database)
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
        try:
            cls.uniqueInstance.__connection.close()
            print("CONNECTION CLOSED")
        except Exception:
            return

    @staticmethod
    def create_cursor():
        """Create a cursor and extract as dictionary"""
        return DatabaseConnection.__run().cursor(cursor_factory=sql_dict.RealDictCursor)

    @classmethod
    def rollback(cls):
        cls.uniqueInstance.__connection.rollback()

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