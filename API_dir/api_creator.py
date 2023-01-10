from fastapi import FastAPI
from .account_app import account_app
from .tarif_app import tarif_app
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware

main_app = FastAPI()
main_app.include_router(account_app)
main_app.include_router(tarif_app)

origins = ["*"]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_app.get('/')
def main_route():
    return {'status': 'SERVER RUNNING'}


def start_server():
    """Start server"""
    run(main_app)


#192.168.3.250
#'192.168.0.104'
#192.168.3.203