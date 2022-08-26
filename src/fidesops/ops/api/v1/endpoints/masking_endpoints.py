import logging
from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from fidesops.ops.api.v1.urn_registry import MASKING, MASKING_STRATEGY, V1_URL_PREFIX
from fidesops.ops.common_exceptions import NoSuchStrategyException, ValidationError
from fidesops.ops.schemas.masking.masking_api import (
    MaskingAPIRequest,
    MaskingAPIResponse,
)
from fidesops.ops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
)
from fidesops.ops.service.masking.strategy.masking_strategy import MaskingStrategy
from fidesops.ops.service.strategy_factory import strategies, strategy
from fidesops.ops.util.api_router import APIRouter

router = APIRouter(tags=["Masking"], prefix=V1_URL_PREFIX)

logger = logging.getLogger(__name__)


@router.put(MASKING, response_model=MaskingAPIResponse)
def mask_value(request: MaskingAPIRequest) -> MaskingAPIResponse:
    """Masks the value(s) provided using the provided masking strategy"""
    try:
        values = request.values
        masking_strategy_spec = request.masking_strategy
        masking_strategy: MaskingStrategy = strategy(  # type: ignore
            masking_strategy_spec.strategy, masking_strategy_spec.configuration
        )
        logger.info(
            "Starting masking of %s value(s) with strategy %s",
            len(values),
            masking_strategy_spec.strategy,
        )
        masked_values = masking_strategy.mask(values, None)
        return MaskingAPIResponse(plain=values, masked_values=masked_values)
    except NoSuchStrategyException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(MASKING_STRATEGY, response_model=List[MaskingStrategyDescription])
def list_masking_strategies() -> List[MaskingStrategyDescription]:
    """Lists available masking strategies with instructions on how to use them"""
    logger.info("Getting available masking strategies")
    return [
        strategy.get_description()
        for strategy in strategies()
        if issubclass(strategy, MaskingStrategy)
    ]
