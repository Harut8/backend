import jose.jwe
from fastapi import HTTPException, status, Depends, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .account_app import get_current_user
from .api_routes import APIRoutes
from MODELS_dir.tarif_model import (TarifToClient, PersonalTarifForClient, PersonalTarifInfo, BuyTarifeByTransfer)
from SERVICE_dir.service_manipulator_tarifes import ServiceManipulatorTARIFES as SMt
from SERVICE_dir.excel_rewriter import ExcelAnketaRewriter
from SERVICE_dir.jwt_logic import JWTParamas
"""-------------START OF TARIFES API-s-----------------"""

tarif_app = APIRouter(tags=["TARIF FUNCTIONALITY"])


async def excel_creator(order_id):
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
async def get_tarifes_for_view_route(language):
    """ GET ALL POSSIBLE TARIFES FOR VIEW """
    if language in ('ru', 'hy', 'en'):
        temp_ = SMt.get_tarifes_for_view(language=language)
        if temp_ is not None:
            return temp_
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF VIEW ERROR'})


@tarif_app.get(APIRoutes.get_personal_info_route+'{language}')
async def get_tarifes_for_view_route(language: str):
    """ GET INFO FOR TARIFES FOR PERSONAL CREATEING """
    if language.lower() in ('ru', 'hy', 'en'):
        temp_ = SMt.get_tarifes_for_personal_crateing(language)
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
    state_of_buy = SMt.post_transfer_tarif(personal_tarife)
    if state_of_buy is not None:
        excel_creator_back.add_task(excel_creator, state_of_buy["order_id"])
        #excel_creator_back.add_task(excel_sender, state_of_buy["order_id"] )
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'BUY ERROR'})


#@tarif_app.get(APIRoutes.verifyorder)




# @tarif_app.post(APIRoutes.post_tarife_to_client)
# def post_tarife_to_client(tarif_for_client: TarifToClient, access_token: OAuth2PasswordBearer = Depends(get_current_user)):
#     """ POST TARIFE FOR CLIENT """
#     if SMt.post_tarif_to_company(tarif=tarif_for_client, client_token=access_token):
#         return {"status": "TARIF ADDED TO CLIENT"}
#     raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF ADD ERROR'})


"""-------------END OF TARIFES API-s-----------------"""


#192.168.3.250
#'192.168.0.104'
#192.168.3.203