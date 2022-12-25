from fastapi import FastAPI as Fapi
from fastapi import HTTPException as HTEXP
from uvicorn import run
from .api_routes import APIRoutes
from MODELS_dir import acc_model as AcRM
from SERVICE_dir.serivce_manipulator import ServiceManipulator as SMp
api = Fapi()


@api.get(APIRoutes.main)
async def start():
    return {'SERVER_STATUS': "RUNNING"}


@api.post(APIRoutes.acc_register_route)
async def acc_signin(acc_reg_model: AcRM.AccountRegModel):
    """AcRM is account registration model
    REGISTRATION API"""
    tmp = SMp.post_acc_into_temp_db(temp_acc_model=acc_reg_model)
    if tmp:
        return {"status": "REGISTERED"}
    else:
        return {"status": "ADD ERROR"}


@api.get(APIRoutes.acc_verify_route)
async def acc_verify(temp_acc_id: str, data: str):
    """VERIFY ACCOUNT SENDING EMAIL"""
    if SMp.verify_link(temp_id=int(temp_acc_id)):
        return {"status": "OK"}
    else:
        return {"status": "ERROR"}


@api.get(APIRoutes.acc_recovery_route)
async def acc_recovery(receiver_email: str):
    """SEND CODE TO EMAIL FOR RECOVERY"""
    tmp_ = SMp.recovery_code(receiver_email=receiver_email)
    if tmp_ == False:
        return {"status": "ERROR"}
    SMp.recovery_code_var = tmp_
    return {"status": "CODE SEND"}


@api.post(APIRoutes.acc_recovery_route)
async def acc_recovery(code_for_verify: str):
    """ CHECK CODE FOR RECOVERY"""
    if code_for_verify == SMp.recovery_code_var:
        SMp.recovery_code_var = None
        return {"status": "OK"}
    else:
        return {"status": "CODE ERROR"}


@api.put(APIRoutes.acc_update_pass)
async def acc_update_pass(acc_rec_model: AcRM.AccountRecModel):
    """ UPDATE PASS OF USER """
    if SMp.update_acc_pass(acc_email=acc_rec_model.acc_email, acc_pass=acc_rec_model.acc_pass):
        return {"status": "OK"}
    else:
        return {"status": "UPDATE ERROR"}


def start_server():
    """Start server"""
    run(api, host='192.168.0.104')
