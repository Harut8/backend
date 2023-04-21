import jose.jwt
from SERVICE_dir.jwt_logic import JWTParamas
from SERVICE_dir.send_excel import send_mail
from DB_dir.db_manipulator_tarifes import DatabaseManipulatorTARIFES
from MODELS_dir.tarif_model import (TarifModelForView,
                                    InnerModelForTarif,
                                    TarifToClient,
                                    PersonalTarifForClient,
                                    PersonalTarifInfo,
                                    PersonalTarifForView,
                                    BuyTarifeByTransfer,
                                    TarifModelForExcel)

language_dict = {
            "ru": 0,
            "en": 1,
            "hy": 2
        }


class ServiceManipulatorTARIFES:
    """BUSINESS LOGIC FOR TARIFES"""
    @staticmethod
    def check_summ_and_return(
            item: PersonalTarifInfo):
        try:
            summ_ = item.mobile_cass_price*item.mobile_cass_count+\
            item.cass_stantion_count*item.cass_stantion_price+\
            item.mobile_cass_count*item.mobile_cass_price+\
            item.web_manager_price*item.web_manager_count
            return summ_
        except Exception as e:
            print(e)
            return

    @staticmethod
    def send_link_excel_download(order_id):
        info_ = DatabaseManipulatorTARIFES.get_email_for_excel(order_id)
        print(info_, "hasav")
        if info_:
            if send_mail(info_["c_email"], order_id):
                print("success")
                return True
        return

    @staticmethod
    def get_tarif_details(tarif_id):
        info_ = DatabaseManipulatorTARIFES.get_tarif_details(tarif_id)
        if info_ is not None:
            return info_
        return

    @staticmethod
    def change_valute_to_card(tarif_id):
        info_ = DatabaseManipulatorTARIFES.change_valute_to_card(tarif_id)
        if info_ is not None:
            return info_
        return

    @staticmethod
    def post_transfer_tarif(
            item: BuyTarifeByTransfer,
            valute: int):
        try:
            print(item.tarif_id)
            temp_ = DatabaseManipulatorTARIFES.post_personal_info_to_order(
                order_summ=item.order_summ,
                tarif_id=item.tarif_id,
                cass_stantion_count=item.cass_stantion_count,
                mobile_cass_count=item.mobile_cass_count,
                mobile_manager_count=item.mobile_manager_count,
                web_manager_count=item.web_manager_count,
                client_token=item.client_token,
                interval=item.interval,
                valute=valute
            )
            if temp_:
                return temp_
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_tarifes_for_view(language: str):
        """Returns tarifes table for view"""
        temp_ = DatabaseManipulatorTARIFES.get_tarifes_for_view()
        try:
            lan_ = language_dict[language]
            if temp_ is not None:
                print(temp_)
                data_for_view = [
                    TarifModelForView(
                        tarif_id=i['tarif_id'],
                        tarif_names=i['tarif_names'][lan_],
                        tarif_month_prices=i['tarif_month_prices'],
                        inner_content=InnerModelForTarif(
                            cassa_names=i['cassa_names'][lan_],
                            cassa_counts=i['cassa_counts'],
                            manager_names=i['manager_names'][lan_],
                            manager_counts=i['manager_counts'],
                            web_names=i['web_names'][lan_],
                            web_counts=i['web_counts'],
                            mobile_cassa_names=i['mobile_cassa_names'][lan_],
                            mobile_cassa_counts=i['mobile_cassa_counts'],
                            tarifes_others=i['tarifes_others'],)
                    )
                    for i in temp_
                ]
                return data_for_view
            else:
                return None
        except Exception as e:
            print(e)
            return

    @staticmethod
    def post_tarif_to_company(*, tarif: TarifToClient, client_token: str):
        """ ADD TARIF TO CLIENT USING TOKEN"""
        try:
            id_ = jose.jwt.decode(
                client_token,
                JWTParamas.ACCESS_SECRET_KEY,
                JWTParamas.ALGORITHM)['sub'].replace(JWTParamas.SOLD_KEY, "")
            temp_ = DatabaseManipulatorTARIFES.post_tarife_to_client(
                company_id=id_,
                tarif_id_or_info=tarif.tarif_id_or_info)
            if temp_:
                return True
            return None
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_info_for_excel(order_id):
        try:
            info_ = DatabaseManipulatorTARIFES.get_info_for_excel(order_id)
            if info_ is not None:
                return TarifModelForExcel(
                    order_id=info_['order_id'],
                    c_name=info_['c_name'],
                    c_inn=info_['c_inn'],
                    c_address=info_['c_address'],
                    order_summ=info_['order_summ'],
                    count=info_['count'],
                    csc=info_['csc'],
                    mcc=info_['mcc'],
                    mmc=info_['mmc'],
                    wmc=info_['wmc'],
                )
            return
        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_tarifes_for_personal_crateing(language):
        try:
            temp_ = DatabaseManipulatorTARIFES.get_tarifes_for_personal()
            #print(temp_)
            lan_ = language_dict[language]
            if temp_ is None:
                return
            else:
                #return temp_
                return PersonalTarifForView(
                cass_stantion_name=temp_[3]["c_f_name"][lan_],
                cass_stantion_price=temp_[3]["c_per_price"],
                mobile_cass_name=temp_[2]["c_f_name"][lan_],
                mobile_cass_price=temp_[2]["c_per_price"],
                mobile_manager_name=temp_[0]["c_f_name"][lan_],
                mobile_manager_price=temp_[0]["c_per_price"],
                web_manager_name =temp_[1]["c_f_name"][lan_],
                web_manager_price=temp_[1]["c_per_price"],

                )
        except Exception as e:
            print(e)
            return

