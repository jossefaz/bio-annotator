import pytest

from bio_annotator.common.bioutils.assembly import AssemblyEnum

@pytest.mark.parametrize("input, expected_output",
                         [(37, AssemblyEnum.GRCh37),
                          (38, AssemblyEnum.GRCh38),
                          ('37', AssemblyEnum.GRCh37),
                          ('38', AssemblyEnum.GRCh38),
                          ('grch37', AssemblyEnum.GRCh37),
                          ('grch38', AssemblyEnum.GRCh38),
                          (19, AssemblyEnum.GRCh37),
                          ('19', AssemblyEnum.GRCh37),
                          ('hg19', AssemblyEnum.GRCh37),
                          ('hg38', AssemblyEnum.GRCh38),
                          ('GRCh37', AssemblyEnum.GRCh37),
                          ('GRCh38', AssemblyEnum.GRCh38),
                          (AssemblyEnum.GRCh37, AssemblyEnum.GRCh37),
                          (AssemblyEnum.GRCh38, AssemblyEnum.GRCh38)]
                         )
def test_assembly_enum_accept_many_input_and_return_expected_assembly(input, expected_output):
    assert AssemblyEnum(input) == expected_output