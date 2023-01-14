from jose import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Union, Any
from SERVICE_dir.serivce_manipulator_account import ServiceManipulatorACCOUNT


class JWTParamas:
    SECRET_KEY = '6c8c0e67f3d1c42637603597d47ca3d8f399deec3d224356ad4cc869bd141d12'
    REFRESH_SECRET_KEY = '22e639813fd17fcc812a513a6f34218f0fe7c282d8099a92422f919dc2c97a7b'
    VERIFY_SECRET_KEY = '5df8bb072055803fe85769b4384cb184aefe216683b1c16717b02cfa6905a5fe'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes


def create_access_token(subject_id: Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JWTParamas.ACCESS_TOKEN_EXPIRE_MINUTES)
    id_ = str(subject_id)
    to_encode = {"exp": expires_delta, "sub": id_}
    encoded_jwt = jwt.encode(to_encode, JWTParamas.SECRET_KEY, JWTParamas.ALGORITHM)
    ServiceManipulatorACCOUNT.ACCESS_TOKEN_FOR_CHECK = encoded_jwt
    ServiceManipulatorACCOUNT.ACCOUNT_ID_FOR_TOKEN = id_
    return encoded_jwt


def create_token_for_email_verify(subject_id: str):
    to_encode = {"sub": subject_id}
    encoded_jwt = jwt.encode(to_encode, JWTParamas.VERIFY_SECRET_KEY, JWTParamas.ALGORITHM)
    return encoded_jwt



def create_refresh_token(subject_id: Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JWTParamas.REFRESH_TOKEN_EXPIRE_MINUTES)
    id_ = str(subject_id)
    to_encode = {"exp": expires_delta, "sub": id_}
    encoded_jwt = jwt.encode(to_encode, JWTParamas.REFRESH_SECRET_KEY, JWTParamas.ALGORITHM)
    ServiceManipulatorACCOUNT.REFRESH_TOKEN_FOR_CHECK = encoded_jwt
    ServiceManipulatorACCOUNT.ACCOUNT_ID_FOR_TOKEN = id_
    return encoded_jwt


def change_secret_keys():
    from secrets import token_hex
    JWTParamas.SECRET_KEY, JWTParamas.REFRESH_SECRET_KEY = token_hex(32), token_hex(32)


class TokenPayload(BaseModel):
    exp: datetime
    sub: Any


