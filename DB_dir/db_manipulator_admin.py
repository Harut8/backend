from .db_connection import DatabaseConnection as DBConnection


class DatabaseManipulatorADMIN:

    @staticmethod
    def get_payments_for_view(*, order_state: bool, order_curr_type: tuple):
        try:
            with DBConnection.create_cursor() as connection:
                connection.execute("""
                select order_id,
                       
                       order_summ,
                       cass_stantion_count,
                       mobile_cass_count,
                       mobile_manager_count,
                       web_manager_count,
                       order_curr_type,
                       order_date,
                       order_ending 
                from saved_order_and_tarif soat 
                where order_state = %(order_state)s 
                and order_curr_type in  %(order_curr_type)s
                order by order_date desc
                """, {
                    "order_state": order_state,
                    "order_curr_type": order_curr_type
                })
                return connection.fetchall()
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_links_for_sending(order_id):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute(""" 
                SELECT * from get_links_state(%(order_id)s);
                """, {'order_id': order_id})
                info_ = cursor.fetchone()
                if info_ is not None:
                    return [j for j in info_.values()]
                return
        except Exception as e:
            print(e)
            return

    @staticmethod
    def verify_payment_of_client(order_id):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""
                do
                $$
begin
	if (select order_state from saved_order_and_tarif soat  where order_id = %(order_id_)s) = true 
	then
	update client_tarif set start_license = current_timestamp, end_license = 
                current_timestamp+
                concat(date_part('day',(select order_ending -order_date from saved_order_and_tarif where order_id=%(order_id_)s)), ' days')::interval
                where c_t_tarif_id = (select tarif_id_fk from saved_order_and_tarif where order_id = %(order_id_)s);
	else
	DELETE FROM client_tarif where c_t_tarif_id = 1 and c_t_id = (select company_id from saved_order_and_tarif where order_id = %(order_id_)s);
	DELETE FROM saved_order_and_tarif WHERE tarif_id_fk = 1 and company_id = (select company_id from saved_order_and_tarif where order_id = %(order_id_)s);
	update saved_order_and_tarif set order_state = true where order_id = %(order_id_)s;
                INSERT INTO client_tarif(c_t_id, c_t_tarif_id, end_license)
                select company_id,
                tarif_id_fk,
                current_timestamp+
                concat(date_part('day',(select order_ending -order_date from saved_order_and_tarif where order_id=%(order_id_)s)), ' days')::interval
                from saved_order_and_tarif where order_id=%(order_id_)s;
end if;
end;
$$

                """, {"order_id_": int(order_id)})
                DBConnection.commit()
                return True
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_email_for_link(order_id):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("select c_email from company where c_id = "
                               "(SELECT company_id from saved_order_and_tarif where order_id = %(order_id)s)",
                               {"order_id": int(order_id)})
                return cursor.fetchone()
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_links(order_id):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""
                 select product_link  from links l 
                 where product_id in (
                 select
                 case
                 when cass_stantion_count <> 0 then 1
                 else Null
                 end from saved_order_and_tarif soat 
                 where order_id = %(order_id)s
                 union
                 select 
                 case
                 when mobile_cass_count <> 0 then 2
                 else Null
                 end from saved_order_and_tarif soat 
                 where order_id = %(order_id)s
                 union 
                 select 
                 case
                 when web_manager_count <> 0 then 3
                 else Null
                 end from saved_order_and_tarif soat 
                 where order_id = %(order_id)s
                 union 
                 select 
                 case
                 when mobile_manager_count <> 0 then 4
                 else Null
                 end 
                 from saved_order_and_tarif soat 
                 where order_id = %(order_id)s)""",
                               {"order_id": int(order_id)})
                return cursor.fetchone()
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_dillers():
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute(
                    """
                    select d.d_name, d.d_id from diller d order by d.d_id;
                    """
                )
                info_ = cursor.fetchall()
                return info_
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_comapnies(admin_login, search:str):
        try:
            if search.isdigit():
                search_from = "c_inn"
            else:
                search_from = "c_name"
            print(search_from)
            with DBConnection.create_cursor() as cursor:
                cursor.execute(
                    f"""
                    with cte as (
                    select c_id,
                    case 
                    when (select * from (select pt2.permission_id = 1 as tip from admin_table at2
                        join privilege_table pt on at2.admin_privilege = pt.privilege_id 
                        join permission_table pt2 on pt2.permission_id = pt.privilege_type 
                        where at2.admin_login=%(admin_login)s) s where tip in (true)) then c_unique_id
                    else 0
                    end as c_unique_id, c_diller_id, c_name, c_contact_name, c_phone, c_email, c_inn, c_address,
                    row_number () over(partition by c.c_diller_id order by c.c_diller_id) as numer from company c)
                    select * from cte where {search_from} like %(search)s;
                    """,
                    {'admin_login': admin_login,
                     "search": '%'+search+'%'}
                )
                info_ = cursor.fetchall()
                return info_
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_company_and_tarif_by_id(company_id):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""
                select distinct soat.order_id, soat.order_summ, soat.order_date pay_date,
soat.cass_stantion_count, soat.mobile_cass_count, soat.mobile_manager_count, soat .web_manager_count,
(select curr_name from curr_types where curr_id = soat.order_curr_type) as curr_type,
case 
	when soat.order_state then (select ct.start_license from client_tarif ct where ct.c_t_id = soat.company_id and ct.c_t_tarif_id = soat.tarif_id_fk )
	else null 
end start_license,
case 
	when soat.order_state then (select ct.end_license from client_tarif ct where ct.c_t_id = soat.company_id and ct.c_t_tarif_id = soat.tarif_id_fk )
	else null
end end_license
from saved_order_and_tarif soat
left join client_tarif ct on ct.c_t_id = soat.company_id 
where soat.company_id = %(comp_id)s
                """, {
                    'comp_id': company_id
                })
                return cursor.fetchall()
        except Exception as e:
            raise e

    @staticmethod
    def block_tarif_for_company(order_id, admin_login):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""select * from check_permission(%(admin_login)s)""", {
                    'admin_login': admin_login
                })
                if cursor.fetchone()["check_permission"] != 1:
                    return
                cursor.execute("""
                UPDATE saved_order_and_tarif set order_state = false where order_id = %(order_id)s;
                """, {"order_id": order_id})
                return 1
        except Exception as e:
            raise e

    @staticmethod
    def check_permission(admin_login):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""select * from check_permission(%(admin_login)s)""", {
                    'admin_login': admin_login
                })
                if cursor.fetchone()["check_permission"] != 1:
                    return
                return 1
        except Exception as e:
            raise e

    @staticmethod
    def signin_admin(admin_login, admin_password):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""
                select at2.admin_login, at2.admin_name, at2.admin_privilege  from admin_table at2 
                where at2.admin_login = %(admin_login)s and at2.admin_password = %(admin_password)s;
                """, {
                    'admin_login': admin_login,
                    'admin_password': admin_password
                })
                return cursor.fetchone()
        except Exception as e:
            raise e

    @staticmethod
    def get_used_device_count(company_id):
        try:
            product_id_table = {
                1: 'cass_stantion_count',
                2: 'mobile_cass_count',
                3: 'web_manager_count',
                4: 'mobile_manager_count'
            }
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""
                with cte2 as (
                select count(*), l.product_id_fk  from licenses l
                where l.unique_id_cp = (select c.c_unique_id  from company c where c.c_id = %(comp_id)s)
                group by l.product_id_fk order by l.product_id_fk )
                select * from cte2;
                """, {
                    'comp_id': company_id
                })
                #print(cursor.fetchone())
                return [{product_id_table[i["product_id_fk"]]:i["count"]} for i in cursor.fetchall()]
        except Exception as e:
            raise e


