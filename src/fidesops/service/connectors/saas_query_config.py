from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, TypeVar

import pydash

from fidesops.common_exceptions import FidesopsException
from fidesops.core.config import config
from fidesops.graph.config import ScalarField
from fidesops.graph.traversal import TraversalNode
from fidesops.models.policy import Policy
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.schemas.saas.saas_config import Endpoint, SaaSRequest
from fidesops.schemas.saas.shared_schemas import SaaSRequestParams
from fidesops.service.connectors.query_config import QueryConfig
from fidesops.util import saas_util
from fidesops.util.collection_util import Row, merge_dicts
from fidesops.util.saas_util import FIDESOPS_GROUPED_INPUTS, unflatten_dict

logger = logging.getLogger(__name__)

T = TypeVar("T")


class SaaSQueryConfig(QueryConfig[SaaSRequestParams]):
    """Query config that generates populated SaaS requests for a given collection"""

    def __init__(
        self,
        node: TraversalNode,
        endpoints: Dict[str, Endpoint],
        secrets: Dict[str, Any],
        data_protection_request: Optional[SaaSRequest] = None,
        privacy_request: Optional[PrivacyRequest] = None,
    ):
        super().__init__(node)
        self.collection_name = node.address.collection
        self.endpoints = endpoints
        self.secrets = secrets
        self.data_protection_request = data_protection_request
        self.privacy_request = privacy_request
        self.action: Optional[str] = None

    def get_request_by_action(self, action: str) -> Optional[SaaSRequest]:
        """
        Returns the appropriate request config based on the
        current collection and preferred action (read, update, delete)
        """
        try:
            # store action name for logging purposes
            self.action = action
            collection_name = self.node.address.collection
            request = self.endpoints[collection_name].requests[action]  # type: ignore
            logger.info(
                f"Found matching endpoint to {action} '{collection_name}' collection"
            )
            return request
        except KeyError:
            logger.info(
                f"The '{action}' action is not defined for the '{collection_name}' endpoint in {self.node.node.dataset.connection_key}"
            )
            return None

    def get_masking_request(self) -> Optional[SaaSRequest]:
        """Returns a tuple of the preferred action and SaaSRequest to use for masking.
        An update request is preferred, but we can use a gdpr delete endpoint or delete endpoint if not MASKING_STRICT.
        """

        update: Optional[SaaSRequest] = self.get_request_by_action("update")
        gdpr_delete: Optional[SaaSRequest] = None
        delete: Optional[SaaSRequest] = None

        if not config.execution.masking_strict:
            gdpr_delete = self.data_protection_request
            delete = self.get_request_by_action("delete")

        try:
            # Return first viable option
            action_type: str = next(
                action
                for action in [
                    "update" if update else None,
                    "data_protection_request" if gdpr_delete else None,
                    "delete" if delete else None,
                ]
                if action
            )

            # store action name for logging purposes
            self.action = action_type

            logger.info(
                f"Selecting '{action_type}' action to perform masking request for '{self.collection_name}' collection."
            )
            return next(request for request in [update, gdpr_delete, delete] if request)
        except StopIteration:
            return None

    def generate_requests(
        self, input_data: Dict[str, List[Any]], policy: Optional[Policy]
    ) -> List[SaaSRequestParams]:
        """Takes the input_data and uses it to generate a list of SaaS request params"""

        filtered_data = self.node.typed_filtered_values(input_data)

        request_params = []

        # Build SaaS requests for fields that are independent of each other
        for string_path, reference_values in filtered_data.items():
            for value in reference_values:
                request_params.append(
                    self.generate_query({string_path: [value]}, policy)
                )

        # Build SaaS requests for fields that are dependent on each other
        grouped_input_data: List[Dict[str, Any]] = input_data.get(
            FIDESOPS_GROUPED_INPUTS, []
        )
        for dependent_data in grouped_input_data:
            request_params.append(self.generate_query(dependent_data, policy))

        return request_params

    def generate_query(
        self, input_data: Dict[str, List[Any]], policy: Optional[Policy]
    ) -> SaaSRequestParams:
        """
        This returns the method, path, header, query, and body params needed to make an API call.
        This is the API equivalent of building the components of a database
        query statement (select statement, where clause, limit, offset, etc.)
        """

        current_request: SaaSRequest | None = self.get_request_by_action("read")
        if not current_request:
            raise FidesopsException(
                f"The 'read' action is not defined for the '{self.collection_name}' "
                f"endpoint in {self.node.node.dataset.connection_key}"
            )

        # create the source of param values to populate the various placeholders
        # in the path, headers, query_params, and body
        param_values: Dict[str, Any] = {}
        for param_value in current_request.param_values or []:
            if param_value.references or param_value.identity:
                # TODO: how to handle missing reference or identity values in a way
                # in a way that is obvious based on configuration
                input_list = input_data.get(param_value.name)
                if input_list:
                    param_values[param_value.name] = input_list[0]
            elif param_value.connector_param:
                param_values[param_value.name] = pydash.get(
                    self.secrets, param_value.connector_param
                )

        if self.privacy_request:
            param_values["privacy_request_id"] = self.privacy_request.id

        # map param values to placeholders in path, headers, and query params
        saas_request_params: SaaSRequestParams = saas_util.map_param_values(
            self.action, self.collection_name, current_request, param_values  # type: ignore
        )

        logger.info(f"Populated request params for {current_request.path}")

        return saas_request_params

    def generate_update_stmt(  # pylint: disable=R0914
        self, row: Row, policy: Policy, request: PrivacyRequest
    ) -> SaaSRequestParams:
        """
        This returns the method, path, header, query, and body params needed to make an API call.
        The fields in the row are masked according to the policy and added to the request body
        if specified by the body field of the masking request.
        """

        current_request: SaaSRequest = self.get_masking_request()  # type: ignore
        collection_name: str = self.node.address.collection
        collection_values: Dict[str, Row] = {collection_name: row}
        identity_data: Dict[str, Any] = request.get_cached_identity_data()

        # create the source of param values to populate the various placeholders
        # in the path, headers, query_params, and body
        param_values: Dict[str, Any] = {}
        for param_value in current_request.param_values or []:
            if param_value.references:
                param_values[param_value.name] = pydash.get(
                    collection_values, param_value.references[0].field
                )
            elif param_value.identity:
                param_values[param_value.name] = pydash.get(
                    identity_data, param_value.identity
                )
            elif param_value.connector_param:
                param_values[param_value.name] = pydash.get(
                    self.secrets, param_value.connector_param
                )

        if self.privacy_request:
            param_values["privacy_request_id"] = self.privacy_request.id

        # remove any row values for fields marked as read-only, these will be omitted from all update maps
        for field_path, field in self.field_map().items():
            if field.read_only:
                pydash.unset(row, field_path.string_path)

        # mask row values
        update_value_map: Dict[str, Any] = self.update_value_map(row, policy, request)
        masked_object: Dict[str, Any] = unflatten_dict(update_value_map)

        # map of all values including those not being masked/updated
        all_value_map: Dict[str, Any] = self.all_value_map(row)
        # both maps use field paths for the keys so we can merge them before unflattening
        # values in update_value_map will override values in all_value_map
        complete_object: Dict[str, Any] = unflatten_dict(
            merge_dicts(all_value_map, update_value_map)
        )

        # removes outer {} wrapper from body for greater flexibility in custom body config
        param_values["masked_object_fields"] = json.dumps(masked_object)[1:-1]
        param_values["all_object_fields"] = json.dumps(complete_object)[1:-1]

        # map param values to placeholders in path, headers, and query params
        saas_request_params: SaaSRequestParams = saas_util.map_param_values(
            self.action, self.collection_name, current_request, param_values  # type: ignore
        )

        logger.info(f"Populated request params for {current_request.path}")

        return saas_request_params

    def all_value_map(self, row: Row) -> Dict[str, Any]:
        """
        Takes a row and preserves only the fields that are defined in the Dataset.
        Used for scenarios when an update endpoint has required fields other than
        just the fields being updated.
        """
        all_value_map: Dict[str, Any] = {}
        for field_path, field in self.field_map().items():
            # only map scalar fields
            if (
                isinstance(field, ScalarField)
                and pydash.get(row, field_path.string_path) is not None
            ):
                all_value_map[field_path.string_path] = pydash.get(
                    row, field_path.string_path
                )
        return all_value_map

    def query_to_str(self, t: T, input_data: Dict[str, List[Any]]) -> str:
        """Convert query to string"""
        return "Not yet supported for SaaSQueryConfig"

    def dry_run_query(self) -> Optional[str]:
        """dry run query for display"""
        return None
