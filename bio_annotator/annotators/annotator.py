import asyncio
import os

from aiofiles import os as aios

from bio_annotator.schemas.variants import Variant


class AsyncAnnotator:
    def __init__(self, annotator_name, file_path=''):
        self.annotator_name = annotator_name
        self.file_path = file_path

    @classmethod
    @property
    def executable_bin(cls):
        return 'echo "ERROR: AsyncAnnotator called directly"'

    @classmethod
    def create_annotator(cls, annotator_name):
        for subclass in cls.__subclasses__():
            if subclass.__name__ == annotator_name:
                return subclass(annotator_name)
        raise ValueError(f"Invalid annotator name: {annotator_name}")

    async def __aenter__(self):
        self.annotator = self.create_annotator(self.annotator_name)
        return self.annotator

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.file_path):
            await aios.remove(self.file_path)

    async def annotate_batch(self, *args, **kwargs):
        process = await asyncio.create_subprocess_exec(
            self.executable_bin,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout, stderr

    async def annotate_one(self, variant: Variant, *args, **kwargs):
        self.file_path = variant.to_vcf()
        return await self.annotate_batch(*args, **kwargs)

