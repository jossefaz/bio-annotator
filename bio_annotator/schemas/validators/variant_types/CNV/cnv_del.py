from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.common.exceptions import CnvPayloadError
from bio_annotator.common.exceptions import ChomosomeRangeError
from bio_annotator.schemas.variant import Variant
from bio_annotator.schemas.validators.variant import VariantValidator
from bio_annotator.schemas.validators.variant import validation_error_handler


class DELValidator(VariantValidator):

    def __init__(self, variant_schema: Variant):
        super().__init__(variant_schema)

    @classmethod
    @property
    def variant_type(cls):
        return VariantTypeEnum.DEL

    @validation_error_handler
    def validate(self):
        self.validate_alt()
        self.validate_start()
        self.validate_end()
        return super().validate()

    def validate_end(self):
        if not self.variant_schema.end:
            raise CnvPayloadError(f"end is missing")
        start, end = self.variant_schema.start, self.variant_schema.end
        chromosome_range = self.get_chromosome().max_range
        error_msg = None
        if not (start < end - 1 and end <= chromosome_range):
            error_msg = end
        if not start < end - 1:
            error_msg = 'DEL variants must have at least a length of 2 bp'
        if error_msg:
            raise ChomosomeRangeError(chromosome_msg=self.variant_schema.chromosome,
                                      max_range_msg=chromosome_range,
                                      position_msg=error_msg)

    def validate_start(self):
        start = self.variant_schema.start
        chromosome_range = self.get_chromosome().max_range
        if not 1 <= start <= chromosome_range:
            raise ChomosomeRangeError(chromosome_msg=self.variant_schema.chromosome,
                                      max_range_msg=chromosome_range,
                                      position_msg=str(start))

    def validate_alt(self):
        if self.variant_schema.alt:
            raise CnvPayloadError(f"alt must be set to None for all DEL variants")

    def validate_ref(self):
        raise NotImplementedError("Must be implemented for next version")
