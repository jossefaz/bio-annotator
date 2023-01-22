import gzip
import json

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.schemas.variant import Variant


async def annotate_variant(annotator_name:str, variant: Variant):
    async with AsyncAnnotator(annotator_name) as annotator:
        annotator.sanity_check()
        stdout, stderr = await annotator.annotate_one(variant)
        if stderr:
            raise

        with gzip.open(annotator.output_file, 'rb') as f:
            file_content = f.read()
            return json.loads(file_content)