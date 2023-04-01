import jose.jwt
import redis
import asyncio
from DB_dir.db_manipulator_account import DatabaseManipulatorACCOUNT as DBManipulator
from MODELS_dir.acc_model import AccountRegModel
from MODELS_dir.acc_model import AccountSignModel, AccountViewModel, AccountViewInnerModel
from SERVICE_dir import verify_email_sender as ves
from SERVICE_dir import send_recovery_code as src
from SERVICE_dir import send_unique_id as sui
from SERVICE_dir import jwt_logic
from SERVICE_dir.admin_client_secure import decode_client_id_for_verify


class ServiceManipulatorACCOUNT:
    """BUSINESS LOGIC FOR ACCOUNT"""
    recovery_code_var = None
    pass_for_email_send = None
    TOKEN_THREAD1 = None
    TOKEN_THREAD2 = None
    redis_client = redis.Redis(host='127.0.0.1', port=6379)
    language_dict = {
        "ru": 0,
        "en": 1,
        "hy": 2
    }

    @staticmethod
    def call_async_function(acc_email, generated_link,):
        ves.send_verify_link(
            receiver_email=acc_email,
            message=generated_link)

    @staticmethod
    def get_links():
        try:
            info_ = DBManipulator.get_links()
            if info_ is not None:
                return info_
            return
        except Exception as e:
            raise e

    @staticmethod
    async def post_acc_into_temp_db(temp_acc_model: AccountRegModel):
        """ POST DATA TO temp db
            GET id for generating unique url for verifying
            UPDATE temp db and add link to table"""
        try:
            #SAVE IN REDIS
            #email and password for sending with unique code
            #after verify link click
            ServiceManipulatorACCOUNT.redis_client.set(
                temp_acc_model.acc_email,
                temp_acc_model.acc_pass,
                600)
            DATA_ = DBManipulator.post_acc_into_temp_db(item=temp_acc_model)
            if DATA_:
                if DATA_ == "ka":
                    return "ka"
                id_for_link = DBManipulator.get_id_from_temp_db(name=temp_acc_model.acc_org_name)['t_id']
                id_for_link_generated_JWTencoded = jwt_logic.create_token_for_email_verify(str(id_for_link))
                generated_link = ves.generate_url(id_=id_for_link_generated_JWTencoded)
                if 1 == 1:
                    task2 = asyncio.create_task(
                        DBManipulator.post_link_into_temp_company(link=generated_link,
                                                                  name=temp_acc_model.acc_org_name))
                    await task2
                    return temp_acc_model.acc_email, generated_link
                else:
                    #DBManipulator.delete_data_from_temp_if_failed(acc_email=temp_acc_model.acc_email)
                    return None
            else:
                #DBManipulator.delete_data_from_temp_if_failed(acc_email=temp_acc_model.acc_email)
                return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def verify_link(*, verify_token: str):
        """ verify email using temp id """
        try:
            temp_id = jose.jwt.decode(verify_token,
                                      jwt_logic.JWTParamas.VERIFY_SECRET_KEY,
                                      jwt_logic.JWTParamas.ALGORITHM)['sub']
            temp_ = DBManipulator.verify_link(temp_id=int(temp_id))
            if temp_ is not None:
                data = temp_['del_tmp_add_company'][1:-1].split(',')
                return data
            else:
                return None
        except Exception as e:
            print(e)
            return

    @staticmethod
    def recovery_code(*, receiver_email: str):
        """ METHOD FOR SENDING RECOVERY CODE
          tmp_ FOR SAVING RECOVERY CODE AND RETURN IT FOR
          CHECKING IN FUTURE"""
        tmp_ = src.send_recovery_code(receiver_email=receiver_email)
        from API_dir.api_creator import host
        try:
            #save recovery code for future checking
            ServiceManipulatorACCOUNT.redis_client.set(receiver_email, tmp_, 600)
            if tmp_ is not None:
                return True
            else:
                return
        except Exception as e:
            print(e)
            return

    @staticmethod
    def recovery_code_checker(*, code_for_verify: str, receiver_email: str):
        #red_client = redis.Redis(host='127.0.0.1', port=6379)
        try:
            code_in_db = ServiceManipulatorACCOUNT.redis_client.get(receiver_email)
            print(code_in_db, code_for_verify)
            return int(code_in_db) == int(code_for_verify)
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_acc_pass(*, acc_email: str, acc_new_pass: str):
        """UPDATE PASSWORD AFTER SUCCESS RECOVERY CODE CHECKING"""
        if DBManipulator.update_acc_pass(acc_email=acc_email, acc_pass=acc_new_pass):
            return True
        else:
            return False

    @staticmethod
    def signin_acc(acc_email: str, acc_pass: str,):
        """ SEND DATA FOR VALIDATING IN DATABASE
            START THREADS FOR CHANGING TOKEN EVERY 30 MINUTE
        """
        tmp_ = DBManipulator.signin_acc(acc_email=acc_email, acc_pass=acc_pass)
        try:
            if tmp_ is not None:
                return tmp_
            return
        except Exception as e:
            print(e)
            return

    @staticmethod
    def signin_acc_info(*, acc_token: str, lan: str):
        tmp_ = DBManipulator.signin_acc_info(acc_token=acc_token, lan_num=ServiceManipulatorACCOUNT.language_dict[lan]+1)
        if tmp_ is not None:
            print(tmp_)
            return AccountViewModel(
                c_id=tmp_["c_id"],
                c_name=tmp_["c_name"],
                c_contact_name=tmp_["c_contact_name"],
                c_phone=tmp_["c_phone"],
                c_email=tmp_["c_email"],
                tarif_list=tmp_["tarif_list"],
            )
        return

    @staticmethod
    def send_unique_code_and_pass(*, acc_unique_id: str, acc_email: str):
        """ IF unique_code sent then update table verify_status"""
        try:
            pass_for_sending = ServiceManipulatorACCOUNT.redis_client.get(acc_email)
            if pass_for_sending is None:
                return False
            pass_for_sending = pass_for_sending.decode('ascii')
            if sui.send_unique_id(receiver_email=acc_email,
                                  message=f"Your unique code --- {acc_unique_id} ,"
                                          f" Your email --- {acc_email},"
                                          f" Your password --- {pass_for_sending}"):
                if DBManipulator.update_verify_status(acc_unique_id=int(acc_unique_id)):
                    return True
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def add_access_token_to_account(*, access_token: str, account_id: str):
        """UPDATE ACCOUNT TOKEN"""
        if DBManipulator.update_acc_token(
                access_token=access_token,
                acc_id=str(account_id)):
            return True
        return False

    @staticmethod
    def check_refresh_token(*, client_id: str, client_refresh_token: str,):
        """CHECK SENDED TOKEN WITH REDIS SAVED TOKEN"""
        try:
            real_refresh_token = ServiceManipulatorACCOUNT.\
                redis_client.get(
                client_id+jwt_logic.JWTParamas.SOLD_KEY + 'refresh').\
                decode('ascii')
            if client_refresh_token == real_refresh_token:
                return True
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def auto_update_token_for_account(account_id=None, access_token=None):
        """AUTOMATICLY UPDATE TOKENS FOR ACCOUNT IF CHECKING OF REFRESH TOKEN IS OK"""
        try:
            if account_id is not None and access_token is not None:
                if ServiceManipulatorACCOUNT.\
                        add_access_token_to_account(
                        access_token=access_token,
                        account_id=account_id,):
                    return True
            return
        except Exception as e:
            print(e)
            return False




