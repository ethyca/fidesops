import os
from typing import Optional, List
from itertools import repeat, chain
import logging
import json
from multiprocessing import Pool
import requests


from fidesops.schemas.masking.masking_configuration import (
    MaskingConfiguration,
)
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
    MaskingStrategyConfigurationDescription,
)
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy


logger = logging.getLogger(__name__)

NLP = "nlp"


class NLPMaskingConfiguration(MaskingConfiguration):
    """Configuration for NLPMaskingStrategy"""

    language: str = "English"
    batch_size: int = 16
    parallelism: int = 4
    svc_url: str = os.environ["NLP_SVC_URL"]
    api_key: str = os.environ["NLP_SVC_API_KEY"]


class NLPMaskingStrategy(MaskingStrategy):
    """Masks a value by invoking an NLP deidentification service"""

    def __init__(self, configuration: NLPMaskingConfiguration):
        self.language = configuration.language
        self.batch_size = configuration.batch_size
        self.parallelism = configuration.parallelism
        self.svc_url = configuration.svc_url
        self.api_key = configuration.api_key

    @staticmethod
    def strategy_name() -> str:
        return NLP

    def mask(
        self, values: Optional[List[str]], request_id: Optional[str]
    ) -> Optional[List[str]]:
        """Returns the deidentified version of the provided values. Returns None if the provided value
        is None"""
        if values is None:
            return None
        batches = NLPMaskingStrategy.make_batches(values, self.batch_size)
        responses = list()
        with Pool(processes=self.parallelism) as pool:
            responses = pool.starmap(
                NLPMaskingStrategy.de_identify_text,
                zip(batches, repeat(self.svc_url), repeat(self.api_key)),
            )

        return list(chain.from_iterable(responses))

    @staticmethod
    def de_identify_text(texts: List[str], url: str, api_key: str) -> List[str]:
        endpoint = url
        body = {"text": texts, "key": api_key}
        response = requests.post(endpoint, json=body, verify=False)
        if not response.ok:
            message = f"Received errored response with status {response.status_code} from deidentification service."
            logger.error(message)
            logger.debug(f"Errored response body: {response.content}")
            raise ValueError(message)
        return NLPMaskingStrategy.parse_response(response.text)

    @staticmethod
    def parse_response(response_str: str) -> List[str]:
        # TODO: pick up and log masking stats on response body
        cleaned = list()
        response_body = json.loads(response_str)
        for record in response_body:  # each response is an array of records
            cleaned.append(
                record["result"]
            )  # within each record, 'result' field is cleaned text
        return cleaned

    @staticmethod
    def make_batches(texts: List[str], batch_size: int) -> List[str]:
        num_batches = int(len(texts) / batch_size)
        batches = [texts[i : i + batch_size] for i in range(num_batches)]
        remainder = len(texts) % batch_size
        if remainder:
            batches.append(texts[-remainder:])
        return batches

    @staticmethod
    def get_configuration_model() -> MaskingConfiguration:
        return NLPMaskingConfiguration

    # MR Note - We will need a way to ensure that this does not fall out of date. Given that it
    # includes subjective instructions, this is not straightforward to automate
    @staticmethod
    def get_description() -> MaskingStrategyDescription:
        return MaskingStrategyDescription(
            name=NLP,
            description="Masks the input text value by using an external NLP deidentification service",
            configurations=[
                MaskingStrategyConfigurationDescription(
                    key="language",
                    description="Specifies the language of the input text.",
                ),
                MaskingStrategyConfigurationDescription(
                    key="batch_size",
                    description="Size of batches (number of text fields) to send per call to the NLP service",
                ),
                MaskingStrategyConfigurationDescription(
                    key="parallelism",
                    description="How many parallel calls to make to the NLP service",
                ),
                MaskingStrategyConfigurationDescription(
                    key="svc_url",
                    description="The NLP service URL to use for text deidentification",
                ),
            ],
        )

    @staticmethod
    def data_type_supported(data_type: Optional[str]) -> bool:
        """Determines whether or not the given data type is supported by this masking strategy"""
        supported_data_types = {"string"}
        return data_type in supported_data_types

    def secrets_required(self) -> bool:
        return False
