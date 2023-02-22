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
                """, {
                    "order_state": order_state,
                    "order_curr_type": order_curr_type
                })
                return connection.fetchall()
        except Exception as e:
            print(e)
            return

    @staticmethod
    def verify_payment_of_client(order_id):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("SELECT verify_payment(%(order_id)s)", {"order_id": int(order_id)})
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

