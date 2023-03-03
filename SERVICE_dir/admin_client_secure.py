
from jose import jwt


def encode_client_id_for_url(client_id: str):
    from .jwt_logic import JWTParamas
    payload_of_client_order = {'sub': str(client_id)}
    try:
        return jwt.encode(payload_of_client_order, JWTParamas.CLIENT_ORDER_KEY, JWTParamas.ALGORITHM)
    except Exception as e:
        raise Exception(e)


def decode_client_id_for_verify(client_id_token: str):
    try:
        from .jwt_logic import JWTParamas
        return jwt.decode(client_id_token, JWTParamas.CLIENT_ORDER_KEY, JWTParamas.ALGORITHM)["sub"]
    except Exception as e:
        raise Exception(e)