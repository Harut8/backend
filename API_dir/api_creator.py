from fastapi import FastAPI, Request

from .account_app import account_app
from .tarif_app import tarif_app
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
from configparser import ConfigParser

conf = ConfigParser()
conf.read('API_dir/API_CONFIG.ini')
host = conf.get('API', 'host')


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


@main_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    x = request.query_params
    print(request.url)
    print(request.query_params)
    response = await call_next(request)
    return response


def start_server():
    """Start server"""
    run(main_app, host=host)


#192.168.3.250
#'192.168.0.104'
#192.168.3.203