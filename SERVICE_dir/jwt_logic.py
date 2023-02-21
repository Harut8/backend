from jose import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Union, Any
from SERVICE_dir.serivce_manipulator_account import ServiceManipulatorACCOUNT


class JWTParamas:
    """
    CLASS FOR DEFAULT   SECRET KEYS
    KEYS USE FOR GENERATE JWT TOKENS
    SOLD_KEY FOR ADDING TO CLIENT ID  (SECURE)
    """
    ACCESS_SECRET_KEY = '6c8c0e67f3d1c42637603597d47ca3d8f399deec3d224356ad4cc869bd141d12'
    REFRESH_SECRET_KEY = '22e639813fd17fcc812a513a6f34218f0fe7c282d8099a92422f919dc2c97a7b'
    VERIFY_SECRET_KEY = '5df8bb072055803fe85769b4384cb184aefe216683b1c16717b02cfa6905a5fe'
    SOLD_KEY = '40cc0ff78e3fd3ce52a997e14a688273ac7b361be6eebfd617f5b3c6e73be751'
    CLIENT_ORDER_KEY = 'b8a451705f0a96c5fef4ecb677cb2e2324ebde0e439c0a1d3b811a3420537640'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 65  # 65 minutes


def create_access_token(subject_id: Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JWTParamas.ACCESS_TOKEN_EXPIRE_MINUTES)
    id_ = str(subject_id)+JWTParamas.SOLD_KEY
    to_encode = {"exp": expires_delta, "sub": id_}
    encoded_jwt = jwt.encode(to_encode, JWTParamas.ACCESS_SECRET_KEY, JWTParamas.ALGORITHM)
    ServiceManipulatorACCOUNT.redis_client.set(id_, encoded_jwt, 60*60)
    return encoded_jwt


def create_refresh_token(subject_id: Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JWTParamas.REFRESH_TOKEN_EXPIRE_MINUTES)
    id_ = str(subject_id)+JWTParamas.SOLD_KEY
    to_encode = {"exp": expires_delta, "sub": id_}
    encoded_jwt = jwt.encode(to_encode, JWTParamas.REFRESH_SECRET_KEY, JWTParamas.ALGORITHM)
    ServiceManipulatorACCOUNT.redis_client.set(id_+'refresh', encoded_jwt, 65*60)
    return encoded_jwt


def create_token_for_email_verify(subject_id: str):
    to_encode = {"sub": subject_id, "exp": datetime.utcnow() + timedelta(minutes=60)}
    encoded_jwt = jwt.encode(to_encode, JWTParamas.VERIFY_SECRET_KEY, JWTParamas.ALGORITHM)
    return encoded_jwt


class TokenPayload(BaseModel):
    """class for setting values after decoding a token"""
    exp: datetime
    sub: Any


