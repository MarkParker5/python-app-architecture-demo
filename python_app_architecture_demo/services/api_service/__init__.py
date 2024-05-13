from threading import Thread
import uvicorn
from fastapi import FastAPI
from ..abstract_service import AbstractService
from api import get_app


class ApiService(AbstractService):

    def __init__(self, app: FastAPI):
        super().__init__()
        self.app = app

    # override
    def main_loop(self):
        uvicorn.run(self.app)

    def _loop_iteration(self): pass # don't need it here, because we run the FastAPI app in the main loop
