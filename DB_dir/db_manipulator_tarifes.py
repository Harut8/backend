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
    def get_email_for_excel(order_id):
        """R"""
        with DBConnection.create_cursor() as cursor:
            try:
                cursor.execute("SELECT c_email FROM company where "
                               "c_id = (select company_id from saved_order_and_tarif where order_id=%(order_id)s)",
                               {'order_id': order_id})
                temp_ = cursor.fetchone()
                return temp_
            except Exception as e:
                print(e)
                return None

    @staticmethod
    def post_personal_info_to_order(*,
                                    order_summ,
                                    cass_stantion_count,
                                    mobile_cass_count,
                                    mobile_manager_count,
                                    web_manager_count,
                                    client_token,
                                    interval
                                    ):
        """Returns a dict of tarifes information"""
        with DBConnection.create_cursor() as cursor:
            try:
                cursor.execute(
                    """
                    do 
                    $do$
                    declare 
                    inn_info int;
                    begin
                    SELECT c_inn into inn_info from company where c_token = %(client_token)s;
                    if inn_info is null then 
                        raise Exception 'error' ;
                    end if;
                    end;
                    $do$
                    """
                ,{
                    "client_token": client_token
                    })
                cursor.execute("""select c_id from company where c_token = %(client_token)s""",{"client_token":client_token})
                company_id = cursor.fetchone()["c_id"]
                cursor.execute("""
                INSERT INTO saved_order_and_tarif(
                               order_summ,
                               cass_stantion_count,
                               mobile_cass_count,
                               mobile_manager_count,
                               web_manager_count,
                               company_id,
                               order_ending
                               ) VALUES(
                               %(order_summ)s,
                               %(cass_stantion_count)s,
                               %(mobile_cass_count)s,
                               %(mobile_manager_count)s,
                               %(web_manager_count)s,
                               %(company_id)s,
                               current_timestamp + interval '%(interval)s month'
                               ) RETURNING order_id"""
                               ,
                               {
                                   "order_summ": order_summ,
                                   "cass_stantion_count": cass_stantion_count,
                                   "mobile_cass_count": mobile_cass_count,
                                   "mobile_manager_count": mobile_manager_count,
                                   "web_manager_count": web_manager_count,
                                   "company_id": company_id,
                                   "interval": interval
                               })
                info = cursor.fetchone()
                DBConnection.commit()
                return info
            except Exception as e:
                print(e)
                return None

    @staticmethod
    def get_tarifes_for_personal():
        """RETURN dict tarif info for personal createing"""
        with DBConnection.create_cursor() as cursor:
            try:
                cursor.execute("""
                select c_f_name,c_per_price from cassa_field cf where cf.c_f_id =1
                union
                select m_f_name,m_per_price from manager_field mf  where mf.m_f_id =1
                union
                select w_m_f_name,w_m_per_price from web_manager_field sf  where sf .w_m_f_id =1
                union
                select m_c_f_name,m_c_per_price from mobile_cassa_field mcf  where mcf .m_c_f_id =1
                ;""")
                temp_ = cursor.fetchall()
                return temp_
            except Exception as e:
                print(e)
                return None

    @staticmethod
    def get_info_for_excel(order_id):
        with DBConnection.create_cursor() as cursor:
            try:
                cursor.execute("""
                select order_id,
                       c_name,
                       c_inn,
                       c_address,
                       order_summ, 
                       soad.cass_stantion_count +soad.mobile_cass_count + soad.mobile_manager_count+ soad.web_manager_count as count,
                       soad.cass_stantion_count as csc,
                       soad.mobile_cass_count as mcc,
                       soad.mobile_manager_count as mmc,
                       soad.web_manager_count as wmc
                       
                from company cy
                join saved_order_and_tarif soad on soad.company_id = cy.c_id
                where order_id = %(order_id)s
                ;""",
                               {"order_id": order_id})
                temp_ = cursor.fetchone()
                return temp_
            #(select company_id from saved_order_and_tarif where order_id = %(order_id)s)
            except Exception as e:
                print(e)
                return None
    # @staticmethod
    # def post_tarife_to_client(*, company_id: int, tarif_id_or_info):
    #     """ ADD TARIF TO CLIENT TABLE"""
    #     with DBConnection.create_cursor() as cursor:
    #         try:
    #             if isinstance(tarif_id_or_info, int):
    #                 cursor.execute("INSERT INTO client_tarif (c_t_id, c_t_tarif_id)"
    #                                "VALUES ( %(company_id)s, %(tarif_id)s)",
    #                                {'company_id': company_id,
    #                                 'tarif_id': tarif_id_or_info
    #                                 })
    #                 DBConnection.commit()
    #                 return True
    #             else:
    #                 # cursor.execute("SELECT add_personal_tarifes("
    #                 #                "%(cassa_count)s ,"
    #                 #                "%(manager_count)s ,"
    #                 #                "%(sklad_count)s ,"
    #                 #                "%(company_id)s"
    #                 #                ")",
    #                 #                {'cassa_count': tarif_id_or_info.cass_stantion,
    #                 #                 'manager_count': tarif_id_or_info.mobile_manager,
    #                 #                 'sklad_count': tarif_id_or_info.web_manager,
    #                 #                 'company_id': company_id})
    #                 # DBConnection.commit()
    #                 return None
    #         except Exception as e:
    #             print(e)
    #             return None

