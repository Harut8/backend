from db_connection import DatabaseConnection as DBConnection


class DatabaseManipulator:
    """ CLASS FOR MANIPULATING WITH DATABASE TABLES """
    def __fetch_as_dict(self, fetch_data):
        return [dict(i) for i in fetch_data]


