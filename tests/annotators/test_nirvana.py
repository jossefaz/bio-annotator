import pytest
from bio_annotator.annotators.nirvana.nirvana import Nirvana
from bio_annotator.common.exceptions import AnnotatorConfigurationMissingError


@pytest.mark.parametrize("env_setup", [{"NIRVANA_EXC": "exc",
                                        "NIRVANA_BIN": "bin",
                                        "NIRVANA_DATA": "data"}],
                         indirect=True)
def test_sanity_check_success(env_setup):
    Nirvana.sanity_check()

@pytest.mark.parametrize("env_setup", [{"NIRVANA_EXC": "exc"}],
                         indirect=True)
def test_sanity_check_missing(env_setup):
    with pytest.raises(AnnotatorConfigurationMissingError):
        Nirvana.sanity_check()
