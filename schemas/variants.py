import asyncio
from typing import Optional
from uuid import uuid4

import aiofiles
from pydantic import BaseModel

from common.constants import VCF_COLUMNS
from common.constants import VCF_HEADERS
from common.types import HumanReference
from common.types import REF_ALT_NUCL
from common.types import VariantTypeEnum
from common.types import Chromosome as ChromosomeRegex


class VariantOptions(BaseModel):
    hgvs: bool = True


class Variant(BaseModel):
    variant_type: VariantTypeEnum
    chromosome: ChromosomeRegex
    human_reference: HumanReference
    start: int
    end: Optional[int]
    ref: REF_ALT_NUCL
    alt: Optional[REF_ALT_NUCL]
    version: Optional[int]
    options: Optional[VariantOptions] = VariantOptions()

    @property
    def vcf_template(self):
        return '{chromosome}\t{start}\t.\t{ref}\t{alt}\t.\t.\t.'

    async def to_vcf(self, directory='cache'):
        file_name = f"{directory}/{uuid4()}.vcf"
        variant_dict = self.dict()
        vcf_string = self.vcf_template.format(**variant_dict)

        async with aiofiles.open(file_name, 'w') as f:
            await f.write('\n'.join(VCF_HEADERS))
            await f.write('\n')
            await f.write(VCF_COLUMNS)
            await f.write('\n')
            await f.write(vcf_string)
        return file_name