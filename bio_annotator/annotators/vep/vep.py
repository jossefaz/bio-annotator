import os

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.common.exceptions import AnnotatorConfigurationMissingError


class VEP(AsyncAnnotator):

    @classmethod
    @property
    def executable_bin(cls):
        return os.getenv('VEP_EXC')

    @classmethod
    @property
    def data_path(self):
        return os.getenv('VEP_DATA')

    @classmethod
    def sanity_check(cls):
        if not all([cls.executable_bin, cls.data_path, os.getenv("VEP_BIN")]):
            raise AnnotatorConfigurationMissingError(cls.__name__)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...