from fastapi import FastAPI, Request
from .account_app import account_app
from .tarif_app import tarif_app
#from .admin_app import admin_app
from .license_app import license_app
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
from configparser import ConfigParser
from SERVICE_dir.serivce_manipulator_account import ServiceManipulatorACCOUNT as SMa
from DB_dir.db_connection import DatabaseConnection


conf = ConfigParser()
conf.read('API_dir/API_CONFIG.ini')
host = conf.get('API', 'host')
#main_app = FastAPI(docs_url=None, redoc_url=None)
main_app = FastAPI()
main_app.include_router(account_app)
main_app.include_router(tarif_app)
#main_app.include_router(admin_app)
main_app.include_router(license_app)

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


@main_app.on_event('shutdown')
def end_api_background_tasks():
    # if SMa.TOKEN_THREAD1 is not None and SMa.TOKEN_THREAD2 is not None:
    #     SMa.TOKEN_THREAD1.cancel()
    #     SMa.TOKEN_THREAD2.cancel()
    DatabaseConnection.close()


@main_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    x = request.query_params
    #print(await request.body())
    #print(await request.body())
    response = await call_next(request)
    return response


def start_server():
    """Start server"""
    run(main_app, host=host, port=8000)


#192.168.3.250
#'192.168.0.104'
#192.168.3.203
