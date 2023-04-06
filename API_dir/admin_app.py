from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from starlette import status
from starlette.responses import RedirectResponse

from SERVICE_dir.jwt_logic import JWTParamas, TokenPayload, create_access_token, create_refresh_token
from .api_routes import APIRoutes
from MODELS_dir.admin_model import PaymentListEnum
from SERVICE_dir.service_maipulator_admin import ServiceManipulatorADMIN
admin_app = APIRouter(tags=["ADMIN PANEL FUNCTIONAL"])
from SERVICE_dir.order_verify_email_sender import send_order_verify_link_email, generate_url_for_verify_tarif
from SERVICE_dir.links_for_download_send import send_download_links


admin_oauth = OAuth2PasswordBearer(
        tokenUrl="/admin/signin",
        scheme_name="JWT"
    )


async def get_admin_login(token: str = Depends(admin_oauth)):
    """CHECK INVALID TOKENS
       CHECK EXPIRED TOKENS"""
    try:
        payload = jwt.decode(
            token, JWTParamas.ACCESS_SECRET_KEY, algorithms=[JWTParamas.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        print(token_data)
        if token_data.exp < datetime.utcnow().replace(tzinfo=timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ERROR",
                headers={"WWW-Authenticate": "EXPIRED TIME"},
            )
        return token_data.sub
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERROR",
            headers={"WWW-Authenticate": "Bearer"},
        )


@admin_app.post('/admin/signin')
async def signin(admin_sign_model: OAuth2PasswordRequestForm = Depends()):
    check_ = ServiceManipulatorADMIN.signin_admin(
        admin_login=admin_sign_model.username,
        admin_password=admin_sign_model.password)
    print(check_)
    if check_:
        ACCESS_TOKEN = create_access_token(check_["admin_login"], expires_delta=timedelta(hours=10))
        REFRESH_TOKEN = create_refresh_token(check_["admin_login"], expires_delta=timedelta(hours=10))
        return {
            "access_token": ACCESS_TOKEN,
            "refresh_token": REFRESH_TOKEN
        }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ERROR")


def send_link_for_download(order_id_token, email_):
    print('mtav')
    info_ = ServiceManipulatorADMIN.links_for_downloading(order_id_token)
    send_download_links(receiver_email=email_, message=info_)


def send_verify_link_to_client(client_email, client_token):
    gen_url = generate_url_for_verify_tarif(order_id_token=client_token)
    send_order_verify_link_email(receiver_email=client_email, message=gen_url)


@admin_app.get(APIRoutes.verifypayment)
async def client_verify_payment_link(client_token: str, send_link: BackgroundTasks):
    #send_link.add_task(send_link_for_download, client_token)
    if ServiceManipulatorADMIN.verify_payment_of_client(client_token):
        email_ = ServiceManipulatorADMIN.send_email_for_order_verify(client_token)
        if email_ is not None:
            send_link.add_task(send_link_for_download, client_token, email_)
            return RedirectResponse('http://pcassa.ru/')
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'SET PAYMENT ERROR'})


@admin_app.post(APIRoutes.verifyorder)
async def send_link_for_verify_payment(client_token: str,
                                       back_task: BackgroundTasks,
                                       admin_login=Depends(get_admin_login)):
    if ServiceManipulatorADMIN.check_permission(admin_login.replace(JWTParamas.SOLD_KEY, '')):
        info_ = ServiceManipulatorADMIN.send_email_for_order_verify(client_token)
        if info_:
            back_task.add_task(send_verify_link_to_client, info_, client_token)
            return {"status": "ok", "message": "VERIFY LINK SENDED"}
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'SEND EMAIL ERROR'})


@admin_app.get(APIRoutes.getpaymentlist)
async def admin_get_payment_list(type_of_payment: PaymentListEnum, admin_login=Depends(get_admin_login)):
    info_ = ServiceManipulatorADMIN.get_payment_list(type_of_payment)
    if info_ is not None:
        return info_
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'GET PAYMENT ERROR'})


@admin_app.get('/admin/company')
async def get_companies(q='', admin_login=Depends(get_admin_login)):
    info_ = ServiceManipulatorADMIN.get_companies(
        admin_login=admin_login.replace(JWTParamas.SOLD_KEY, ''),
        search=q)
    if info_:
        return info_
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'ERROR'})


@admin_app.get('/admin/company/{company_id}')
async def get_company_and_tarif(company_id: int, admin_login=Depends(get_admin_login)):
    info_ = ServiceManipulatorADMIN.get_company_and_tarif_by_id(company_id)
    if info_:
        return info_
    raise HTTPException(status_code=400, detail='ERROR', headers={'status': 'ERROR'})


@admin_app.post('/admin/company/tarif/{order_id}')
async def block_tarif_for_company(order_id: int, admin_login=Depends(get_admin_login)):
    if ServiceManipulatorADMIN.block_tarif_for_company(order_id, admin_login.replace(JWTParamas.SOLD_KEY, '')):
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail='ERROR', headers={'status': 'ERROR'})