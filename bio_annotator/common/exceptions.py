from dataclasses import dataclass
from typing import List


@dataclass
class ErrorContent:
    code: int
    error_code: int
    message: str


@dataclass
class ErrorMessages:
    INVALID_CHROMOSOME = ErrorContent(code=400, error_code=1, message="Invalid chromosome during validation")
    CNV_INVALID_PAYLOAD = ErrorContent(code=400, error_code=2, message="CNV Variant wrong payload")
    SNV_INVALID_PAYLOAD = ErrorContent(code=400, error_code=3, message="SNV Variant wrong payload")
    CHROMOSOME_RANGE_ERROR = ErrorContent(code=400, error_code=4, message="Chromosome range out of bound error")
    ANNOTATOR_CONFIGURATION_ERROR = ErrorContent(code=500, error_code=5,
                                                 message="At least one of the mandatory setting for annotator is missing")


class BioAnnotatorError(Exception):
    def __init__(self, error: ErrorContent):
        self.error_code = error.error_code
        self.code = error.code
        self.message = error.message

    def __str__(self):
        return str(self.message)


class InvalidChromosomeError(BioAnnotatorError):

    def __init__(self):
        super().__init__(ErrorMessages.INVALID_CHROMOSOME)


class PayloadError(BioAnnotatorError):

    def __init__(self, error: ErrorContent):
        super().__init__(error)


class CnvPayloadError(PayloadError):

    def __init__(self, param=None):
        super().__init__(ErrorMessages.CNV_INVALID_PAYLOAD)
        self.message = f"{self.message} : {str(param)}"


class SnvPayloadError(PayloadError):

    def __init__(self, param=None):
        super().__init__(ErrorMessages.SNV_INVALID_PAYLOAD)
        self.message = f"{self.message} : {str(param)}"


class ChomosomeRangeError(PayloadError):

    def __init__(self, chromosome_msg: str = '', max_range_msg: str = '', position_msg: str = ''):
        super().__init__(ErrorMessages.CHROMOSOME_RANGE_ERROR)
        if chromosome_msg:
            chromosome_msg = f"chromosome={chromosome_msg}"
        if max_range_msg:
            max_range_msg = f"max_range={max_range_msg}"
        if position_msg:
            position_msg = f"position={position_msg}"
        self.message = f"{self.message} : {chromosome_msg}, {max_range_msg}, {position_msg}"


class AnnotatorConfigurationMissingError(BioAnnotatorError):

    def __init__(self, annotator_name: str):
        super().__init__(ErrorMessages.ANNOTATOR_CONFIGURATION_ERROR)
        self.message = f"{self.message} : {annotator_name}"
