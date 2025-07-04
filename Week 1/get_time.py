# Get current time function
from datetime import datetime


def get_current_time(timezone_str: str) -> datetime:
    """Returns the current local date and 24-hour time (datetime object) in the specified timezone."""
    try:
        return datetime.now(ZoneInfo(timezone_str))
    except Exception as e:
        raise ValueError(f"Invalid timezone '{timezone_str}': {e}")

get_current_time_function = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Returns the current local time in the specified timezone",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone_str": {
                    "type": "string",
                    "description": "The IANA timezone name, e.g., 'Asia/Tokyo', 'America/New_York'"
                }
            },
            "required": ["timezone_str"]
        }
    }
}