import asyncio
import os

from aiofiles import os as aios

from bio_annotator.schemas.variant import Variant


class AsyncAnnotator:
    def __init__(self, annotator_name):
        self.annotator_name = annotator_name
        self.output_file = ''
        self.input_file = ''

    @classmethod
    @property
    def executable_bin(cls):
        return 'echo "ERROR: AsyncAnnotator called directly"'

    @classmethod
    def sanity_check(cls):
        NotImplemented("To be implemented only in child classes")

    @classmethod
    def create_annotator(cls, annotator_name):
        for subclass in cls.__subclasses__():
            if subclass.__name__.lower() == annotator_name.lower():
                return subclass(annotator_name)
        raise ValueError(f"Invalid annotator name: {annotator_name}")

    async def __aenter__(self):
        self.annotator = self.create_annotator(self.annotator_name)
        return self.annotator

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.input_file):
            await aios.remove(self.input_file)

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
        self.input_file = variant.to_vcf()
        return await self.annotate_batch(*args, **kwargs)

