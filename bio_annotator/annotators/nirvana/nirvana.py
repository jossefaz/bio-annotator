import os

from bio_annotator.annotators.annotator import AsyncAnnotator


class Nirvana(AsyncAnnotator):

    @classmethod
    @property
    def executable_bin(cls):
        return os.getenv("NIRVANA_BIN")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...