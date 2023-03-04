from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel

class TimeAndId(BaseModel):
    sub: str
    exp: datetime

def encode_client_id_for_url(client_id: str):
    from .jwt_logic import JWTParamas
    payload_of_client_order = {'sub': str(client_id), 'exp': datetime.utcnow()+timedelta(hours=6)}
    try:
        return jwt.encode(payload_of_client_order, JWTParamas.CLIENT_ORDER_KEY, JWTParamas.ALGORITHM)
    except Exception as e:
        raise Exception(e)


def decode_client_id_for_verify(client_id_token: str):
    try:
        from .jwt_logic import JWTParamas
        info_ = jwt.decode(client_id_token, JWTParamas.CLIENT_ORDER_KEY, JWTParamas.ALGORITHM)
        return TimeAndId(sub=info_["sub"], exp=info_["exp"])

    except Exception as e:
        raise Exception(e)
