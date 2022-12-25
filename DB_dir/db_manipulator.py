from .db_connection import DatabaseConnection as DBConnection
from MODELS_dir.acc_model import AccountRegModel
import hashlib


class DatabaseManipulator:
    """ CLASS FOR MANIPULATING WITH DATABASE TABLES """
    @staticmethod
    def post_acc_into_temp_db(*, item: AccountRegModel):
        """ INSERT acc INFO INTO TEMP DATABASE"""
        try:
            hash_str = hashlib.sha256(item.acc_pass.encode())
            hash_pass = hash_str.hexdigest()
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
                                    %(org_name)s,
                                    '{hash_pass}',
                                    %(contact_name)s,
                                    %(acc_phone)s,
                                    %(acc_email)s,
                                    'link',
                                    %(acc_inn)s,
                                    %(acc_kpp)s,
                                    %(acc_k_schet)s,
                                    %(acc_r_schet)s,
                                    %(acc_bik)s,
                                    %(acc_bank_name)s,
                                    %(acc_address)s)
                                    """
                cursor.execute(SQL_query, {
                    'org_name': item.acc_org_name,
                    'contact_name': item.acc_contact_name,
                    'acc_phone': item.acc_phone,
                    'acc_email': item.acc_email,
                    'acc_inn': item.acc_inn,
                    'acc_kpp': item.acc_kpp,
                    'acc_k_schet': item.acc_k_schet,
                    'acc_r_schet': item.acc_r_schet,
                    'acc_bik': item.acc_bik,
                    'acc_bank_name': item.acc_bank_name,
                    'acc_address': item.acc_address,
                })
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
                return cursor.fetchall()[0]
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def post_link_into_temp_company(*, link, name):
        """ AFTER ADDING User to temp_company
            generate link and update column"""
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

    @staticmethod
    def verify_link(*, temp_id: int):
        """ CALL STORED FUNCTION for verifying
            DELETE FROM temp_company ADD TO company"""
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""SELECT del_tmp_add_company({temp_id})"""
                cursor.execute(SQL_query)
                DBConnection.commit()
                print('SUCCESS TO VERIFY LINK')
                return True
        except Exception as e:
            print(e)
            return False


    @staticmethod
    def update_acc_pass(*, acc_email: str, acc_pass: str):
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""UPDATE company SET c_pass = %(pass)s WHERE c_email = %(email)s"""
                hash_str = hashlib.sha256(acc_pass.encode())
                hash_pass = hash_str.hexdigest()
                cursor.execute(SQL_query, {'email': acc_email, 'pass': hash_pass})
                DBConnection.commit()
                print('SUCCESSFULL UPDATING PASS')
                return True
        except Exception as e:
            print(e)
            return False


