"""Utility functions for test support"""
import threading
import time
from typing import Callable, Any
import logging
from sqlalchemy import and_

from fidesops.models.privacy_request import ExecutionLog

logger = logging.getLogger(__name__)


def wait_for(f: Callable[[Any], bool], timeout=3, period=0.25, *args, **kwargs) -> bool:
    """Utility function to wait for the result of a callable to
    be true before proceeding."""

    def runner():
        must_end = time.time() + timeout
        while time.time() < must_end:
            print(f"invoke {f}")
            try:
                if f(*args, **kwargs):
                    time.sleep(0.25)
                    return True
                time.sleep(period)
            except Exception as e:
                print(e)
        return False

    t = threading.Thread(target=runner)
    t.start()
    t.join()


def wait_for_privacy_request(db, privacy_request_id: str) -> bool:
    """Wait until there exists an execution log record for the given privacy
    request id whose status is either 'complete' or 'error'"""
    logger.info(f"Waiting for privacy request {privacy_request_id}")

    def f():
        x = (
            db.query(ExecutionLog)
            .filter(
                and_(
                    ExecutionLog.privacy_request_id == privacy_request_id,
                    ExecutionLog.status.in_(("complete", "error")),
                )
            )
            .first()
        )
        return x is not None

    return wait_for(f)
