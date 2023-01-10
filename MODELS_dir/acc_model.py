from pydantic import BaseModel
from pydantic import Field
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
    acc_inn: str | None = Field(default=None, description="Идентификационный номер налогоплательщика")
    acc_kpp: str | None = Field(default=None, description="код причины постановки")
    acc_bik: str | None = Field(default=None, description="Бик (банковский идентификационный код)")
    acc_bank_name: str | None = Field(default=None, description="")
    acc_k_schet: str | None = Field(default=None, description="К/счет (корреспондентский счет)")
    acc_r_schet: str | None = Field(default=None, description="Р/счет (расчетный счет)")
    acc_address: str | None = Field(default=None, description="address")


class AccountRecModel(BaseModel):
    """ MODEL FOR ACCOUNT RECOVERY"""
    acc_email: str
    acc_new_pass: str


class AccountSignModel(BaseModel):
    """ MODEL FOR ACCOUNT SIGNIN """
    username: str
    password: str
