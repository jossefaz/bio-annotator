import pytest
from unittest.mock import patch
from pydantic import ValidationError

from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.common.exceptions import ChomosomeRangeError
from bio_annotator.common.exceptions import SnvPayloadError
from bio_annotator.schemas.validators.variant_types.SNV.snv import SUBValidator
from bio_annotator.schemas.variant import Variant
from bio_annotator.schemas.validators.variant_types.SNV.small_ins import ValidationMessages as small_ins_messages
from bio_annotator.schemas.validators.variant_types.SNV.snv import ValidationMessages as sub_messages
from bio_annotator.schemas.validators.variant import VariantValidator

@patch('bio_annotator.schemas.variant.Variant.__init__', side_effect=SnvPayloadError("wrong attribute"))
def test_flow_create_variant_SNV_end_validator_fail(_):
    # chr6 max : 171115067
    start_val = 171115066
    end_val = 171115067
    chrom = "6"
    with pytest.raises(SnvPayloadError) as excinfo:
        Variant(variant_type=VariantTypeEnum.SNV, chromosome=chrom,
                      human_reference="GRCh37", start=start_val, end=end_val, ref="A")
    assert excinfo.value.message == SnvPayloadError("wrong attribute").message

def test_create_variant_SNV_end_validator_fail():
    # chr6 max : 171115067
    start_val = 171115066
    end_val = 171115067
    chrom = "6"
    with pytest.raises(ValueError) as excinfo:
        payload = Variant(variant_type=VariantTypeEnum.SNV, chromosome=chrom,
                                human_reference="GRCh37", start=start_val, end=end_val, ref="A")
        VariantValidator(payload).get_validator().validate()
    assert str(excinfo.value) == SnvPayloadError(f"end was given : {end_val}").message

@pytest.mark.parametrize("variant_type", [VariantTypeEnum.SNV, VariantTypeEnum.DEL, VariantTypeEnum.DUP])
def test_create_variant_snv_and_cnv_start_validator_bigger_than_range(variant_schema_factory, variant_type):
    # chr6 max : 171115067
    start_val = 171115070
    end_val = 171115078
    chrom = "6"
    with pytest.raises(ValueError) as excinfo:
        payload = variant_schema_factory(variant_type=variant_type, chromosome=chrom,
                                                human_reference="GRCh37", start=start_val, end=end_val, ref="A")
        validator = VariantValidator(payload).get_validator()
        validator.validate()
    chromosome_range = validator.get_chromosome().max_range
    start_value_error = ChomosomeRangeError(chromosome_msg=chrom,
                                            max_range_msg=chromosome_range,
                                            position_msg=str(start_val))
    assert str(excinfo.value) == start_value_error.message





@pytest.mark.variant
@pytest.mark.integration
@pytest.mark.service
def test_create_variant_wrong_variant_type_sent(variant_schema_factory):
    create_variant_payload = variant_schema_factory()
    create_variant_payload.variant_type = "NOT_EXIST_TYPE"
    with pytest.raises(ValidationError):
        Variant.validate(create_variant_payload.dict())

@pytest.mark.parametrize("variant_type", [VariantTypeEnum.SMALL_DEL, VariantTypeEnum.SMALL_INS])
def test_create_variant_INDEL_start_validator_bigger_than_end(variant_type, variant_schema_factory):
    variant_payload = variant_schema_factory(variant_type=variant_type)
    assert variant_payload.variant_type == VariantTypeEnum.SNV
    SUBValidator.validate_snv_payload_type(variant_payload)
    assert variant_payload.variant_type == variant_type
    validator = VariantValidator(variant_payload).get_validator()
    chromosome = validator.get_chromosome()
    variant_payload.start = chromosome.max_range + 1
    with pytest.raises(ValueError) as excinfo:
        validator.validate()
    end_value_error = ChomosomeRangeError(chromosome_msg=chromosome.chromosome,
                                          max_range_msg=chromosome.max_range,
                                          position_msg=variant_payload.start)
    assert str(excinfo.value) == end_value_error.message


@pytest.mark.parametrize("variant_type, expected_message", [
    (VariantTypeEnum.SMALL_INS, small_ins_messages.ONLY_ONE_NUCL_REF),
    (VariantTypeEnum.SNV, sub_messages.ONLY_ONE_NUCL_REF)])
def test_create_variant_SMALL_INS_and_SNV_validator_raise_when_ref_greater_than_one_nucleotide(variant_type,
                                                                                               expected_message,
                                                                                               variant_schema_factory):
    variant_payload = variant_schema_factory(variant_type=variant_type)
    assert variant_payload.variant_type == VariantTypeEnum.SNV
    SUBValidator.validate_snv_payload_type(variant_payload)
    assert variant_payload.variant_type == variant_type
    variant_payload.ref += 'A'
    validator = VariantValidator(variant_payload).get_validator()
    chromosome = validator.get_chromosome()
    variant_payload.start = chromosome.max_range + 1
    with pytest.raises(ValueError) as excinfo:
        validator.validate()
    assert str(excinfo.value) == f"SNV Variant wrong payload : {expected_message}"

def test_validate_snv_payload_will_return_none_when_ref_alt_same_length_greater_than_1(variant_schema_factory):
    variant_payload = variant_schema_factory(variant_type=VariantTypeEnum.SNV)
    variant_payload.ref = 'TTT'
    variant_payload.alt = 'AAA'
    variant_type = SUBValidator.validate_snv_payload_type(variant_payload)
    assert variant_type is None