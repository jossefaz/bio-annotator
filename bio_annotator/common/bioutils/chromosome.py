import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import List
from typing import Union

from common.bioutils.assembly import AssemblyEnum
from common.bioutils.iscn.cytobands.cytoband import Cytoband
import common.bioutils.iscn.cytobands.grch_37 as cyto37
import common.bioutils.iscn.cytobands.grch_38 as cyto38

REFSEQ_ZFILL = 6
nucleotides = ['A', 'C', 'T', 'G']
chromosome_ncbi_mapper = defaultdict(str,
                                     {str(i): str(i) for i in range(23)} |
                                     {
                                         "X": "23",
                                         "23": "X",
                                         "Y": "24",
                                         "24": "Y",
                                         "M": "12920",
                                         "12920": "M"
                                     })



class Chromosome:

    def __init__(self, chromosome_number, refseq_version, range, cytobands: List[Cytoband] = None, alias=None):
        self.reference_sequence = f"NC_{str(chromosome_number).zfill(REFSEQ_ZFILL)}"
        self.version = refseq_version
        self.chromosome = alias or chromosome_number
        self._assembly = None
        self.max_range = range
        self.cytobands = cytobands

    @property
    def assembly(self):
        return self._assembly

    @assembly.setter
    def assembly(self, assembly):
        self._assembly = assembly

    def check_range(self, position: Union[int, range]):
        if isinstance(position, (int, range)):
            check_position = position[-1] if isinstance(position, range) else position
            if 1 <= check_position <= self.max_range:
                return True
        return False

    def get_cytobands(self, position: Union[int, range]):
        if not self.cytobands:
            return
        cytobands = []
        for c in self.cytobands:
            if position in c:
                if isinstance(position, int):
                    return c.cytoband
                cytobands.append(c.cytoband)
        return cytobands

    @cached_property
    def ctyobands_map(self):
        cytobands_map = {'p': {}, 'q': {}}
        for c in self.cytobands:
            cyto_type = c.type.value
            band = str(c.band)
            s_band = str(c.s_band)
            ss_band = str(c.ss_band or '')
            if band not in cytobands_map[cyto_type]:
                cytobands_map[cyto_type][band] = {}
            if s_band not in cytobands_map[cyto_type][band]:
                cytobands_map[cyto_type][band][s_band] = {}
            if not ss_band:
                cytobands_map[cyto_type][band][s_band][''] = c
                continue
            if ss_band not in cytobands_map[cyto_type][band][s_band]:
                cytobands_map[cyto_type][band][s_band][ss_band] = c
        return cytobands_map

    def get_ctyoband_range(self, cytoband_notation):
        cytoband_regex = "(?P<type>p|q)" \
                         "(?P<band>[1-9])" \
                         "(?P<s_band>[1-9])" \
                         ".?(?P<ss_band>[1-9][0-9]?)?"
        if (match := re.match(cytoband_regex, cytoband_notation)):
            cytoband = match.groupdict()
            try:
                cytoband = self.ctyobands_map[cytoband['type']][cytoband['band']][cytoband['s_band']][
                    cytoband['ss_band'] or '']
                if isinstance(cytoband, Cytoband):
                    return cytoband.range
            except KeyError:
                return

    def __repr__(self):
        return f"Chromosome(chromosome_number={int(self.reference_sequence.split('NC_')[1])}, " \
               f"refseq_version={self.version}, " \
               f"alias={self.chromosome})"


class GRCh37:
    _1 = Chromosome(chromosome_number=1, refseq_version=10, range=249250621, cytobands=cyto37.chromosome_1)
    _2 = Chromosome(chromosome_number=2, refseq_version=11, range=243199373, cytobands=cyto37.chromosome_2)
    _3 = Chromosome(chromosome_number=3, refseq_version=11, range=198022430, cytobands=cyto37.chromosome_3)
    _4 = Chromosome(chromosome_number=4, refseq_version=11, range=191154276, cytobands=cyto37.chromosome_4)
    _5 = Chromosome(chromosome_number=5, refseq_version=9, range=180915260, cytobands=cyto37.chromosome_5)
    _6 = Chromosome(chromosome_number=6, refseq_version=11, range=171115067, cytobands=cyto37.chromosome_6)
    _7 = Chromosome(chromosome_number=7, refseq_version=13, range=159138663, cytobands=cyto37.chromosome_7)
    _8 = Chromosome(chromosome_number=8, refseq_version=10, range=146364022, cytobands=cyto37.chromosome_8)
    _9 = Chromosome(chromosome_number=9, refseq_version=11, range=141213431, cytobands=cyto37.chromosome_9)
    _10 = Chromosome(chromosome_number=10, refseq_version=10, range=135534747, cytobands=cyto37.chromosome_10)
    _11 = Chromosome(chromosome_number=11, refseq_version=9, range=135006516, cytobands=cyto37.chromosome_11)
    _12 = Chromosome(chromosome_number=12, refseq_version=11, range=133851895, cytobands=cyto37.chromosome_12)
    _13 = Chromosome(chromosome_number=13, refseq_version=10, range=115169878, cytobands=cyto37.chromosome_13)
    _14 = Chromosome(chromosome_number=14, refseq_version=8, range=107349540, cytobands=cyto37.chromosome_14)
    _15 = Chromosome(chromosome_number=15, refseq_version=9, range=102531392, cytobands=cyto37.chromosome_15)
    _16 = Chromosome(chromosome_number=16, refseq_version=9, range=90354753, cytobands=cyto37.chromosome_16)
    _17 = Chromosome(chromosome_number=17, refseq_version=10, range=81195210, cytobands=cyto37.chromosome_17)
    _18 = Chromosome(chromosome_number=18, refseq_version=9, range=78077248, cytobands=cyto37.chromosome_18)
    _19 = Chromosome(chromosome_number=19, refseq_version=9, range=59128983, cytobands=cyto37.chromosome_19)
    _20 = Chromosome(chromosome_number=20, refseq_version=10, range=63025520, cytobands=cyto37.chromosome_20)
    _21 = Chromosome(chromosome_number=21, refseq_version=8, range=48129895, cytobands=cyto37.chromosome_21)
    _22 = Chromosome(chromosome_number=22, refseq_version=10, range=51304566, cytobands=cyto37.chromosome_22)
    _23 = Chromosome(chromosome_number=23, refseq_version=10, alias='X', range=155270560, cytobands=cyto37.chromosome_x)
    _24 = Chromosome(chromosome_number=24, refseq_version=9, alias='Y', range=59373566, cytobands=cyto37.chromosome_y)
    _12920 = Chromosome(chromosome_number=12920, refseq_version=1, alias='M', range=16569)
    _X = Chromosome(chromosome_number=23, refseq_version=10, alias='X', range=155270560, cytobands=cyto37.chromosome_x)
    _Y = Chromosome(chromosome_number=24, refseq_version=9, alias='Y', range=59373566, cytobands=cyto37.chromosome_y)
    _M = Chromosome(chromosome_number=12920, refseq_version=1, alias='M', range=16569)

    def __init__(self):
        _ = [setattr(c, 'assembly', AssemblyEnum.GRCh37) for c in self.all_chromosome()]

    @classmethod
    def all_chromosome(cls):
        return [getattr(cls, chrom) for chrom in dir(cls)
                if not chrom.startswith('__') and not callable(getattr(cls, chrom))]

    @classmethod
    def all_reference_sequence(cls):
        return [c.reference_sequence for c in cls.all_chromosome()]


class GRCh38:
    _1 = Chromosome(chromosome_number=1, refseq_version=11, range=248956422, cytobands=cyto38.chromosome_1)
    _2 = Chromosome(chromosome_number=2, refseq_version=12, range=242193529, cytobands=cyto38.chromosome_2)
    _3 = Chromosome(chromosome_number=3, refseq_version=12, range=198295559, cytobands=cyto38.chromosome_3)
    _4 = Chromosome(chromosome_number=4, refseq_version=12, range=190214555, cytobands=cyto38.chromosome_4)
    _5 = Chromosome(chromosome_number=5, refseq_version=10, range=181538259, cytobands=cyto38.chromosome_5)
    _6 = Chromosome(chromosome_number=6, refseq_version=12, range=170805979, cytobands=cyto38.chromosome_6)
    _7 = Chromosome(chromosome_number=7, refseq_version=14, range=159345973, cytobands=cyto38.chromosome_7)
    _8 = Chromosome(chromosome_number=8, refseq_version=11, range=145138636, cytobands=cyto38.chromosome_8)
    _9 = Chromosome(chromosome_number=9, refseq_version=12, range=138394717, cytobands=cyto38.chromosome_9)
    _10 = Chromosome(chromosome_number=10, refseq_version=11, range=133797422, cytobands=cyto38.chromosome_10)
    _11 = Chromosome(chromosome_number=11, refseq_version=10, range=135086622, cytobands=cyto38.chromosome_11)
    _12 = Chromosome(chromosome_number=12, refseq_version=12, range=133275309, cytobands=cyto38.chromosome_12)
    _13 = Chromosome(chromosome_number=13, refseq_version=11, range=114364328, cytobands=cyto38.chromosome_13)
    _14 = Chromosome(chromosome_number=14, refseq_version=9, range=107043718, cytobands=cyto38.chromosome_14)
    _15 = Chromosome(chromosome_number=15, refseq_version=10, range=101991189, cytobands=cyto38.chromosome_15)
    _16 = Chromosome(chromosome_number=16, refseq_version=10, range=90338345, cytobands=cyto38.chromosome_16)
    _17 = Chromosome(chromosome_number=17, refseq_version=11, range=83257441, cytobands=cyto38.chromosome_17)
    _18 = Chromosome(chromosome_number=18, refseq_version=10, range=80373285, cytobands=cyto38.chromosome_18)
    _19 = Chromosome(chromosome_number=19, refseq_version=10, range=58617616, cytobands=cyto38.chromosome_19)
    _20 = Chromosome(chromosome_number=20, refseq_version=11, range=64444167, cytobands=cyto38.chromosome_20)
    _21 = Chromosome(chromosome_number=21, refseq_version=9, range=46709983, cytobands=cyto38.chromosome_21)
    _22 = Chromosome(chromosome_number=22, refseq_version=11, range=50818468, cytobands=cyto38.chromosome_22)
    _23 = Chromosome(chromosome_number=23, refseq_version=11, alias='X', range=156040895, cytobands=cyto38.chromosome_x)
    _24 = Chromosome(chromosome_number=24, refseq_version=10, alias='Y', range=57227415, cytobands=cyto38.chromosome_y)
    _12920 = Chromosome(chromosome_number=12920, refseq_version=1, alias='M', range=16569)
    _X = Chromosome(chromosome_number=23, refseq_version=11, alias='X', range=156040895, cytobands=cyto38.chromosome_x)
    _Y = Chromosome(chromosome_number=24, refseq_version=10, alias='Y', range=57227415, cytobands=cyto38.chromosome_y)
    _M = Chromosome(chromosome_number=12920, refseq_version=1, alias='M', range=16569)

    def __init__(self):
        _ = [setattr(c, 'assembly', AssemblyEnum.GRCh38) for c in self.all_chromosome()]

    @classmethod
    def all_chromosome(cls):
        return [getattr(cls, chrom) for chrom in dir(cls)
                if not chrom.startswith('__') and not callable(getattr(cls, chrom))]


@dataclass
class MappedChromosome:
    GRCh37: Chromosome
    GRCh38: Chromosome


def get_chromosome(chromosome, assembly: Union[str, int, AssemblyEnum, None] = AssemblyEnum.GRCh37) -> Union[
    Chromosome, MappedChromosome]:
    chromosome = map_refseq_or_chrom_to_chromosome(chromosome)
    chrom37: Union[Chromosome, None] = getattr(GRCh37, f"_{chromosome}", None)
    chrom38: Union[Chromosome, None] = getattr(GRCh38, f"_{chromosome}", None)
    if chrom38 and chrom37:
        chrom37.assembly = AssemblyEnum.GRCh37
        chrom38.assembly = AssemblyEnum.GRCh38
        mapped_chromosome = MappedChromosome(GRCh37=chrom37, GRCh38=chrom38)
        if (mapped_assembly := AssemblyEnum.get_assembly(assembly)):
            return getattr(mapped_chromosome, mapped_assembly.value)
        return mapped_chromosome


def map_refseq_or_chrom_to_chromosome(reference_sequence_or_chrom):
    mapper = chromosome_ncbi_mapper | {refseq: str(int(refseq.split('NC_')[-1])) for refseq in
                                       GRCh37.all_reference_sequence()}
    return mapper.get(str(reference_sequence_or_chrom).upper())