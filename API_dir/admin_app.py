from fastapi import APIRouter, HTTPException
from .api_routes import APIRoutes
from MODELS_dir.admin_model import PaymentListEnum
from SERVICE_dir.service_maipulator_admin import ServiceManipulatorADMIN
admin_app = APIRouter(tags=["ADMIN PANEL FUNCTIONAL"])


@admin_app.post(APIRoutes.ispayed)
async def admin_verify_payment(client_token: str):
    if ServiceManipulatorADMIN.verify_payment_of_client(client_token):
        return {"status": "ok", "message": "payment is authorized"}
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'SET PAYMENT ERROR'})


@admin_app.get(APIRoutes.getpaymentlist)
async def admin_get_payment_list(type_of_payment: PaymentListEnum):
    info_ = ServiceManipulatorADMIN.get_payment_list(type_of_payment)
    if info_ is not None:
        return info_
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'GET PAYMENT ERROR'})
