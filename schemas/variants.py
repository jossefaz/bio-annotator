import asyncio

from pydantic import BaseModel

from common.constants import VCF_COLUMNS
from common.constants import VCF_HEADERS


class Variant(BaseModel):
    chromosome: str
    start: str
    end: str
    ref: str
    alt: str
    assembly: str

    async def to_vcf(self, file_name: str):
        vcf_template = '{chromosome}\t{start}\t.\t{ref}\t{alt}\t.\t.\t.'
        variant_dict = self.dict()
        vcf_string = vcf_template.format(**variant_dict)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._write_to_file, file_name, vcf_string)

    def _write_to_file(self, file_name, vcf_string):
        with open(file_name, 'w') as f:
            f.write('\n'.join(VCF_HEADERS))
            f.write('\n')
            f.write(VCF_COLUMNS)
            f.write('\n')
            f.write(vcf_string)
