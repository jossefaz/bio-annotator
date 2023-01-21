from fastapi import HTTPException
from starlette import status

from bio_annotator.common.types import VariantTypeEnum
from bio_annotator.schemas.variant import Variant
from bio_annotator.schemas.validators.variant_types.SNV.snv import SUBValidator
from bio_annotator.schemas.validators.variant import VariantValidator


def validate_variant_payload(payload: Variant):
    if payload.variant_type == VariantTypeEnum.SNV:
        payload_type = SUBValidator.validate_snv_payload_type(payload)
        if not payload_type:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                "SNV supported types are : small del, small ins or single substitution")
    validated_payload = VariantValidator(payload).get_validator().validate()
    return validated_payload
