
from common.bioutils.chromosome import Chromosome
from common.bioutils.chromosome import get_chromosome
from common.exceptions import ChomosomeRangeError
from common.exceptions import InvalidChromosomeError
from common.exceptions import PayloadError
from schemas.variants import Variant


def validation_error_handler(validator):
    def variant_validator_handler(*args, **kwargs):
        try:
            return validator(*args, **kwargs)
        except (PayloadError, ChomosomeRangeError) as ve:
            raise ValueError(ve.message)

    return variant_validator_handler


class VariantValidator:

    def __init__(self, variant_schema: Variant):
        self.variant_schema = variant_schema

    @classmethod
    @property
    def variant_type(cls):
        raise NotImplementedError('No variant type found')

    def get_validator(self):
        for validator in VariantValidator.__subclasses__():
            if validator.variant_type == self.variant_schema.variant_type:
                return validator(self.variant_schema)
        raise ValueError("No validator found for input variant type. Might not be supported yet")

    def validate(self):
        self.variant_schema.version = self.get_chromosome().version
        return self.variant_schema

    def get_chromosome(self) -> Chromosome:
        mapped_chromosome = get_chromosome(self.variant_schema.chromosome)
        if mapped_chromosome:
            return getattr(mapped_chromosome, self.variant_schema.human_reference)
        raise InvalidChromosomeError()
