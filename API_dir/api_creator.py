from fastapi import FastAPI as Fapi
from fastapi import HTTPException as HTEXP
from uvicorn import run
from .api_routes import APIRoutes
from MODELS_dir import acc_model as AcRM
from SERVICE_dir.serivce_manipulator_account import ServiceManipulatorACCOUNT as SMp
from SERVICE_dir.service_manipulator_tarifes import ServiceManipulatorTARIFES as SMt
from fastapi.middleware.cors import CORSMiddleware

api = Fapi()

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get(APIRoutes.main)
async def start():
    return {'SERVER_STATUS': "RUNNING"}


""" --------------START ACCOUNT API-s---------------
--- account signup 
--- account signin
--- account verify
--- account recovery code send
--- account recovery code check
--- account new password setting
"""


@api.post(APIRoutes.acc_register_route)
async def acc_signup(acc_reg_model: AcRM.AccountRegModel):
    """AcRM is account registration model
    REGISTRATION API"""
    tmp = SMp.post_acc_into_temp_db(temp_acc_model=acc_reg_model)
    if tmp:
        return {"status": "REGISTERED"}
    else:
        return {"status": "ERROR"}


@api.get(APIRoutes.acc_verify_route)
async def acc_verify(temp_acc_id: str, data: str):
    """VERIFY ACCOUNT SENDING EMAIL"""
    temp_ = SMp.verify_link(temp_id=int(temp_acc_id))
    if temp_[0]:
        print(temp_)
        if SMp.send_unique_code_and_pass(acc_unique_id=temp_[1], acc_email=temp_[2]):
            return {"status": 'VERIFYING SUCCESS'}
    else:
        return {"status": "ERROR"}


@api.get(APIRoutes.acc_recovery_route)
async def acc_recovery(receiver_email: str):
    """SEND CODE TO EMAIL FOR RECOVERY
        GET recovery code and save it"""
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
        return {"status": "VERIFY CODE TRUE"}
    else:
        return {"status": "CODE ERROR"}


@api.put(APIRoutes.acc_update_pass)
async def acc_update_pass(acc_rec_model: AcRM.AccountRecModel):
    """ UPDATE PASS OF USER """
    if SMp.update_acc_pass(acc_email=acc_rec_model.acc_email, acc_new_pass=acc_rec_model.acc_new_pass):
        return {"status": "UPDATE PASSWORD IS SUCCESSFUL"}
    else:
        return {"status": "UPDATE ERROR"}


@api.post(APIRoutes.acc_login_route)
async def signin_acc(acc_sign_model: AcRM.AccountSignModel):
    """ SIGNIN CHECKING RETURN VALUES """
    check_ = SMp.signin_acc(acc_email=acc_sign_model.acc_email, acc_pass=acc_sign_model.acc_pass)
    if check_[0]:
        return check_[1]
    else:
        return {"status": "SIGNIN ERROR"}


"""-------------END OF ACCOUNT API-s-----------------"""


"""-------------START OF TARIFES API-s-----------------"""


@api.get(APIRoutes.get_tarifes_for_view_route)
def get_tarifes_for_view_route():
    temp_ = SMt.get_tarifes_for_view()
    if temp_[0]:
        return temp_[1]
    else:
        return {"status": "ERROR GETTING TARIFES"}

def start_server():
    """Start server"""
    run(api,)


#192.168.3.250
#'192.168.0.104'