from enum import Enum
from pydantic import BaseModel, validator
from datetime import datetime


class PaymentListEnum(Enum):
    typecardbuyed = 'bycard'
    typetransferbuyed = 'bytransfer'
    typeall = 'allbuyed'
    typeinorder = 'inorder'


class PaymentListView(BaseModel):
    order_id: str
    order_summ: int
    cass_stantion_count: int
    mobile_cass_count: int
    mobile_manager_count: int
    web_manager_count: int
    order_curr_type: int
    order_date: datetime
    order_ending: datetime
    c_name: str
    c_contact_name: str
    c_phone: str
    c_email: str
    c_inn: str
    c_address: str

    @validator('order_date', 'order_ending')
    def order_date_checker(cls, arg: datetime, **kwargs):
        try:
            return arg.strftime('%Y-%m-%d')
        except Exception:
            raise Exception('ERROR')

