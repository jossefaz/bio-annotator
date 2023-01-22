import pytest
from httpx import AsyncClient

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.api import BaseRouteRegistry
from bio_annotator.api.annotation.v1.common.routes import RoutesRegistry
from bio_annotator.server import app

BASE_URL = BaseRouteRegistry.ANNOTATION_v1

@pytest.mark.asyncio
@pytest.mark.parametrize("annotator", AsyncAnnotator.__subclasses__())
async def test_annotation_route_will_instantiate_async_annotator(annotator, variant_schema_factory):
    annotator_name = annotator.__name__.lower()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"{BASE_URL}{RoutesRegistry.SINGLE_ANNOTATION.format(annotator_name=annotator_name)}",
                                 json=variant_schema_factory().dict())
        print()