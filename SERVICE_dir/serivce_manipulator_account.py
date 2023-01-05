from DB_dir.db_manipulator_account import DatabaseManipulatorACCOUNT as DBManipulator
from MODELS_dir.acc_model import AccountRegModel
from MODELS_dir.acc_model import AccountSignModel
from SERVICE_dir import verify_email_sender as ves
from SERVICE_dir import send_recovery_code as src
from SERVICE_dir import send_unique_id as sui


class ServiceManipulatorACCOUNT:
    """BUSINESS LOGIC FOR ACCOUNT"""
    recovery_code_var = None
    pass_for_email_send = None

    @staticmethod
    def post_acc_into_temp_db(temp_acc_model: AccountRegModel):
        """ POST DATA TO temp db
            GET id for generating unique url for verifying
            UPDATE temp db and add link to table"""
        ServiceManipulatorACCOUNT.pass_for_email_send = temp_acc_model.acc_pass
        if DBManipulator.post_acc_into_temp_db(item=temp_acc_model):
            id_for_link_generate = DBManipulator.get_id_from_temp_db(name=temp_acc_model.acc_org_name)['t_id']
            generated_link = ves.generate_url(id_=id_for_link_generate)
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
    def verify_link(*, temp_id: int):
        """ verify email using temp id """
        temp_ = DBManipulator.verify_link(temp_id=temp_id)
        if temp_[0]:
            data = temp_[1]['del_tmp_add_company'][1:-1].split(',')
            print(data)
            return True, data[0], data[1]
        else:
            return False,

    @staticmethod
    def recovery_code(*, receiver_email: str):
        """ METHOD FOR SENDING RECOVERY CODE
          tmp_ FOR SAVING RECOVERY CODE AND RETURN IT FOR
          CHECKING IN FUTURE"""
        tmp_ = src.send_recovery_code(receiver_email=receiver_email)
        if tmp_[0]:
            return tmp_[1]
        else:
            return False

    @staticmethod
    def update_acc_pass(*, acc_email: str, acc_new_pass: str):
        """UPDATE PASSWORD AFTER SUCCESS RECOVERY CODE CHECKING"""
        if DBManipulator.update_acc_pass(acc_email=acc_email, acc_pass=acc_new_pass):
            return True
        else:
            return False

    @staticmethod
    def signin_acc(*, acc_email: str, acc_pass: str):
        """ Signin checking and return data from db """
        tmp_ = DBManipulator.signin_acc(acc_email=acc_email, acc_pass=acc_pass)
        if tmp_[0]:
            return True, tmp_[1]
        return tmp_

    @staticmethod
    def send_unique_code_and_pass(*, acc_unique_id: str, acc_email: str):
        """ IF unique_code sent then update table verify_status"""
        if ServiceManipulatorACCOUNT.pass_for_email_send is None:
            return False
        if sui.send_unique_id(receiver_email=acc_email,
                              message=f"Your unique code --- {acc_unique_id} ,"
                                      f" Your email --- {acc_email},"
                                      f" Your password --- {ServiceManipulatorACCOUNT.pass_for_email_send}"):
            ServiceManipulatorACCOUNT.pass_for_email_send = None
            if DBManipulator.update_verify_status(acc_unique_id=int(acc_unique_id)):
                return True
        ServiceManipulatorACCOUNT.pass_for_email_send = None
        return False





