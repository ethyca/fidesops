import logging
import os
from typing import Any, Mapping, Union, Optional

MASKED = "MASKED"


class NotPii(str):
    """whitelist non pii data"""


def get_fides_log_record_factory() -> Any:
    """intercepts default LogRecord for custom handling of params"""

    def factory(  # pylint: disable=R0913
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: str,
        args: Union[tuple[Any, ...], Mapping[str, Any]],
        exc_info: Any,
        func: str = None,
        sinfo: str = None,
    ) -> logging.LogRecord:
        env_log_pii: bool = os.getenv("LOG_PII") == "True"
        if not env_log_pii:
            args: tuple[Any, ...] = tuple(_mask_pii_for_logs(arg) for arg in args)
        return logging.LogRecord(
            name=name,
            level=level,
            pathname=fn,
            lineno=lno,
            msg=msg,
            args=args,
            exc_info=exc_info,
            func=func,
            sinfo=sinfo,
        )

    return factory


def _mask_pii_for_logs(pii_text: Any) -> Any:
    """
    :param pii_text: param that contains possible pii
    :return: depending on ENV config, returns masked pii param
    """
    if isinstance(pii_text, NotPii):
        return pii_text
    return MASKED
