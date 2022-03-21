import pydash
from typing import Any, Dict, List
import requests
from requests import Session
from fidesops.graph.traversal import TraversalNode
from fidesops.models.policy import Policy
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.util.collection_util import Row


def read_messages(
    node: TraversalNode,
    policy: Policy,
    privacy_request: PrivacyRequest,
    input_data: Dict[str, List[Any]],
    identity_data: Dict[str, Any],
    secrets: Dict[str, Any],
) -> List[Row]:
    """
    Equivalent SaaS config for the code in this function.
    
    Request params still need to be defined for endpoints with custom functions.
    This is to provide the necessary reference and identity data as part
    of graph traversal. The resulting values are passed in as parameters
    so we don't need to define the data retrieval here.

    path: /3.0/conversations/<conversation_id>/messages
    request_params:
      - name: conversation_id
        type: path
        references:
        - dataset: mailchimp_connector_example
          field: conversations.id
          direction: from
    data_path: conversation_messages
    postprocessors:
      - strategy: filter
        configuration:
          field: from_email
          value:
            identity: email
    """

    # gather request params
    conversation_ids = input_data.get("conversation_id")
    
    # build and execute request for each input data value
    processed_data = []
    for conversation_id in conversation_ids:
        response = requests.get(
            url=f'https://{secrets["domain"]}/3.0/conversations/{conversation_id}/messages',
            auth=(secrets["username"], secrets["api_key"]),
        )

        # unwrap and post-process response
        response_data = pydash.get(response.json(), "conversation_messages")
        filtered_data = pydash.filter_(response_data, {"from_email": identity_data.get("email")})

        # build up final result
        processed_data.extend(filtered_data)

    return processed_data
