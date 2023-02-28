from fastapi import APIRouter, HTTPException
from .api_routes import APIRoutes
from MODELS_dir.license_model import CheckLicenseModel, AddLicenseModel
from SERVICE_dir.service_maipulator_license import ServiceManipulatorLICENSE


license_app = APIRouter(tags=['LICENSE FUNCTIONALITY'])


@license_app.post(APIRoutes.addlicense)
async def add_license(add_info: AddLicenseModel):
    info_ = ServiceManipulatorLICENSE.add_license(add_info)
    if info_ is not None:
        return info_
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'ADD LICENSE ERROR'})


@license_app.post(APIRoutes.checklicense)
async def check_license(check_info: CheckLicenseModel):
    ...
