from .db_connection import DatabaseConnection as DBConnection


class DatabaseManipulatorTARIFES:
    """Manipulator FOR MANIPULATION TABLES ABOUT TARIFES."""

    @staticmethod
    def get_tarifes_for_view():
        """Returns a dict of tarifes information"""
        with DBConnection.create_cursor() as cursor:
            try:
                cursor.execute("SELECT * from get_tarifes_for_view()")
                temp_ = cursor.fetchall()
                return True, temp_
            except Exception as e:
                print(e)
                return False,
