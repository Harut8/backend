from MODELS_dir.admin_model import PaymentListEnum, PaymentListView
from DB_dir.db_manipulator_admin import DatabaseManipulatorADMIN
from .admin_client_secure import encode_client_id_for_url, decode_client_id_for_verify


class ServiceManipulatorADMIN:

    @staticmethod
    def verify_payment_of_client(order_id_token: str):
        order_id = decode_client_id_for_verify(order_id_token)
        if DatabaseManipulatorADMIN.verify_payment_of_client(order_id):
            return True
        return None

    @classmethod
    def __create_list_of_payment(cls, info_):
        return [
            PaymentListView(
                order_id=encode_client_id_for_url(i["order_id"]),
                order_summ=i["order_summ"],
                cass_stantion_count=i["cass_stantion_count"],
                mobile_cass_count=i["mobile_cass_count"],
                mobile_manager_count=i["mobile_manager_count"],
                web_manager_count=i["web_manager_count"],
                order_curr_type=i["order_curr_type"],
                order_date=i["order_date"],
                order_ending=i["order_ending"],
            )
            for i in info_
        ]

    @staticmethod
    def get_payment_list(type_of_payment: PaymentListEnum):
        match type_of_payment:
            case type_of_payment.typetransferbuyed:
                info_ = DatabaseManipulatorADMIN.get_payments_for_view(
                    order_state=True,
                    order_curr_type=(0,)
                )
                if info_ is not None:
                    return ServiceManipulatorADMIN.__create_list_of_payment(info_)
                return
            case type_of_payment.typecardbuyed:
                info_ = DatabaseManipulatorADMIN.get_payments_for_view(
                    order_state=True,
                    order_curr_type=(1,)
                )
                if info_ is not None:
                    return ServiceManipulatorADMIN.__create_list_of_payment(info_)
                return
            case type_of_payment.typeinorder:
                info_ = DatabaseManipulatorADMIN.get_payments_for_view(
                    order_state=False,
                    order_curr_type=(0, 1)
                )
                if info_ is not None:
                    return ServiceManipulatorADMIN.__create_list_of_payment(info_)
                return
            case type_of_payment.typeall:
                info_ = DatabaseManipulatorADMIN.get_payments_for_view(
                    order_state=True,
                    order_curr_type=(0, 1)
                )
                if info_ is not None:
                    return ServiceManipulatorADMIN.__create_list_of_payment(info_)
                return
            case _:
                return
