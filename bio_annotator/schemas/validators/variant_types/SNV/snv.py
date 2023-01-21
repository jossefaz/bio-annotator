from dataclasses import dataclass

from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.common.exceptions import SnvPayloadError
from bio_annotator.common.exceptions import ChomosomeRangeError
from bio_annotator.schemas.variant import Variant
from bio_annotator.schemas.validators.variant import VariantValidator

@dataclass
class ValidationMessages:
    ALT_MISSING = "alt must be given for SNV variants"
    ONLY_ONE_NUCL_REF = "in SNV, only one nucleotide replaced by one other nucleotide is supported"

class SUBValidator(VariantValidator):

    def __init__(self, variant_schema: Variant):
        super().__init__(variant_schema)

    @classmethod
    @property
    def variant_type(cls):
        return VariantTypeEnum.SNV

    def validate(self):
        self.validate_end()
        self.validate_alt()
        self.validate_ref_alt()
        self.validate_start()
        return super().validate()

    @staticmethod
    def validate_snv_payload_type(payload: Variant):
        payload_type = None
        ref = len(payload.ref or '')
        alt = len(payload.alt or '')
        if ref > alt:
            payload.variant_type = payload_type = VariantTypeEnum.SMALL_DEL
        if ref < alt:
            payload.variant_type = payload_type = VariantTypeEnum.SMALL_INS
        if ref == alt == 1:
            payload.variant_type = payload_type = VariantTypeEnum.SNV
        return payload_type

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
        if not len(self.variant_schema.alt) == len(self.variant_schema.ref) == 1:
            raise SnvPayloadError(ValidationMessages.ONLY_ONE_NUCL_REF)

    def validate_ref(self):
        raise NotImplementedError("Must be implemented for next version")