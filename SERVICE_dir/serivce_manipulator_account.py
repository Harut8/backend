import jose.jwt
import redis

from DB_dir.db_manipulator_account import DatabaseManipulatorACCOUNT as DBManipulator
from MODELS_dir.acc_model import AccountRegModel
from MODELS_dir.acc_model import AccountSignModel
from SERVICE_dir import verify_email_sender as ves
from SERVICE_dir import send_recovery_code as src
from SERVICE_dir import send_unique_id as sui
from SERVICE_dir import jwt_logic


class ServiceManipulatorACCOUNT:
    """BUSINESS LOGIC FOR ACCOUNT"""
    recovery_code_var = None
    pass_for_email_send = None
    ACCESS_TOKEN_FOR_CHECK = None
    REFRESH_TOKEN_FOR_CHECK = None
    TOKEN_THREAD1 = None
    TOKEN_THREAD2 = None
    redis_client = redis.Redis(host='127.0.0.1', port=6379)

    @staticmethod
    def post_acc_into_temp_db(temp_acc_model: AccountRegModel):
        """ POST DATA TO temp db
            GET id for generating unique url for verifying
            UPDATE temp db and add link to table"""
        ServiceManipulatorACCOUNT.redis_client.set(
            temp_acc_model.acc_email,
            temp_acc_model.acc_pass,
            100)
        #ServiceManipulatorACCOUNT.pass_for_email_send = temp_acc_model.acc_pass
        if DBManipulator.post_acc_into_temp_db(item=temp_acc_model):
            id_for_link = DBManipulator.get_id_from_temp_db(name=temp_acc_model.acc_org_name)['t_id']
            id_for_link_generated_JWTencoded = jwt_logic.create_token_for_email_verify(str(id_for_link))
            generated_link = ves.generate_url(id_=id_for_link_generated_JWTencoded)
            if ves.send_verify_link(receiver_email=temp_acc_model.acc_email, message=generated_link):
                DBManipulator.post_link_into_temp_company(link=generated_link, name=temp_acc_model.acc_org_name)
                return True
            else:
                DBManipulator.delete_data_from_temp_if_failed(acc_email=temp_acc_model.acc_email)
                return False
        else:
            DBManipulator.delete_data_from_temp_if_failed(acc_email=temp_acc_model.acc_email)
            return False

    @staticmethod
    def verify_link(*, verify_token: str):
        """ verify email using temp id """
        temp_id = jose.jwt.decode(verify_token,
                                  jwt_logic.JWTParamas.VERIFY_SECRET_KEY,
                                  jwt_logic.JWTParamas.ALGORITHM)['sub']
        temp_ = DBManipulator.verify_link(temp_id=int(temp_id))
        if temp_ is not None:
            data = temp_['del_tmp_add_company'][1:-1].split(',')
            return data
        else:
            return None

    @staticmethod
    def recovery_code(*, receiver_email: str):
        """ METHOD FOR SENDING RECOVERY CODE
          tmp_ FOR SAVING RECOVERY CODE AND RETURN IT FOR
          CHECKING IN FUTURE"""
        tmp_ = src.send_recovery_code(receiver_email=receiver_email)
        from API_dir.api_creator import host

        ServiceManipulatorACCOUNT.redis_client.set(receiver_email, tmp_, 1000)
        if tmp_ is not None:
            return True
        else:
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
        if tmp_ is not None:
            from threading import Timer, Event
            ServiceManipulatorACCOUNT.TOKEN_THREAD1 = Timer(
                30, ServiceManipulatorACCOUNT.signin_acc,
                [acc_email, acc_pass]
            )
            ServiceManipulatorACCOUNT.TOKEN_THREAD2 = Timer(
                30, ServiceManipulatorACCOUNT.auto_update_token_for_account,
                args=[tmp_]
            )
            ServiceManipulatorACCOUNT.TOKEN_THREAD1.start()
            ServiceManipulatorACCOUNT.TOKEN_THREAD2.start()
            return tmp_
        return

    @staticmethod
    def signin_acc_info(*, acc_token: str):
        tmp_ = DBManipulator.signin_acc_info(acc_token=acc_token)
        if tmp_ is not None:
            return tmp_
        return

    @staticmethod
    def send_unique_code_and_pass(*, acc_unique_id: str, acc_email: str):
        """ IF unique_code sent then update table verify_status"""
        pass_for_sending = ServiceManipulatorACCOUNT.redis_client.get(acc_email).decode('ascii')
        if pass_for_sending is None:
            return False
        if sui.send_unique_id(receiver_email=acc_email,
                              message=f"Your unique code --- {acc_unique_id} ,"
                                      f" Your email --- {acc_email},"
                                      f" Your password --- {pass_for_sending}"):
            ServiceManipulatorACCOUNT.pass_for_email_send = None
            if DBManipulator.update_verify_status(acc_unique_id=int(acc_unique_id)):
                ServiceManipulatorACCOUNT.pass_for_email_send = None
                return True
        ServiceManipulatorACCOUNT.pass_for_email_send = None
        return False

    @staticmethod
    def add_access_token_to_account(*, access_token: str, account_id: str):
        """UPDATE ACCOUNT TOKEN"""
        if DBManipulator.add_access_token_to_account(access_token=access_token, account_id=str(account_id)):
            return True
        return False

    @staticmethod
    def check_refresh_token(*, client_refresh_token: str,):
        """CHECK SENDED TOKEN"""
        print(ServiceManipulatorACCOUNT.REFRESH_TOKEN_FOR_CHECK)
        if client_refresh_token == ServiceManipulatorACCOUNT.REFRESH_TOKEN_FOR_CHECK:
            return True
        return False

    @staticmethod
    def auto_update_token_for_account(account_object=None):
        """AUTOMATICLY UPDATE TOKENS FOR ACCOUNT"""
        if account_object is not None:
            jwt_logic.change_secret_keys()
            __ACCESS_TOKEN = jwt_logic.create_access_token(account_object)
            if ServiceManipulatorACCOUNT.add_access_token_to_account(
                access_token=__ACCESS_TOKEN,
                account_id=account_object['c_id']):
                return True
        return




