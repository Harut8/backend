# import hashlib
# from datetime import datetime, timezone
# from MODELS_dir.admin_model import PaymentListEnum, PaymentListView
# from DB_dir.db_manipulator_admin import DatabaseManipulatorADMIN
# from .admin_client_secure import encode_client_id_for_url, decode_client_id_for_verify
#
#
# class ServiceManipulatorADMIN:
#
#     @staticmethod
#     def verify_payment_of_client(order_id_token: str):
#         info_ = decode_client_id_for_verify(order_id_token)
#         order_id = info_.sub
#         time_state = info_.exp
#         print(time_state, order_id)
#         if time_state > datetime.now(tz=timezone.utc):
#             if DatabaseManipulatorADMIN.verify_payment_of_client(order_id):
#                 print('ok')
#                 return True
#         return None
#
#     @staticmethod
#     def links_for_downloading(order_id_token):
#         order_id = decode_client_id_for_verify(order_id_token).sub
#         info_ = DatabaseManipulatorADMIN.get_links_for_sending(order_id)
#         if info_ is not None:
#             return info_
#         return
#
#     @staticmethod
#     def send_email_for_order_verify(order_id_token: str):
#         order_id = decode_client_id_for_verify(order_id_token).sub
#         info_ = DatabaseManipulatorADMIN.get_email_for_link(order_id)
#         if info_ is not None:
#             return info_['c_email']
#         return
#
#     @staticmethod
#     def check_permission(admin_login):
#         if DatabaseManipulatorADMIN.check_permission(admin_login):
#             return True
#
#     @classmethod
#     def __create_list_of_payment(cls, info_):
#         return [
#             PaymentListView(
#                 order_id=encode_client_id_for_url(i["order_id"]),
#                 order_summ=i["order_summ"],
#                 cass_stantion_count=i["cass_stantion_count"],
#                 mobile_cass_count=i["mobile_cass_count"],
#                 mobile_manager_count=i["mobile_manager_count"],
#                 web_manager_count=i["web_manager_count"],
#                 order_curr_type=i["order_curr_type"],
#                 order_date=i["order_date"],
#                 order_ending=i["order_ending"],
#                 c_name=i["c_name"],
#                 c_contact_name=i["c_contact_name"],
#                 c_phone=i["c_phone"],
#                 c_email=i["c_email"],
#                 c_inn=i["c_inn"],
#                 c_address=i["c_address"],
#             )
#             for i in info_
#         ]
#
#     @staticmethod
#     def get_payment_list(type_of_payment: PaymentListEnum):
#         match type_of_payment:
#             case type_of_payment.typetransferbuyed:
#                 info_ = DatabaseManipulatorADMIN.get_payments_for_view(
#                     order_state=(True, False),
#                     order_curr_type=(0,)
#                 )
#                 if info_ is not None:
#                     return ServiceManipulatorADMIN.__create_list_of_payment(info_)
#                 return
#             case type_of_payment.typecardbuyed:
#                 info_ = DatabaseManipulatorADMIN.get_payments_for_view(
#                     order_state=(True, False),
#                     order_curr_type=(1,)
#                 )
#                 if info_ is not None:
#                     return ServiceManipulatorADMIN.__create_list_of_payment(info_)
#                 return
#             case type_of_payment.typeinorder:
#                 info_ = DatabaseManipulatorADMIN.get_payments_for_view(
#                     order_state=(False,),
#                     order_curr_type=(0, 1)
#                 )
#                 if info_ is not None:
#                     return ServiceManipulatorADMIN.__create_list_of_payment(info_)
#                 return
#             case type_of_payment.typeall:
#                 info_ = DatabaseManipulatorADMIN.get_payments_for_view(
#                     order_state=(True, False),
#                     order_curr_type=(0, 1, 2)
#                 )
#                 if info_ is not None:
#                     return ServiceManipulatorADMIN.__create_list_of_payment(info_)
#                 return
#             case _:
#                 return
#
#     @staticmethod
#     def get_companies(admin_login, search):
#         dillers = DatabaseManipulatorADMIN.get_dillers()
#         companies = DatabaseManipulatorADMIN.get_comapnies(admin_login=admin_login, search=search)
#         return_data = {i["d_id"]: [] for i in dillers}
#         if companies:
#             for i in companies:
#                 return_data[i["c_diller_id"]] += [i.items()]
#             for i in dillers:
#                 return_data[i["d_name"]] = return_data.pop(i["d_id"])
#
#         return return_data
#
#     @staticmethod
#     def get_company_and_tarif_by_id(company_id):
#         info_ = DatabaseManipulatorADMIN.get_company_and_tarif_by_id(company_id)
#         info_2 = DatabaseManipulatorADMIN.get_used_device_count(company_id)
#         if info_ and info_2:
#             return {"tarifes": info_, "used_device": info_2}
#
#     @staticmethod
#     def block_tarif_for_company(order_id, admin_login):
#         if DatabaseManipulatorADMIN.block_tarif_for_company(order_id, admin_login):
#             return 1
#
#     @staticmethod
#     def signin_admin(admin_login, admin_password):
#         acc_pass = hashlib.sha256(admin_password.encode()).hexdigest().upper()
#         info_ = DatabaseManipulatorADMIN.signin_admin(admin_login, acc_pass)
#         if info_:
#             return info_
#         return
#
#
