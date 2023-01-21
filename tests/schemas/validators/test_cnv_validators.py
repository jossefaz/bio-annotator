import pytest

from bio_annotator.common.exceptions import PayloadError
from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.common.exceptions import ChomosomeRangeError
from bio_annotator.schemas.variant import Variant
from bio_annotator.schemas.validators.variant import VariantValidator



@pytest.mark.parametrize("variant_type", [VariantTypeEnum.DEL, VariantTypeEnum.DUP])
def test_create_variant_CNV_end_validator_bigger_than_range(variant_type):
    # chr6 max : 171115067
    max_range = 171115067
    chrom = "6"
    start_val = 171115067
    end_val = 171115080
    payload = Variant(variant_type=variant_type, chromosome=chrom,
                      human_reference="GRCh37", start=start_val, end=end_val, ref="A")
    validator = VariantValidator(payload).get_validator()
    with pytest.raises(PayloadError) as excinfo:
        validator.validate()
    chromosome_range = validator.get_chromosome().max_range
    end_value_error = ChomosomeRangeError(chromosome_msg=chrom,
                                          max_range_msg=chromosome_range,
                                          position_msg=str(end_val))
    assert str(excinfo.value) == end_value_error.message

@pytest.mark.parametrize("variant_type", [VariantTypeEnum.DEL, VariantTypeEnum.DUP])
def test_create_variant_CNV_start_validator_bigger_than_end(variant_type):
    # chr6 max : 171115067
    max_range = 171115067
    chrom = "6"
    start_val = 171115061
    end_val = 171115060
    with pytest.raises(PayloadError) as excinfo:
        payload = Variant(variant_type=variant_type, chromosome=chrom,
                                human_reference="GRCh37", start=start_val, end=end_val, ref="A")
        validator = VariantValidator(payload).get_validator()
        validator.validate()
    chromosome_range = validator.get_chromosome().max_range
    end_value_error = ChomosomeRangeError(chromosome_msg=chrom,
                                          max_range_msg=chromosome_range,
                                          position_msg=f"{variant_type.value} variants must have at least a length of 2 bp")
    assert str(excinfo.value) == end_value_error.message