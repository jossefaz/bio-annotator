from dataclasses import dataclass


@dataclass
class ErrorMessages:
    INVALID_CHROMOSOME = "Invalid chromosome during validation"
    CNV_INVALID_PAYLOAD = "CNV Variant wrong payload"
    SNV_INVALID_PAYLOAD = "SNV Variant wrong payload"
    CHROMOSOME_RANGE_ERROR = "Chromosome range out of bound error"


class BioAnnotatorError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class InvalidChromosomeError(BioAnnotatorError):

    def __init__(self):
        self.message = ErrorMessages.INVALID_CHROMOSOME


class PayloadError(BioAnnotatorError):

    def __init__(self, message=None):
        self.message = message


class CnvPayloadError(PayloadError):

    def __init__(self, param=None):
        super().__init__(f"{ErrorMessages.CNV_INVALID_PAYLOAD} : {str(param)}")


class SnvPayloadError(PayloadError):

    def __init__(self, param=None):
        super().__init__(f"{ErrorMessages.SNV_INVALID_PAYLOAD} : {str(param)}")


class ChomosomeRangeError(PayloadError):

    def __init__(self, chromosome_msg: str = '', max_range_msg: str = '', position_msg: str = ''):
        if chromosome_msg:
            chromosome_msg = f"chromosome={chromosome_msg}"
        if max_range_msg:
            max_range_msg = f"max_range={max_range_msg}"
        if position_msg:
            position_msg = f"position={position_msg}"
        self.message = f"{ErrorMessages.CHROMOSOME_RANGE_ERROR} : {chromosome_msg}, {max_range_msg}, {position_msg}"
