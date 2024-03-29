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
        print(11)
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
	DELETE FROM client_tarif where c_t_tarif_id = '992112fb-1ed1-45f4-90d9-fabb0532069a'
	 and c_t_id = (select company_id from saved_order_and_tarif where order_id = %(order_id_)s);
	DELETE FROM saved_order_and_tarif WHERE tarif_id_fk = '992112fb-1ed1-45f4-90d9-fabb0532069a'
	 and company_id = (select company_id from saved_order_and_tarif where order_id = %(order_id_)s);
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

                """, {"order_id_": order_id})
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
                               {"order_id": order_id})
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



