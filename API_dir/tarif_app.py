import jose.jwe
import requests
from fastapi import HTTPException, status, Depends, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from SERVICE_dir.admin_client_secure import encode_client_id_for_url
from SERVICE_dir.service_maipulator_admin import ServiceManipulatorADMIN
from .account_app import get_current_user
from .admin_app import send_verify_link_to_client
from .api_routes import APIRoutes
from MODELS_dir.acc_model import Language
from MODELS_dir.tarif_model import (TarifToClient, PersonalTarifForClient, PersonalTarifInfo, BuyTarifeByTransfer, TarifDetailsGet)
from SERVICE_dir.service_manipulator_tarifes import ServiceManipulatorTARIFES as SMt
from SERVICE_dir.excel_rewriter import ExcelAnketaRewriter
from SERVICE_dir.jwt_logic import JWTParamas
"""-------------START OF TARIFES API-s-----------------"""

tarif_app = APIRouter(tags=["TARIF FUNCTIONALITY"])


def excel_creator(order_id):
    #avelcanel api exceli sarqelu hmar
    info_1 = SMt.get_info_for_excel(order_id)
    info_2 = SMt.get_tarifes_for_personal_crateing(language='ru')
    if info_1 and info_2 is not None:
        if ExcelAnketaRewriter.set_all_attributes(info_1, info_2):
            if SMt.send_link_excel_download(order_id):
                print("EMAIL EXCEL")
            raise Exception("EXCEL SENDING ERROR")
    raise Exception("EXCEL ERROR")


#access_token: OAuth2PasswordBearer = Depends(get_current_user)
@tarif_app.get(APIRoutes.get_tarifes_for_view_route+'{language}')
async def get_tarifes_for_view_route(language: Language):
    """ GET ALL POSSIBLE TARIFES FOR VIEW """
    temp_ = SMt.get_tarifes_for_view(language=language.value)
    if temp_ is not None:
        return temp_
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF VIEW ERROR'})


@tarif_app.get(APIRoutes.get_personal_info_route+'{language}')
async def get_tarifes_for_view_route(language: Language):
    """ GET INFO FOR TARIFES FOR PERSONAL CREATEING """
    temp_ = SMt.get_tarifes_for_personal_crateing(language.value)
    if temp_ is not None:
        return temp_
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF VIEW ERROR'})


@tarif_app.post(APIRoutes.getallsumm)
async def get_tarifes_all_summ(personal_tarife: PersonalTarifInfo,
                         access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    summ_of_tarife = SMt.check_summ_and_return(personal_tarife)
    if summ_of_tarife is not None:
        return {"summ": summ_of_tarife}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'SUMM ERROR'})


@tarif_app.post(APIRoutes.buybytransfer)
async def buy_tarife_by_transfer(personal_tarife: BuyTarifeByTransfer,
                           excel_creator_back: BackgroundTasks,
                           access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    #personal_tarife.company_id = jose.jwe.decrypt(access_token, JWTParamas.ACCESS_SECRET_KEY)
    personal_tarife.client_token = access_token
    state_of_buy = SMt.post_transfer_tarif(personal_tarife, valute=0)
    if state_of_buy is not None:
        excel_creator_back.add_task(excel_creator, state_of_buy["order_id"])
        #excel_creator_back.add_task(excel_sender, state_of_buy["order_id"] )
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'BUY ERROR'})


@tarif_app.post(APIRoutes.free)
async def buy_free_tarif(personal_tarife: BuyTarifeByTransfer,
                         back_task: BackgroundTasks,
                         access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    personal_tarife.client_token = access_token
    state_of_buy = SMt.post_transfer_tarif(personal_tarife, valute=2)
    if state_of_buy is not None:
        client_token = encode_client_id_for_url(state_of_buy["order_id"])
        info_ = ServiceManipulatorADMIN.send_email_for_order_verify(client_token)
        if info_:
            back_task.add_task(send_verify_link_to_client, info_, client_token)
            return {"status": "ok", "message": "VERIFY LINK SENDED"}
        return {"status": "ok", "message": "VERIFY LINK NOT SENDED"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'BUY ERROR'})


@tarif_app.get("/checkpayment")
async def check_payment(orderId: str, client_token: str, lang: str, back_task: BackgroundTasks):
    checking = requests.post(
        f"""https://alfa.rbsuat.com/payment/rest/getOrderStatusExtended.do?orderId={orderId}&token=snsf2mafqocsnn25tbdhcve8sj""")
    checking = checking.json()
    print(checking)
    if checking["orderStatus"] == 2 and checking[" errorCode"] == 0:
        print(checking)
        info_ = 1
        # info_ = ServiceManipulatorADMIN.send_email_for_order_verify(client_token, "pre")
        if info_:
            # back_task.add_task(send_verify_link_to_client, info_, client_token)
            return {"status": "ok", "message": "VERIFY LINK SENDED"}
    else:
        raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'BUY ERROR'})


@tarif_app.post(APIRoutes.buybycard)
async def buy_tarife_by_card(
        personal_tarife: BuyTarifeByTransfer,
        access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    # if bank works okay
    personal_tarife.client_token = access_token
    state_of_buy = SMt.post_transfer_tarif(item=personal_tarife, valute=1, type_of="pre")
    if not state_of_buy:
        print(999)
        raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'BUY ERROR'})
    order_id = state_of_buy["order_id"]
    client_token = encode_client_id_for_url(order_id)
    url_for_return = f"""https://alfa.rbsuat.com/payment/rest/register.do?token=snsf2mafqocsnn25tbdhcve8sj&orderNumber={order_id}&amount={personal_tarife.order_summ}&returnUrl=http%3A%2F%2F192.168.0.102%3A8000%2Fcheckpayment%3Fclient_token%3D{client_token}"""
    bank_check = requests.post(url_for_return)
    bank_check = bank_check.json()
    state_of_buy = SMt.update_bank_id(order_id=order_id, bank_order_id=bank_check["orderId"])
    personal_tarife.client_token = access_token

    if state_of_buy is not None:
        # 127.0.0.1/checkpayment?order_id={bank_check["orderId"]}&client_token={access_token}
        # client_token = encode_client_id_for_url(state_of_buy["order_id"])
        print(bank_check["formUrl"])
        return RedirectResponse(bank_check["formUrl"])
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'BUY ERROR'})


@tarif_app.post(APIRoutes.acc_get_tarif_details)
async def get_tarif_details(tarif_id_body: TarifDetailsGet,
                            access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    print(tarif_id_body)
    info_ = SMt.get_tarif_details(tarif_id_body.tarif_id)
    if info_ is not None:
        return info_
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'DETAIL ERROR'})


@tarif_app.post(APIRoutes.changetocard)
async def change_valute_to_card(
        tarif_id_model: TarifDetailsGet,
        back_task: BackgroundTasks,
        access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    #if bank works okay
    info_ = SMt.change_valute_to_card(tarif_id_model.tarif_id)
    if info_ is not None:
        client_token = encode_client_id_for_url(info_)
        info_ = ServiceManipulatorADMIN.send_email_for_order_verify(client_token)
        if info_:
            back_task.add_task(send_verify_link_to_client, info_, client_token)
            return {"status": "ok"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'CHANGING ERROR'})


"""-------------END OF TARIFES API-s-----------------"""


#192.168.3.250
#'192.168.0.104'
#192.168.3.203
