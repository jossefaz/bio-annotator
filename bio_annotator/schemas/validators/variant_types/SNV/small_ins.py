from dataclasses import dataclass

from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.common.exceptions import SnvPayloadError
from bio_annotator.common.exceptions import ChomosomeRangeError
from bio_annotator.schemas.variant import Variant
from bio_annotator.schemas.validators.variant import VariantValidator


@dataclass
class ValidationMessages:
    ALT_MISSING = "alt must be given for small insertions variants"
    ALT_LESS_THAN_REF = "For small insertions, 'alt' must contain more nucleotides than 'ref'"
    ONLY_ONE_NUCL_REF = "For small insertions, 'ref' must only one nucleotide, " \
                        "which represent the previous nucleotide before the insertion"
    ALT_NOT_START_WITH_REF = f"For small insertions, 'alt' must begin by the ref nucleotide, i.e A > ATCC"


class SMALLINSValidator(VariantValidator):

    def __init__(self, variant_schema: Variant):
        super().__init__(variant_schema)

    @classmethod
    @property
    def variant_type(cls):
        return VariantTypeEnum.SMALL_INS

    def validate(self):
        self.validate_end()
        self.validate_alt()
        self.validate_ref_alt()
        self.validate_start()
        return super().validate()

    def validate_end(self):
        if self.variant_schema.end:
            raise SnvPayloadError(f"end was given : {self.variant_schema.end}")

    def validate_start(self):
        start = self.variant_schema.start
        chromosome_range = self.get_chromosome().max_range
        if not 1 <= start <= chromosome_range:
            raise ChomosomeRangeError(chromosome_msg=self.variant_schema.chromosome,
                                      max_range_msg=chromosome_range,
                                      position_msg=str(start))

    def validate_alt(self):
        if not self.variant_schema.alt:
            raise SnvPayloadError(ValidationMessages.ALT_MISSING)

    def validate_ref_alt(self):
        if len(self.variant_schema.alt) < len(self.variant_schema.ref):
            raise SnvPayloadError(ValidationMessages.ALT_LESS_THAN_REF)
        if not len(self.variant_schema.ref) == 1:
            raise SnvPayloadError(ValidationMessages.ONLY_ONE_NUCL_REF)
        if not self.variant_schema.alt.startswith(self.variant_schema.ref):
            raise SnvPayloadError(ValidationMessages.ALT_NOT_START_WITH_REF)

    def validate_ref(self):
        raise NotImplementedError("Must be implemented for next version")
