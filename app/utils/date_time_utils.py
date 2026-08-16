from datetime import datetime, timezone

def get_current_utc_time() -> datetime:
    """
    Returns the current UTC time as a datetime object.
    """
    return datetime.now(timezone.utc)