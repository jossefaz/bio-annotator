from enum import Enum

from pydantic import constr


class VariantTypeEnum(str, Enum):
    SNV = "SNV"
    SMALL_DEL = "SMALL_DEL"
    SMALL_INS = "SMALL_INS"
    DEL = "DEL"
    DUP = "DUP"
    IUPDMAT = "IUPDMAT"
    IUPDPAT = "IUPDPAT"
    HUPDPAT = "HUPDPAT"
    HUPDMAT = "HUPDMAT"
    ROH = "ROH"
    STR = "STR"

CHROMOSOME = "[1-9]|(1[0-9]|2[0-2])|X|Y|M"
NUCLEOTIDES = "[ACTG]"

Chromosome = constr(regex=f"^({CHROMOSOME})$")
REF_ALT_NUCL = constr(regex=f"^{NUCLEOTIDES}*$")

human_reference_ucsc_mapping = {
    'hg19': '37',
    'hg38': '38',
    'GRCh37': '37',
    'GRCh38': '38',
    '37': '37',
    '38': '38'
}


class HumanReference(str, Enum):
    GRCh37 = "GRCh37"
    GRCh38 = "GRCh38"

    @classmethod
    def _missing_(cls, value):
        value = str(value)
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        mapped = human_reference_ucsc_mapping.get(value.lower())
        if mapped:
            return getattr(cls, f"GRCh{mapped}")