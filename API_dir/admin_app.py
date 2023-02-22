from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette.responses import RedirectResponse
from .api_routes import APIRoutes
from MODELS_dir.admin_model import PaymentListEnum
from SERVICE_dir.service_maipulator_admin import ServiceManipulatorADMIN
admin_app = APIRouter(tags=["ADMIN PANEL FUNCTIONAL"])
from SERVICE_dir.order_verify_email_sender import send_order_verify_link_email, generate_url_for_verify_tarif


def send_verify_link_to_client(client_email, client_token):
    gen_url = generate_url_for_verify_tarif(order_id_token=client_token)
    send_order_verify_link_email(receiver_email=client_email, message=gen_url)


@admin_app.get(APIRoutes.verifypayment)
async def client_verify_payment_link(client_token: str):
    if ServiceManipulatorADMIN.verify_payment_of_client(client_token):
        return RedirectResponse('pcassa.ru')
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'SET PAYMENT ERROR'})


@admin_app.post(APIRoutes.verifyorder)
async def send_link_for_verify_payment(client_token: str, back_task: BackgroundTasks):
    info_ = ServiceManipulatorADMIN.send_email_for_order_verify(client_token)
    if info_:
        back_task.add_task(send_verify_link_to_client, info_, client_token)
        return {"status": "ok", "message": "VERIFY LINK SENDED"}
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'SEND EMAIL ERROR'})


@admin_app.get(APIRoutes.getpaymentlist)
async def admin_get_payment_list(type_of_payment: PaymentListEnum):
    info_ = ServiceManipulatorADMIN.get_payment_list(type_of_payment)
    if info_ is not None:
        return info_
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'GET PAYMENT ERROR'})