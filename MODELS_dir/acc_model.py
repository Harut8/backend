from enum import Enum
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import Field, validator, ValidationError, validate_email
import email_validator
import re
"""
HERE IS MODELS FOR WORKING WITH ACCOUNT
---ACCOUNT REGISTRATION
---ACCOUNT LOGIN
---ACCOUNT RECOVERY
"""


class AccountRegModel(BaseModel):
    """Model for registration fields
    IN BUSINESS REG YOU MUST ADD
    acc_inn
    acc_kpp
    acc_bik
    acc_bank_name
    acc_k_schet
    acc_r_schet
    acc_address"""
    acc_contact_name: str
    acc_org_name: str
    acc_email: str
    acc_pass: str
    acc_phone: str
    acc_address: str | None
    acc_country: int
    acc_inn: str | None = Field(default=None, description="Идентификационный номер налогоплательщика", regex=r'\d{1,15}')
    acc_kpp: str | None = Field(default=None, description="код причины постановки", regex=r'\d{1,15}')
    acc_bik: str | None = Field(default=None, description="Бик (банковский идентификационный код)", regex=r'\d{1,15}')
    acc_bank_name: str | None = Field(default=None, description="", regex=r'\w{1,40}')
    acc_k_schet: str | None = Field(default=None, description="К/счет (корреспондентский счет)", regex=r'\d{20}')
    acc_r_schet: str | None = Field(default=None, description="Р/счет (расчетный счет)", regex=r'\d{20}')

    @validator('acc_phone')
    def check_acc_phone(cls, acc_phone):
        try:
            if re.match(r'\+374\d{8}', acc_phone):
                return acc_phone
        except Exception:
            raise ValidationError('PHONE ERROR')

    @validator('acc_email')
    def check_acc_email(cls, acc_email):
        try:
            if validate_email(acc_email):
                return acc_email
        except Exception:
            raise ValidationError('EMAIL ERROR')

    @validator('acc_pass')
    def check_acc_pass(cls, acc_pass):
        try:
            ln = len(acc_pass)
            if ln >= 4 or ln <= 40:
                return acc_pass
            raise ValidationError('PASSWORD ERROR')
        except Exception:
            raise ValidationError('PASSWORD ERROR')


class AccountRecModel(BaseModel):
    """ MODEL FOR ACCOUNT RECOVERY"""
    acc_email: str
    acc_new_pass: str


class AccountVerifyModel(BaseModel):
    receiver_email: str
    code_for_verify: int

    @validator('code_for_verify')
    def check_verify_type(cls, code):
        try:
            if isinstance(code, int) and len(str(code)) == 9:
                return code
            raise ValidationError('CODE ERROR')
        except Exception:
            raise ValidationError('CODE ERROR')

    @validator('receiver_email')
    def check_acc_email(cls, acc_email):
        try:
            if validate_email(acc_email):
                return acc_email
        except Exception:
            raise ValidationError('EMAIL ERROR')


class AccRecoveryEmail(BaseModel):
    receiver_email: str

    @validator('receiver_email')
    def check_acc_email(cls, acc_email):
        try:
            if validate_email(acc_email):
                return acc_email
        except Exception:
            raise ValidationError('EMAIL ERROR')


class AccountSignModel(BaseModel):
    """ MODEL FOR ACCOUNT SIGNIN """
    username: str
    password: str


class AccountViewInnerModel(BaseModel):
    t_id: int
    t_name: str | None
    end_license: Any
    order_state: bool
    #links: list


class AccountViewModel(BaseModel):
    c_id: int
    c_unique_id: str
    c_name: str
    c_contact_name: str
    c_phone: str
    c_email: str
    tarif_list: list[AccountViewInnerModel]


class Refresh(BaseModel):
    refresh_token: str
class Language(Enum):
    ru = 'ru'
    en = 'en'
    hy = 'hy'