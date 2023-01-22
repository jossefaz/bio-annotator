from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from starlette import status

from bio_annotator.api.annotation.v1.common.dependencies import validate_annotator_name
from bio_annotator.api.annotation.v1.common.dependencies import validate_variant_payload
from bio_annotator.api.annotation.v1.common.routes import RoutesRegistry
from bio_annotator.schemas.variant import Variant
from bio_annotator.api.annotation.v1.controller import annotate_variant

annotation_router_v1 = APIRouter()

ANNOTATION_ROUTES = RoutesRegistry()


@annotation_router_v1.post(ANNOTATION_ROUTES.SINGLE_ANNOTATION, status_code=status.HTTP_200_OK)
async def annotate_single_variant(annotator_name: str = Depends(validate_annotator_name), payload: Variant = Depends(validate_variant_payload)):
    return await annotate_variant(annotator_name, payload)
