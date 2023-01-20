import pytest

from bio_annotator.common.constants import VCF_COLUMNS
from bio_annotator.common.constants import VCF_HEADERS


@pytest.mark.asyncio
async def test_to_vcf(tmpdir, variant_schema_factory):
    variant = variant_schema_factory()
    file_name = await variant.to_vcf(directory=tmpdir)
    # check that the file contains the expected data
    vcf_line = variant.vcf_template.format(**variant.dict())
    with open(file_name, 'r') as f:
        lines = f.readlines()
        assert lines[0] == f'{VCF_HEADERS[0]}\n'
        assert lines[1] == f'{VCF_HEADERS[1]}\n'
        assert lines[2] == f'{VCF_COLUMNS}\n'
        assert lines[3] == vcf_line