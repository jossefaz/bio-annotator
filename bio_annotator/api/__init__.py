from fastapi import FastAPI

from bio_annotator.api.annotation.v1.router import annotation_router_v1
from dataclasses import dataclass



@dataclass
class _BaseRouteRegistry:
    ANNOTATION_v1 = 'annotation'

    def __getattribute__(self, item):
        resource_name = object.__getattribute__(self, item)
        version = item.split('_')[1]
        return f"/api/{resource_name}/{version}"


BaseRouteRegistry = _BaseRouteRegistry()


def setup_resources(app_: FastAPI):
    app_.include_router(annotation_router_v1, prefix=BaseRouteRegistry.ANNOTATION_v1)