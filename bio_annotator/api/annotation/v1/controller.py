import asyncio
import gzip
import io
import json
import tempfile
import uuid

import aiofiles

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.schemas.variant import Variant


async def annotate_variant(annotator_name: str, variant: Variant):
    async with AsyncAnnotator(annotator_name) as annotator:
        annotator.sanity_check()
        await annotator.annotate_one(variant)
        async with aiofiles.open(annotator.output_file, mode='rb') as f:
            compressed_data = await f.read()
        with io.BytesIO(compressed_data) as buf, gzip.GzipFile(fileobj=buf) as gz:
            data = await asyncio.get_event_loop().run_in_executor(None, gz.read)
        return json.loads(data)


async def annotate_file(annotator_name: str, assembly: str, file):
    file_name = uuid.uuid4()
    async with aiofiles.open(f"cache/{file_name}.vcf.gz", "wb") as f:
        await f.write(file)
    async with AsyncAnnotator(annotator_name) as annotator:
        annotator.human_reference = assembly
        annotator.input_file = f"cache/{file_name}.vcf.gz"
        await annotator.annotate_batch()
        return annotator.output_file
