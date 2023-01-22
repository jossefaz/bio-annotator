import os

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.common.exceptions import AnnotatorConfigurationMissingError


class VEP(AsyncAnnotator):

    def __init__(self, annotator_name):
        super().__init__(annotator_name)
        self._human_reference = 'GRCh37'
        self.output_file = ''
        self.input_file = ''

    @classmethod
    @property
    def executable(cls):
        return os.getenv('VEP_EXC')

    @classmethod
    @property
    def bin(cls):
        return os.getenv('VEP_BIN')

    @classmethod
    @property
    def data_path(self):
        return os.getenv('VEP_DATA')

    @classmethod
    def sanity_check(cls):
        if not all([cls.executable, cls.data_path, cls.bin]):
            raise AnnotatorConfigurationMissingError(cls.__name__)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...