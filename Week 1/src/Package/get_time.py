# Get current time function
from datetime import datetime
from zoneinfo import ZoneInfo
from rich.console import Console
import asyncio

console = Console()

async def get_current_time(timezone_str: str) -> datetime:
    """
    Returns the current local date and 24-hour time (datetime object) in the specified timezone.
    
    Args:
        timezone_str: The IANA timezone name, e.g., 'Asia/Tokyo', 'America/New_York'

    Returns:
        The current local date and 24-hour time in the specified timezone as a datetime object
    """
    try:
        return datetime.now(ZoneInfo(timezone_str))
    except Exception as e:
        error_msg = f"Invalid timezone '{timezone_str}': {e}. "
        error_msg += "Please use a valid IANA timezone name like 'Asia/Tokyo', 'America/New_York', 'Europe/London', or 'UTC'."
        console.print(f"[italic red](System Message) {error_msg}[/italic red]")
        raise ValueError(error_msg)

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