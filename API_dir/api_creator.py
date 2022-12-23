from fastapi import FastAPI as Fapi
from uvicorn import run
from .api_routes import APIRoutes
from MODELS_dir.base_model import test

api = Fapi()


@api.get(APIRoutes.main)
def start():
    return {'SERVER_STATUS': "RUNNING"}


def start_server():
    """Start server"""
    run(api)
