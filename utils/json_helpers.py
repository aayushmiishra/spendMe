import json
from typing import Any

def parse_json_safely(data: str, default_value: Any = None) -> Any:
    """Safely parse JSON data with error handling"""
    try:
        return json.loads(data) if isinstance(data, str) else data
    except json.JSONDecodeError:
        return default_value