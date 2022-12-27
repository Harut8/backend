from DB_dir.db_manipulator import DatabaseManipulator as DBManipulator
from MODELS_dir.acc_model import AccountRegModel
from MODELS_dir.acc_model import AccountSignModel
from SERVICE_dir import verify_email_sender as ves
from SERVICE_dir import send_recovery_code as src


class ServiceManipulator:
    """BUSINESS LOGIC AFTER FETCHING DATA FROM DB"""
    recovery_code_var = None

    @staticmethod
    def post_acc_into_temp_db(temp_acc_model: AccountRegModel):
        """ POST DATA TO temp db
            GET id for generating unique url for verifying
            UPDATE temp db and add link to table"""
        if DBManipulator.post_acc_into_temp_db(item=temp_acc_model):
            id_for_link_generate = DBManipulator.get_id_from_temp_db(name=temp_acc_model.acc_org_name)['t_id']
            generated_link = ves.generate_url(id_=id_for_link_generate)
            ves.send_verify_link(receiver_email=temp_acc_model.acc_email, message=generated_link)
            DBManipulator.post_link_into_temp_company(link=generated_link, name=temp_acc_model.acc_org_name)
            return True
        else:
            return False

    @staticmethod
    def verify_link(*, temp_id: int):
        """ verify email using temp id"""
        if DBManipulator.verify_link(temp_id=temp_id):
            return True
        else:
            return False

    @staticmethod
    def recovery_code(*, receiver_email: str):
        tmp_ = src.send_recovery_code(receiver_email=receiver_email)
        if tmp_[0]:
            return tmp_[1]
        else:
            return False

    @staticmethod
    def update_acc_pass(*, acc_email: str, acc_new_pass: str):
        if DBManipulator.update_acc_pass(acc_email=acc_email, acc_pass=acc_new_pass):
            return True
        else:
            return False

    @staticmethod
    def signin_acc(*, acc_email: str, acc_pass: str):
        tmp_ = DBManipulator.signin_acc(acc_email=acc_email, acc_pass=acc_pass)
        if tmp_[0]:
            return True, tmp_[1]
        return tmp_





