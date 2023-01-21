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


def create_app() -> FastAPI:
    app_ = FastAPI()
    setup_resources(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()
