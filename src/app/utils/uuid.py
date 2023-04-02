import json
from typing import Any
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> str:
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
