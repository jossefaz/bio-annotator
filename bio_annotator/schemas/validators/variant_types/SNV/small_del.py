from dataclasses import dataclass

from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.common.exceptions import SnvPayloadError
from bio_annotator.common.exceptions import ChomosomeRangeError
from bio_annotator.schemas.variant import Variant
from bio_annotator.schemas.validators.variant import VariantValidator
from bio_annotator.schemas.validators.variant import validation_error_handler

@dataclass
class ValidationMessages:
    ALT_MISSING = "alt must be given for small deletions variants"
    ONLY_ONE_NUCL_REF = "For small deletions, 'alt' must contain only the ref previous nucleotide " \
                        "and ref must contains more than one nucleotide. i.e TCCC > T "
    REF_NOT_START_WITH_ALT = f"For small deletions, 'ref' must begin by the alt nucleotide, i.e TCCC > T"


class SMALLDELValidator(VariantValidator):

    def __init__(self, variant_schema: Variant):
        super().__init__(variant_schema)

    @classmethod
    @property
    def variant_type(cls):
        return VariantTypeEnum.SMALL_DEL

    @validation_error_handler
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
        if len(self.variant_schema.alt) > 1 or len(self.variant_schema.ref) < 2:
            raise SnvPayloadError(ValidationMessages.ONLY_ONE_NUCL_REF)
        if not self.variant_schema.ref.startswith(self.variant_schema.alt):
            raise SnvPayloadError(ValidationMessages.REF_NOT_START_WITH_ALT)

    def validate_ref(self):
        raise NotImplementedError("Must be implemented for next version")