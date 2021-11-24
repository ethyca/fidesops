"""Utility functions for test support"""
import threading
import time
from typing import Callable, Any

from sqlalchemy import and_

from fidesops.models.privacy_request import ExecutionLog


def wait_for(
    f: Callable[[Any], bool], timeout=10, period=0.25, *args, **kwargs
) -> bool:
    """Utility function to wait for the result of a callable to
    be true before proceeding."""

    def runner():
        must_end = time.time() + timeout
        while time.time() < must_end:
            print(f"invoke {f}:{f()}")
            if f(*args, **kwargs):
                time.sleep(0.5)
                return True
            time.sleep(period)
        return False

    t = threading.Thread(target=runner)
    t.start()
    t.join()


def wait_for_privacy_request(db, privacy_request_id: str) -> bool:

    print(f"Wait for privacy request {privacy_request_id}")

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
