import json

import pytest
import asyncio
import gzip
import io
import aiofiles

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.api.annotation.v1.controller import annotate_variant


@pytest.mark.asyncio
@pytest.mark.parametrize("annotator", AsyncAnnotator.__subclasses__())
async def test_annotate_single_variant_will_read_gzip_asynchronously(annotator, variant_schema_factory, monkeypatch):
    TEST_FILE = "test.json.gz"

    def mock_annotator_init(self, annotator_name):
        self.output_file = TEST_FILE

    async def mock_annotate_one(self, variant):
        return True, False

    monkeypatch.setattr(annotator, 'sanity_check', lambda self: True)
    monkeypatch.setattr(annotator, 'annotate_one', mock_annotate_one)
    monkeypatch.setattr(annotator, '__init__', mock_annotator_init)
    test_data = b'{"hello":"world"}'
    with gzip.open(TEST_FILE, "wb") as f:
        f.write(test_data)

    data = await annotate_variant(annotator.__name__, variant_schema_factory())

    assert data == json.loads(test_data)

    await aiofiles.os.remove(TEST_FILE)
