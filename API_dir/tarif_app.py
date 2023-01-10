from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .account_app import get_current_user
from .api_routes import APIRoutes
from MODELS_dir.tarif_model import (TarifToClient, PersonalTarifForClient)
from SERVICE_dir.service_manipulator_tarifes import ServiceManipulatorTARIFES as SMt


"""-------------START OF TARIFES API-s-----------------"""

tarif_app = APIRouter(tags=["TARIF FUNCTIONALITY"])


@tarif_app.get(APIRoutes.get_tarifes_for_view_route)
def get_tarifes_for_view_route(access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    """ GET ALL POSSIBLE TARIFES FOR VIEW """
    temp_ = SMt.get_tarifes_for_view()
    if temp_[0]:
        return temp_[1]
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF VIEW ERROR'})


@tarif_app.post(APIRoutes.post_tarife_to_client)
def post_tarife_to_client(tarif_for_client: TarifToClient, access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    """ POST TARIFE FOR CLIENT """
    if SMt.post_tarif_to_company(tarif=tarif_for_client):
        return {"status": "TARIF ADDED TO CLIENT"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF ADD ERROR'})


"""-------------END OF TARIFES API-s-----------------"""


#192.168.3.250
#'192.168.0.104'
#192.168.3.203