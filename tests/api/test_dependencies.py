import pytest
from fastapi import HTTPException

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.api.annotation.v1.common.dependencies import validate_annotator_name
from bio_annotator.api.annotation.v1.common.dependencies import validate_assembly


@pytest.mark.parametrize("annotator", AsyncAnnotator.__subclasses__())
def test_validate_annotator_name_will_return_annotator_name_if_subclass_of_async_annotator(annotator):
    assert validate_annotator_name(annotator.__name__.lower()) == annotator.__name__.lower()


def test_validate_annotator_name_will_raise_404_if_not_subclass_of_async_annotator():
    with pytest.raises(HTTPException) as exc:
        validate_annotator_name('blabla')


@pytest.mark.parametrize("assembly", ['GRCh37', 'GRCh38'])
def test_validate_assembly_will_return_assembly_if_valid(assembly):
    assert validate_assembly(assembly) == assembly


def test_validate_assembly_name_will_raise_404_if_not_valid():
    with pytest.raises(HTTPException) as exc:
        validate_assembly('blabla')
