from .db_connection import DatabaseConnection as DBConnection
from MODELS_dir.acc_model import AccountRegModel
import hashlib


class DatabaseManipulatorACCOUNT:
    """ CLASS FOR MANIPULATING WITH DATABASE ACCOUNT TABLES """

    @staticmethod
    def post_acc_into_temp_db(*, item: AccountRegModel):
        """ INSERT acc INFO INTO TEMP DATABASE"""
        try:
            hash_str = hashlib.sha256(item.acc_pass.encode())
            hash_pass = hash_str.hexdigest()
            with DBConnection.create_cursor() as cursor:
                CHECK_ORG_NAME_IN_TEMP = """
                 SELECT c_name, c_email, c_phone FROM company
                 WHERE c_name = %(org_name)s or 
                 c_email = %(acc_email)s 
                 or 
                 c_phone = %(acc_phone)s"""
                cursor.execute(CHECK_ORG_NAME_IN_TEMP,
                               {"org_name": item.acc_org_name,
                                "acc_email": item.acc_email,
                                "acc_phone": item.acc_phone
                                })
                check_are_there_company_with_these_params = cursor.fetchone()
                if check_are_there_company_with_these_params:
                    return 'ka'
                cursor.execute("DELETE  FROM temp_company WHERE t_c_name = %(org_name)s"
                               " or"
                               " t_c_email = %(acc_email)s"
                               " or t_c_phone = %(acc_phone)s",
                               {"org_name": item.acc_org_name,
                                "acc_email": item.acc_email,
                                "acc_phone": item.acc_phone
                                })
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
                # DBConnection.close()
                return True
        except Exception as e:
            print(e)
            DBConnection.rollback()
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
            DBConnection.rollback()
            return False

    @staticmethod
    async def post_link_into_temp_company(*, link, name):
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
            DBConnection.rollback()
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
                data = cursor.fetchone()
                if data is not None:
                    return data
                return
        except Exception as e:
            print(e)
            DBConnection.rollback()
            return

    @staticmethod
    def update_verify_status(*, acc_unique_id: int):
        """ GET c_unique_code and password and send to user email"""
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""
                UPDATE company SET c_verify_status = true WHERE c_unique_id = %(acc_unique_id)s
                """
                cursor.execute(SQL_query, {'acc_unique_id': acc_unique_id})
                DBConnection.commit()
                return True
        except Exception as e:
            print(e)
            DBConnection.rollback()
            return False

    @staticmethod
    def update_acc_pass(*, acc_email: str, acc_pass: str):
        """ UPDATE PASSWORD OF ACCOUNT AN THIS EMAIL"""
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""UPDATE company SET c_pass = %(pass)s WHERE c_email = %(email)s"""
                hash_str = hashlib.sha256(acc_pass.encode())
                hash_pass = hash_str.hexdigest()
                cursor.execute(SQL_query, {'email': acc_email, 'pass': hash_pass})
                DBConnection.commit()
                print('SUCCESSFULLY UPDATING PASS')
                return True
        except Exception as e:
            print(e)
            DBConnection.rollback()
            return False

    @staticmethod
    def update_acc_token(*, access_token: str, acc_id: str):
        """ UPDATE TOKEN OF ACCOUNT"""
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = f"""UPDATE company SET c_token = %(access_token)s WHERE c_id = %(c_id)s"""
                cursor.execute(SQL_query,
                               {'access_token': access_token,
                                'c_id': acc_id})
                DBConnection.commit()
                print('SUCCESSFULLY UPDATING TOKEN')
                return True
        except Exception as e:
            print(e)
            DBConnection.rollback()
            return False

    @staticmethod
    def delete_data_from_temp_if_failed(*, acc_email: str):
        """ DELETE ROW FROM temp_company IF EMAIL FAILED """
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = """ DELETE FROM temp_company WHERE t_c_email = %(acc_email)s """
                cursor.execute(SQL_query, {'acc_email': acc_email})
                DBConnection.commit()
                print('SUCCESSFULLY DELETED FROM TEMP')
                return True
        except Exception as e:
            print(e)
            DBConnection.rollback()
            return False

    @staticmethod
    def signin_acc(*, acc_email: str, acc_pass: str):
        """ 3 WAYS TO LOGIN
            company_email and company_password
            company_email and diller_password
            diller_email and diller_password"""
        try:
            with DBConnection.create_cursor() as cursor:
                acc_pass = hashlib.sha256(acc_pass.encode()).hexdigest()
                SQL_query = """SELECT c_id, c_name FROM company
                                WHERE c_email = %(acc_email)s AND c_pass = %(acc_pass)s"""
                cursor.execute(SQL_query, {'acc_email': acc_email, 'acc_pass': acc_pass})
                data = cursor.fetchone()
                print(acc_pass, acc_email)
                if data is None:
                    SQL_query = """SELECT c_name, d_name FROM company c
                     LEFT JOIN diller d ON c.c_diller_id = d.d_id
                     WHERE c_email = %(acc_email)s AND %(acc_pass)s IN (SELECT d_pass FROM diller)"""
                    cursor.execute(SQL_query, {'acc_email': acc_email, 'acc_pass': acc_pass})
                    data = cursor.fetchone()
                    if data is not None:
                        return data
                    elif data is None:
                        SQL_query = """SELECT d_id, d_name FROM diller
                                       WHERE d_email = %(acc_email)s AND d_pass = %(acc_pass)s"""
                        cursor.execute(SQL_query, {'acc_email': acc_email, 'acc_pass': acc_pass})
                        data = cursor.fetchone()
                        if data is not None:
                            return data

                    return
                return data
        except Exception as e:
            print(e)
            DBConnection.rollback()
            return

    @staticmethod
    def signin_acc_info(*, acc_token: str, lan_num: int):
        """ 3 WAYS TO GET INFO BY TOKEN
            company_email and company_password
            company_email and diller_password
            diller_email and diller_password"""
        try:
            with DBConnection.create_cursor() as cursor:
                SQL_query = """SELECT c_id,
                                      c_name,
                                      c_contact_name,
                                      c_phone,
                                      c_email
                               FROM company
                               WHERE c_token = %(acc_token)s"""
                cursor.execute(SQL_query, {'acc_token': acc_token})
                data = cursor.fetchone()
                cursor.execute("""
                SELECT 
                      distinct t_id,
                      t_name[%(lan_num)s],
                      end_license::date,
                      true as order_state
                FROM tarif 
                join client_tarif ct on ct.c_t_id = %(client_id)s and ct.c_t_tarif_id  = t_id
                where t_id in (select tarif_id_fk from saved_order_and_tarif soat where company_id = %(client_id)s)
                union all
                SELECT 
                      distinct t_id,
                      t_name[%(lan_num)s],
                      null::date,
                      false as order_state
                FROM tarif 
                where t_id in (select tarif_id_fk from saved_order_and_tarif soat where company_id = %(client_id)s
                except select c_t_tarif_id  from client_tarif ct2  where c_t_id  = %(client_id)s)
                               """,
                               {"client_id": data['c_id'],
                                "lan_num": lan_num})

                data2 = cursor.fetchall()
                fk_data = []
                for i in data2:
                    cursor.execute(""" 
                                    SELECT * from get_links_state((select order_id from saved_order_and_tarif where tarif_id_fk=%(t_id)s));
                                    """, {'t_id': i['t_id']})
                    fk_data += [i | {"links": cursor.fetchall()}]
                    #print(i, "----------------")
                #print(fk_data)
                data = data | {"tarif_list": fk_data}
                if data is None:
                    SQL_query = """SELECT c_name, d_name FROM company c
                         LEFT JOIN diller d ON c.c_diller_id = d.d_id
                         WHERE c_token = %(acc_token)s """
                    cursor.execute(SQL_query, {'acc_token': acc_token})
                    data = cursor.fetchone()
                    if data is not None:
                        return data
                    elif data is None:
                        #change to token
                        SQL_query = """SELECT d_name, d_contact_name, d_phone, d_email FROM diller
                                           WHERE d_email = %(acc_email)s AND d_pass = %(acc_pass)s"""
                        cursor.execute(SQL_query, {'acc_email': 'ddd', 'acc_pass': 'wjw'})
                        data = cursor.fetchone()
                        if data is not None:
                            return data

                    return
                return data
        except Exception as e:
            print(e)
            DBConnection.rollback()
            return

    # @staticmethod
    # def add_access_token_to_account(*, access_token: str, account_id: str):
    #     try:
    #         with DBConnection.create_cursor() as cursor:
    #             cursor.execute(
    #                 """ UPDATE company SET c_token = %(access_token)s WHERE c_id = %(account_id)s""",
    #                 {'access_token': access_token,
    #                  'account_id': account_id
    #                  })
    #             DBConnection.commit()
    #             return True
    #     except Exception as e:
    #         print(e)
    #         DBConnection.rollback()
    #         return None

    @staticmethod
    def decorator_for_cursor_create():
        try:
            with DBConnection.create_cursor() as cursor:
                pass
        except Exception as e:
            print(e)
            return None

