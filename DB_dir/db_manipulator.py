from .db_connection import DatabaseConnection as DBConnection
from MODELS_dir.acc_reg_model import AccountRegModel

class DatabaseManipulator:
    """ CLASS FOR MANIPULATING WITH DATABASE TABLES """
    @staticmethod
    def post_acc_into_temp_db(*, item: AccountRegModel):
        """ INSERT acc INFO INTO TEMP DATABASE"""
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""
                                    INSERT INTO temp_company(
                                    t_c_name,
                                    t_c_pass,
                                    t_c_contact_name,
                                    t_c_phone,
                                    t_c_email,
                                    t_c_verify_link,
                                    t_c_inn,
                                    t_c_kpp,
                                    t_c_k_schet,
                                    t_c_r_schet,
                                    t_c_bik,
                                    t_c_bank_name,
                                    t_c_address
                                    )
                                    VALUES (
                                    '{item.acc_org_name}',
                                    '{item.acc_pass}',
                                    '{item.acc_contact_name}',
                                    '{item.acc_phone}',
                                    '{item.acc_email}',
                                    'link',
                                    '{item.acc_inn}',
                                    '{item.acc_kpp}',
                                    '{item.acc_k_schet}',
                                    '{item.acc_r_schet}',
                                    '{item.acc_bik}',
                                    '{item.acc_bank_name}',
                                    '{item.acc_address}')
                                    """
                cursor.execute(SQL_query)
                DBConnection.commit()
                #DBConnection.close()
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_id_from_temp_db(*, name):
        """GET ID FROM temp_db FOR ADDING TO COMPANY DB"""
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""SELECT t_id FROM temp_company WHERE t_c_name = '{name}'"""
                cursor.execute(SQL_query)
                print('SUCCESSFULL GETTING NAME')
                return [dict(i) for i in cursor.fetchall()]
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def post_link_into_temp_company(*, link, name):
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""UPDATE temp_company SET t_c_verify_link = '{link}' WHERE t_c_name ='{name}'"""
                cursor.execute(SQL_query)
                DBConnection.commit()
                print('SUCCESS ADD LINK TO temp db')
                return True
        except Exception as e:
            print(e)
            return False


