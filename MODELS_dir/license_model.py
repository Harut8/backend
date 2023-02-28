from pydantic import BaseModel, Field
from enum import Enum


# class DeviceCodes(Enum):
#     cass_stantion = 1
#     mobile_cass = 2
#     web_manager = 3
#     mobile_manager = 4


class AddLicenseModel(BaseModel):
    unique_code: int
    device_code: str
    product_id: int = Field(gt=0, le=4)


class CheckLicenseModel(BaseModel):
    license_key: str
    device_code: str
