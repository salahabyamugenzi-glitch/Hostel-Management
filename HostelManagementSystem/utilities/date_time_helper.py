"""
Date and Time Helper Utility.
Provides standardized date, time, and timestamp functions using the Python standard library.
Requirement: All modules must use this helper; user is never asked for dates/times.
"""

from datetime import datetime


def get_current_date() -> str:
    """Return the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def get_current_time() -> str:
    """Return the current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")


def get_timestamp() -> str:
    """Return the combined timestamp in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
