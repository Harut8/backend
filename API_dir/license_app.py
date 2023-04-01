from fastapi import APIRouter, HTTPException
from .api_routes import APIRoutes
from MODELS_dir.license_model import CheckLicenseModel, AddLicenseModel, GetLicenseType, GetPortForSuro
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
    """if true then license is active"""
    info_ = ServiceManipulatorLICENSE.check_license(check_info)
    print(info_)
    if info_ is not None:
        return info_
    raise HTTPException(status_code=404, detail='ERROR', headers={'status': 'LICENSE TIME ERROR'})


@license_app.post(APIRoutes.licensetype)
async def get_license_type(license_type: GetLicenseType):
    info_ = ServiceManipulatorLICENSE.get_license_type(license_type.license_key)
    if info_ is not None:
        return info_
    raise HTTPException(status_code=400, detail='ERROR', headers={'status': 'LICENSE ERROR'})

@license_app.post('/port_for_suro')
async def get_port_for_suro(u_lc_info: GetPortForSuro):
    info_ = ServiceManipulatorLICENSE.get_port_for_suro(u_lc_info.u_id, u_lc_info.lc_key)
    if info_ is not None:
        return {"port": info_}
    raise HTTPException(status_code=400, detail='ERROR', headers={'status': 'LICENSE ERROR'})
