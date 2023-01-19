import os
import pytest

from common.constants import VCF_COLUMNS
from common.constants import VCF_HEADERS
from schemas.variants import Variant

@pytest.mark.asyncio
async def test_to_vcf(tmpdir):
    variant = Variant(chromosome='1', start='1000', end='1000', ref='A', alt='C', assembly='GRCh38')
    file_name = tmpdir.join("test_file.vcf")
    await variant.to_vcf(file_name)
    # check that the file contains the expected data
    with open(file_name, 'r') as f:
        lines = f.readlines()
        assert lines[0] == f'{VCF_HEADERS[0]}\n'
        assert lines[1] == f'{VCF_HEADERS[1]}\n'
        assert lines[2] == f'{VCF_COLUMNS}\n'
        assert lines[3] == f'{variant.chromosome}\t{variant.start}\t.\t{variant.ref}\t{variant.alt}\t.\t.\t.'