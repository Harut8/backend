from fastapi import APIRouter
from api_routes import APIRoutes

admin_app = APIRouter(tags=["ADMIN PANEL FUNCTIONAL"])


@admin_app.post(APIRoutes.ispayed)
async def admin_verify_payment():
    ...
