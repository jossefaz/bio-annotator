from enum import Enum

human_reference_ucsc_mapping = {
    'hg19': '37',
    'hg38': '38',
    '19': '37',
    'GRCh37': '37',
    'grch37': '37',
    'grch38': '38',
    '37': '37',
    '38': '38'
}


class AssemblyEnum(str, Enum):
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

    @classmethod
    def get_assembly(cls, value):
        try:
            return cls(value)
        except ValueError:
            return
