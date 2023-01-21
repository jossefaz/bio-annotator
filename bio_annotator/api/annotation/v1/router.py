from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from bio_annotator.api.annotation.v1.common.dependencies import validate_variant_payload
from bio_annotator.api.annotation.v1.common.routes import RoutesRegistry
from bio_annotator.schemas.variant import Variant

annotation_router_v1 = APIRouter()

ANNOTATION_ROUTES = RoutesRegistry()


@annotation_router_v1.post(ANNOTATION_ROUTES.SINGLE_ANNOTATION, status_code=status.HTTP_200_OK)
def annotate_single_variant(payload: Variant = Depends(validate_variant_payload)):
    return payload.variant_type
