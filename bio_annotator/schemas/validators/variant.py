
from bio_annotator.common.bioutils.chromosome import Chromosome
from bio_annotator.common.bioutils.chromosome import get_chromosome
from bio_annotator.common.exceptions import ChomosomeRangeError
from bio_annotator.common.exceptions import InvalidChromosomeError
from bio_annotator.common.exceptions import PayloadError
from bio_annotator.schemas.variant import Variant

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
        chromosome = get_chromosome(self.variant_schema.chromosome)
        if not chromosome:
            raise InvalidChromosomeError()
        return chromosome
