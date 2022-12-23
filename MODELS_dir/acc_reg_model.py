from pydantic import BaseModel


class FreeAccountRegModel(BaseModel):
    """Model for FREE registration fields"""
    acc_name: str | None
    acc_org_name: str | None
    acc_email: str | None
    acc_pass: str | None
    acc_phone: str | None


class BusinessAccountRegModel(BaseModel):
    """Model for BUSINESS registration fields"""
    acc_name: str | None
    acc_org_name: str | None
    acc_email: str | None
    acc_pass: str | None
    acc_phone: str | None
