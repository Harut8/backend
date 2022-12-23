from fastapi import FastAPI as Fapi
from fastapi import HTTPException as HTEXP
from uvicorn import run
from .api_routes import APIRoutes
from MODELS_dir import acc_reg_model as AcRM

api = Fapi()


@api.get(APIRoutes.main)
async def start():
    return {'SERVER_STATUS': "RUNNING"}


@api.post(APIRoutes.free_acc_reg_route)
async def acc_signin(acc_reg_model: AcRM.FreeAccountRegModel):
    """AcRM is account registration model
    FREE REGISTRATION"""
    return {"status": "ok"}


@api.post(APIRoutes.free_acc_reg_route)
async def acc_signin(acc_reg_model: AcRM.BusinessAccountRegModel):
    """AcRM is account registration model
    BUSINESS REGISTRATION"""
    return {"status": "ok"}


def start_server():
    """Start server"""
    run(api)
