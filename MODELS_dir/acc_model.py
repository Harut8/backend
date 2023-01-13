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
    acc_contact_name: str | None
    acc_org_name: str | None
    acc_email: str | None
    acc_pass: str | None
    acc_phone: str | None
    acc_address: str | None
    acc_inn: str | None = Field(default=None, description="Идентификационный номер налогоплательщика")
    acc_kpp: str | None = Field(default=None, description="код причины постановки")
    acc_bik: str | None = Field(default=None, description="Бик (банковский идентификационный код)")
    acc_bank_name: str | None = Field(default=None, description="")
    acc_k_schet: str | None = Field(default=None, description="К/счет (корреспондентский счет)")
    acc_r_schet: str | None = Field(default=None, description="Р/счет (расчетный счет)")

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
            if ln>=4 or ln<=40:
                return acc_pass
            raise ValidationError('PASSWORD ERROR')
        except Exception:
            raise ValidationError('PASSWORD ERROR')


class AccountRecModel(BaseModel):
    """ MODEL FOR ACCOUNT RECOVERY"""
    acc_email: str
    acc_new_pass: str


class AccountSignModel(BaseModel):
    """ MODEL FOR ACCOUNT SIGNIN """
    username: str
    password: str
