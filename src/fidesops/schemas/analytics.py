from typing import Optional, List, Dict

from fidesops.schemas.base_class import BaseSchema


class FideslogAnalyticsEvent(BaseSchema):
    """
    Define a new analytics event to send to the fideslog server.
    event: The name/type of this event.
    command: For events submitted as a result of running CLI commands, the name of the command that was submitted. May include the subcommand name(s).
    endpoint: For events submitted as a result of making API server requests, the API endpoint path that was requested. If a fully-qualified URL is provided, only the URL path will be persisted.
    error: For events submitted as a result of running CLI commands that exit with a non-0 status code, or events submitted as a result of API server requests that respond with a non-2xx status code, the error type, without specific error details.
    extra_data: Any additional key/value pairs that should be associated with this event.
    flags: For events submitted as a result of running CLI commands, the flags in use when the command was submitted. Omits flag values (when they exist) by persisting only the portion of each string in this list that come before `=` or `space` characters.
    resource_counts: Should contain the counts of dataset, policy, and system manifests in use when this event was submitted. Include all three keys, even if one or more of their values are `0`. Ex: `{ "datasets": 7, "policies": 26, "systems": 9 }`.
    status_code: For events submitted as a result of making API server requests, the HTTP status code included in the response.
    """
    event: str
    command: Optional[str] = None
    endpoint: Optional[str] = None
    error: Optional[str] = None
    extra_data: Optional[Dict[str, str]] = None
    flags: Optional[List[str]] = None
    resource_counts: Optional[Dict[str, int]] = None
    status_code: Optional[int] = None
