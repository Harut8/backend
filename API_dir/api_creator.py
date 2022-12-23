from fastapi import FastAPI as Fapi
from fastapi import HTTPException as HTEXP
from uvicorn import run
from .api_routes import APIRoutes
from MODELS_dir import acc_reg_model as AcRM
from SERVICE_dir.serivce_manipulator import ServiceManipulator as SMp
api = Fapi()


@api.get(APIRoutes.main)
async def start():
    return {'SERVER_STATUS': "RUNNING"}


@api.post(APIRoutes.acc_reg_route)
async def acc_signin(acc_reg_model: AcRM.AccountRegModel):
    """AcRM is account registration model
    REGISTRATION API"""
    tmp = SMp.post_acc_into_temp_db(temp_acc_model=acc_reg_model)
    if tmp:
        return {"status": "REGISTERED"}
    else:
        return {"status": "ADD ERROR"}

@api.post(APIRoutes.acc_verify_route)
async def acc_verify(temp_acc_id, data):
    print(temp_acc_id)
def start_server():
    """Start server"""
    run(api)
