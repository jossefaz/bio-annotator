import pytest
from bio_annotator.annotators.vep.vep import VEP
from bio_annotator.common.exceptions import AnnotatorConfigurationMissingError


@pytest.mark.parametrize("env_setup", [{"VEP_EXC": "exc",
                                        "VEP_BIN": "bin",
                                        "VEP_DATA": "data"}],
                         indirect=True)
def test_sanity_check_success(env_setup):
    VEP.sanity_check()

@pytest.mark.parametrize("env_setup", [{"VEP_EXC": "exc"}],
                         indirect=True)
def test_sanity_check_missing(env_setup):
    with pytest.raises(AnnotatorConfigurationMissingError):
        VEP.sanity_check()
