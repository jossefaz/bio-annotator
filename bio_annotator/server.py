import os

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from bio_annotator.api import setup_resources
from bio_annotator.common.exceptions import BioAnnotatorError


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(BioAnnotatorError)
    async def custom_exception_handler(request: Request, exc: BioAnnotatorError):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

def init_file_caching():
    # Check if the directory path exists
    if not os.path.exists('cache'):
        # Create the directory path
        os.makedirs('cache')


def create_app() -> FastAPI:
    app_ = FastAPI()
    setup_resources(app_=app_)
    init_listeners(app_=app_)
    init_file_caching()
    return app_


app = create_app()

if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=5000, reload=True)