import random

import pytest


from bio_annotator.common.bioutils.chromosome import get_chromosome
from bio_annotator.common.bioutils.iscn.cytobands.cytoband import Cytoband
from bio_annotator.common.bioutils.iscn.cytobands.cytoband import CytobandTypeEnum


def test_cytoband_can_use_in_op_for_checking_single_position():
    position = random.randint(1, 9999999)
    cytoband = Cytoband(CytobandTypeEnum.p, range(position - 1, position + 1), 1, 1, 31)
    assert position in cytoband
    assert position - 2 not in cytoband


def test_cytoband_can_use_in_op_for_checking_position_range():
    position_range = range(random.randint(1, 1000), random.randint(1001, 2000))
    cytoband = Cytoband(CytobandTypeEnum.p, range(position_range[0] - 1, position_range[-1]), 1, 1, 31)
    assert position_range in cytoband
    position_range_out = range(cytoband.range[0] - 3, cytoband.range[0] - 2)
    assert position_range_out not in cytoband


def test_cytoband_property_return_cytoband_notation():
    cytoband = Cytoband(CytobandTypeEnum.p, range(1, 2), 1, 1, 31)
    assert cytoband.cytoband == "p11.31"
    cytoband = Cytoband(CytobandTypeEnum.p, range(1, 2), 1, 1)
    assert cytoband.cytoband == "p11"

@pytest.mark.parametrize("chromosome, assembly, position, expected_cytoband", [
    (1, 37, 1000, "p36.33"),
    (2, 37, 1000, "p25.3"),
    (3, 37, 1000, "p26.3"),
    (4, 37, 1000, "p16.3"),
    (5, 37, 1000, "p15.33"),
    (6, 37, 1000, "p25.3"),
    (7, 37, 1000, "p22.3"),
    (8, 37, 1000, "p23.3"),
    (9, 37, 1000, "p24.3"),
    (10, 37, 1000, "p15.3"),
    (11, 37, 1000, "p15.5"),
    (12, 37, 1000, "p13.33"),
    (13, 37, 1000, "p13"),
    (14, 37, 1000, "p13"),
    (15, 37, 1000, "p13"),
    (16, 37, 1000, "p13.3"),
    (17, 37, 1000, "p13.3"),
    (18, 37, 1000, "p11.32"),
    (19, 37, 1000, "p13.3"),
    (20, 37, 1000, "p13"),
    (21, 37, 1000, "p13"),
    (22, 37, 1000, "p13"),
    ('x', 37, 1000, "p22.33"),
    ('y', 37, 1000, "p11.32"),
    (1, 38, 1000, "p36.33"),
    (2, 38, 1000, "p25.3"),
    (3, 38, 1000, "p26.3"),
    (4, 38, 1000, "p16.3"),
    (5, 38, 1000, "p15.33"),
    (6, 38, 1000, "p25.3"),
    (7, 38, 1000, "p22.3"),
    (8, 38, 1000, "p23.3"),
    (9, 38, 1000, "p24.3"),
    (10, 38, 1000, "p15.3"),
    (11, 38, 1000, "p15.5"),
    (12, 38, 1000, "p13.33"),
    (13, 38, 1000, "p13"),
    (14, 38, 1000, "p13"),
    (15, 38, 1000, "p13"),
    (16, 38, 1000, "p13.3"),
    (17, 38, 1000, "p13.3"),
    (18, 38, 1000, "p11.32"),
    (19, 38, 1000, "p13.3"),
    (20, 38, 1000, "p13"),
    (21, 38, 1000, "p13"),
    (22, 38, 1000, "p13"),
    ('x', 38, 1000, "p22.33"),
    ('y', 38, 1000, "p11.32"),
])
def test_chromosome_return_cytoband_based_on_given_position(chromosome, assembly, position, expected_cytoband):
    chromosome = get_chromosome(chromosome, assembly)
    assert chromosome.get_cytobands(position) == expected_cytoband

@pytest.mark.parametrize("chromosome, assembly, expected_range, cytoband_notation", [
    (1, 37, range(1, 2300000), "p36.33"),
    (2, 37, range(1, 4400000), "p25.3"),
    (3, 37, range(1, 2800000), "p26.3"),
    (4, 37, range(1, 4500000), "p16.3"),
    (5, 37, range(1, 4500000), "p15.33"),
    (6, 37, range(1, 2300000), "p25.3"),
    (7, 37, range(1, 2800000), "p22.3"),
    (8, 37, range(1, 2200000), "p23.3"),
    (9, 37, range(1, 2200000), "p24.3"),
    (10, 37, range(1, 3000000), "p15.3"),
    (11, 37, range(1, 2800000), "p15.5"),
    (12, 37, range(1, 3300000), "p13.33"),
    (13, 37, range(1, 4500000), "p13"),
    (14, 37, range(1, 3700000), "p13"),
    (15, 37, range(1, 3900000), "p13"),
    (16, 37, range(1, 7900000), "p13.3"),
    (17, 37, range(1, 3300000), "p13.3"),
    (18, 37, range(1, 2900000), "p11.32"),
    (19, 37, range(1, 6900000), "p13.3"),
    (20, 37, range(1, 5100000), "p13"),
    (21, 37, range(1, 2800000), "p13"),
    (22, 37, range(1, 3800000), "p13"),
    ('x', 37, range(1, 4300000), "p22.33"),
    ('y', 37, range(1, 2500000), "p11.32"),
    (1, 38, range(1, 2300000), "p36.33"),
    (2, 38, range(1, 4400000), "p25.3"),
    (3, 38, range(1, 2800000), "p26.3"),
    (4, 38, range(1, 4500000), "p16.3"),
    (5, 38, range(1, 4400000), "p15.33"),
    (6, 38, range(1, 2300000), "p25.3"),
    (7, 38, range(1, 2800000), "p22.3"),
    (8, 38, range(1, 2300000), "p23.3"),
    (9, 38, range(1, 2200000), "p24.3"),
    (10, 38, range(1, 3000000), "p15.3"),
    (11, 38, range(1, 2800000), "p15.5"),
    (12, 38, range(1, 3200000), "p13.33"),
    (13, 38, range(1, 4600000), "p13"),
    (14, 38, range(1, 3600000), "p13"),
    (15, 38, range(1, 4200000), "p13"),
    (16, 38, range(1, 7800000), "p13.3"),
    (17, 38, range(1, 3400000), "p13.3"),
    (18, 38, range(1, 2900000), "p11.32"),
    (19, 38, range(1, 6900000), "p13.3"),
    (20, 38, range(1, 5100000), "p13"),
    (21, 38, range(1, 3100000), "p13"),
    (22, 38, range(1, 4300000), "p13"),
    ('x', 38, range(1, 4400000), "p22.33"),
    ('y', 38, range(1, 300000), "p11.32"),
])
def test_chromosome_return_cytoband_range_based_on_notation(chromosome, assembly, expected_range, cytoband_notation):
    chromosome = get_chromosome(chromosome, assembly)
    assert chromosome.get_ctyoband_range(cytoband_notation) == expected_range

@pytest.mark.parametrize("chromosome, assembly, input_range, expected_cytobands", [
    (1, 37, range(1, 2300100), ['p36.33', 'p36.32']),
    (2, 37, range(1, 4400100), ['p25.3', 'p25.2']),
    (3, 37, range(1, 2800100), ['p26.3', 'p26.2']),
    (4, 37, range(1, 4500100), ['p16.3', 'p16.2']),
    (5, 37, range(1, 4500100), ['p15.33', 'p15.32']),
    (6, 37, range(1, 2300100), ['p25.3', 'p25.2']),
    (7, 37, range(1, 2800100), ['p22.3', 'p22.2']),
    (8, 37, range(1, 2200100), ['p23.3', 'p23.2']),
    (9, 37, range(1, 2200100), ['p24.3', 'p24.2']),
    (10, 37, range(1, 3000100), ['p15.3', 'p15.2']),
    (11, 37, range(1, 2800100), ['p15.5', 'p15.4']),
    (12, 37, range(1, 3300100), ['p13.33', 'p13.32']),
    (13, 37, range(1, 4500100), ['p13', 'p12']),
    (14, 37, range(1, 3700100), ['p13', 'p12']),
    (15, 37, range(1, 3900100), ['p13', 'p12']),
    (16, 37, range(1, 7900100), ['p13.3', 'p13.2']),
    (17, 37, range(1, 3300100), ['p13.3', 'p13.2']),
    (18, 37, range(1, 2900100), ['p11.32', 'p11.31']),
    (19, 37, range(1, 6900100), ['p13.3', 'p13.2']),
    (20, 37, range(1, 5100100), ['p13', 'p12.3']),
    (21, 37, range(1, 2800100), ['p13', 'p12']),
    (22, 37, range(1, 3800100), ['p13', 'p12']),
    ('x', 37, range(1, 4300100), ['p22.33', 'p22.32']),
    ('y', 37, range(1, 2500100), ['p11.32', 'p11.31']),
    (1, 38, range(1, 2300100), ['p36.33', 'p36.32']),
    (2, 38, range(1, 4400100), ['p25.3', 'p25.2']),
    (3, 38, range(1, 2800100), ['p26.3', 'p26.2']),
    (4, 38, range(1, 4500100), ['p16.3', 'p16.2']),
    (5, 38, range(1, 4400100), ['p15.33', 'p15.32']),
    (6, 38, range(1, 2300100), ['p25.3', 'p25.2']),
    (7, 38, range(1, 2800100), ['p22.3', 'p22.2']),
    (8, 38, range(1, 2300100), ['p23.3', 'p23.2']),
    (9, 38, range(1, 2200100), ['p24.3', 'p24.2']),
    (10, 38, range(1, 3000100), ['p15.3', 'p15.2']),
    (11, 38, range(1, 2800100), ['p15.5', 'p15.4']),
    (12, 38, range(1, 3200100), ['p13.33', 'p13.32']),
    (13, 38, range(1, 4600100), ['p13', 'p12']),
    (14, 38, range(1, 3600100), ['p13', 'p12']),
    (15, 38, range(1, 4200100), ['p13', 'p12']),
    (16, 38, range(1, 7800100), ['p13.3', 'p13.2']),
    (17, 38, range(1, 3400100), ['p13.3', 'p13.2']),
    (18, 38, range(1, 2900100), ['p11.32', 'p11.31']),
    (19, 38, range(1, 6900100), ['p13.3', 'p13.2']),
    (20, 38, range(1, 5100100), ['p13', 'p12.3']),
    (21, 38, range(1, 3100100), ['p13', 'p12']),
    (22, 38, range(1, 4300100), ['p13', 'p12']),
    ('x', 38, range(1, 4400100), ['p22.33', 'p22.32']),
    ('y', 38, range(1, 300100), ['p11.32', 'p11.31']),
])
def test_chromosome_return_list_of_cytobands_if_range(chromosome, assembly, input_range, expected_cytobands):
    chromosome = get_chromosome(chromosome, assembly)
    assert chromosome.get_cytobands(input_range) == expected_cytobands