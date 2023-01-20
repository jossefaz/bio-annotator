import asyncio
import os

from schemas.variants import Variant


class AsyncAnnotator:
    def __init__(self, annotator_name, variant: Variant, file_path=None):
        self.annotator_name = annotator_name
        self.file_path = file_path
        self.variant = variant

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
        self.file_path = self.variant.to_vcf()
        return self.annotator

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.file_path):
            await aiof.os.remove(self.file_path)

    async def annotate(self, *args, **kwargs):
        process = await asyncio.create_subprocess_exec(
            self.executable_bin,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout, stderr

