from DB_dir.db_manipulator import DatabaseManipulator as DBManipulator
from MODELS_dir.acc_reg_model import AccountRegModel
from SERVICE_dir import email_sender as es


class ServiceManipulator:
    """BUSINESS LOGIC AFTER FETCHING DATA FROM DB"""

    @staticmethod
    def post_acc_into_temp_db(temp_acc_model: AccountRegModel):
        """ POST DATA TO temp db
            GET id for generating unique url for verifying
            UPDATE temp db and add link to table"""
        if DBManipulator.post_acc_into_temp_db(item=temp_acc_model):
            id_for_link_generate = DBManipulator.get_id_from_temp_db(name=temp_acc_model.acc_org_name)[0]['t_id']
            generated_link = es.generate_url(id=id_for_link_generate)
            es.send_message(receiver_email=temp_acc_model.acc_email, message=generated_link)
            DBManipulator.post_link_into_temp_company(link=generated_link, name=temp_acc_model.acc_org_name)
            return True
        else:
            raise Exception('SOMETHING ERROR')
        return False





