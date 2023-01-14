from .db_connection import DatabaseConnection as DBConnection


class DatabaseManipulatorTARIFES:
    """Manipulator FOR MANIPULATION TABLES ABOUT TARIFES."""

    @staticmethod
    def get_tarifes_for_view():
        """Returns a dict of tarifes information"""
        with DBConnection.create_cursor() as cursor:
            try:
                cursor.execute("SELECT * from get_tarifes_for_view() limit 4")
                temp_ = cursor.fetchall()
                return temp_
            except Exception as e:
                print(e)
                return None

    @staticmethod
    def post_tarife_to_client(*, company_id: int, tarif_id_or_info):
        """ ADD TARIF TO CLIENT TABLE"""
        with DBConnection.create_cursor() as cursor:
            try:
                if isinstance(tarif_id_or_info, int):
                    cursor.execute("INSERT INTO client_tarif (c_t_id, c_t_tarif_id)"
                                   "VALUES ( %(company_id)s, %(tarif_id)s)",
                                   {'company_id': company_id,
                                    'tarif_id': tarif_id_or_info
                                    })
                    DBConnection.commit()
                    return True
                else:
                    cursor.execute("SELECT add_personal_tarifes("
                                   "%(cassa_count)s ,"
                                   "%(manager_count)s ,"
                                   "%(sklad_count)s ,"
                                   "%(company_id)s"
                                   ")",
                                   {'cassa_count': tarif_id_or_info.cass_stantion,
                                    'manager_count': tarif_id_or_info.mobile_manager,
                                    'sklad_count': tarif_id_or_info.web_manager,
                                    'company_id': company_id})
                    DBConnection.commit()
                    return True
            except Exception as e:
                print(e)
                return None
