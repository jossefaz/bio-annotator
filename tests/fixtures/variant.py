import random

import pytest
from pydantic_factories import ModelFactory

from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.schemas.variant import Variant


class VariantFactory(ModelFactory):
    __model__ = Variant

def get_random_nucleotides(number=1, exclude=''):
    allowed = [n for n in ['A', 'C', 'T', 'G'] if n not in exclude]
    return ''.join(random.choices(allowed, k=number))

@pytest.fixture(scope='session')
def variant_schema_factory():
    def factory(**kwargs) -> Variant:
        kwargs['start'] = kwargs.pop('start', random.randint(1, 100))
        kwargs['end'] = kwargs.pop('end', random.randint(100, 1000))
        variant_type = kwargs.pop('variant_type', VariantTypeEnum.SNV)
        if variant_type in [VariantTypeEnum.DEL, VariantTypeEnum.DUP]:
            kwargs['alt'] = None
        else:
            kwargs['end'] = None
        create_variant = VariantFactory.build(**kwargs, variant_type=variant_type)
        if create_variant.variant_type == VariantTypeEnum.SNV:
            create_variant.ref = create_variant.ref[0] if create_variant.ref else get_random_nucleotides()
            create_variant.alt = create_variant.alt[0] if create_variant.alt else get_random_nucleotides()
            if create_variant.ref == create_variant.alt:
                create_variant.alt = get_random_nucleotides(exclude=create_variant.ref)
        if create_variant.variant_type == VariantTypeEnum.SMALL_INS:
            alt = get_random_nucleotides(5)
            if create_variant.alt and len(create_variant.alt) > 1:
                alt = create_variant.alt
            create_variant.alt = alt
            create_variant.ref = create_variant.alt[0]
            create_variant.variant_type = VariantTypeEnum.SNV
        if create_variant.variant_type == VariantTypeEnum.SMALL_DEL:
            ref = get_random_nucleotides(5)
            if create_variant.ref and len(create_variant.ref) > 1:
                ref = create_variant.ref
            create_variant.ref = ref
            create_variant.alt = create_variant.ref[0]
            create_variant.variant_type = VariantTypeEnum.SNV
        return create_variant

    return factory
