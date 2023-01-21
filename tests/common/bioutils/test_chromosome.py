import pytest

from bio_annotator.common.bioutils.assembly import AssemblyEnum
from bio_annotator.common.bioutils.chromosome import get_chromosome

@pytest.mark.parametrize("chromosome, expected_assembly, expected_version, expected_reference_sequence, expected_range", [
    (1, 37, 10, "NC_000001", 249250621),
    (1, 38, 11, "NC_000001", 248956422),
    (2, 37, 11, "NC_000002", 243199373),
    (2, 38, 12, "NC_000002", 242193529),
    (3, 37, 11, "NC_000003", 198022430),
    (3, 38, 12, "NC_000003", 198295559),
    (4, 37, 11, "NC_000004", 191154276),
    (4, 38, 12, "NC_000004", 190214555),
    (5, 37, 9, "NC_000005", 180915260),
    (5, 38, 10, "NC_000005", 181538259),
    (6, 37, 11, "NC_000006", 171115067),
    (6, 38, 12, "NC_000006", 170805979),
    (7, 37, 13, "NC_000007", 159138663),
    (7, 38, 14, "NC_000007", 159345973),
    (8, 37, 10, "NC_000008", 146364022),
    (8, 38, 11, "NC_000008", 145138636),
    (9, 37, 11, "NC_000009", 141213431),
    (9, 38, 12, "NC_000009", 138394717),
    (10, 37, 10, "NC_000010", 135534747),
    (10, 38, 11, "NC_000010", 133797422),
    (11, 37, 9, "NC_000011", 135006516),
    (11, 38, 10, "NC_000011", 135086622),
    (12, 37, 11, "NC_000012", 133851895),
    (12, 38, 12, "NC_000012", 133275309),
    (13, 37, 10, "NC_000013", 115169878),
    (13, 38, 11, "NC_000013", 114364328),
    (14, 37, 8, "NC_000014", 107349540),
    (14, 38, 9, "NC_000014", 107043718),
    (15, 37, 9, "NC_000015", 102531392),
    (15, 38, 10, "NC_000015", 101991189),
    (16, 37, 9, "NC_000016", 90354753),
    (16, 38, 10, "NC_000016", 90338345),
    (17, 37, 10, "NC_000017", 81195210),
    (17, 38, 11, "NC_000017", 83257441),
    (18, 37, 9, "NC_000018", 78077248),
    (18, 38, 10, "NC_000018", 80373285),
    (19, 37, 9, "NC_000019", 59128983),
    (19, 38, 10, "NC_000019", 58617616),
    (20, 37, 10, "NC_000020", 63025520),
    (20, 38, 11, "NC_000020", 64444167),
    (21, 37, 8, "NC_000021", 48129895),
    (21, 38, 9, "NC_000021", 46709983),
    (22, 37, 10, "NC_000022", 51304566),
    (22, 38, 11, "NC_000022", 50818468),
    ('X', 37, 10, "NC_000023", 155270560),
    ('X', 38, 11, "NC_000023", 156040895),
    ('Y', 37, 9, "NC_000024", 59373566),
    ('Y', 38, 10, "NC_000024", 57227415),
    ('M', 37, 1, "NC_012920", 16569),
    ('M', 38, 1, "NC_012920", 16569),
])
def test_get_mapped_chromosome_will_return_expected_chromosome_object(chromosome, expected_assembly, expected_version, expected_reference_sequence, expected_range):
    mapped_chromosome = get_chromosome(chromosome, expected_assembly)
    assert mapped_chromosome.reference_sequence == expected_reference_sequence
    assert mapped_chromosome.version == expected_version
    assert mapped_chromosome.assembly == AssemblyEnum(expected_assembly)
    assert mapped_chromosome.max_range == expected_range
    mapped_chromosome_from_refseq = get_chromosome(expected_reference_sequence, expected_assembly)
    assert mapped_chromosome_from_refseq.chromosome == chromosome
    assert mapped_chromosome_from_refseq.version == expected_version
    assert mapped_chromosome_from_refseq.assembly == AssemblyEnum(expected_assembly)
    assert mapped_chromosome_from_refseq.max_range == expected_range