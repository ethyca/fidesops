import json
from typing import Any


def get_json(obj: Any) -> Any:
    return json.loads(json.dumps(obj, default=lambda o: getattr(o, "__dict__", str(o))))
