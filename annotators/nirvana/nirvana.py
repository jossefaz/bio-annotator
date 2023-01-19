from annotators.annotator import AsyncAnnotator


class Nirvana(AsyncAnnotator):

    @classmethod
    @property
    def executable_bin(cls):
        return "echo"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...