"""
JSON Handler Utility.
Manages reading, writing, and initialising persistent JSON data files.
Uses only the Python standard library.
"""

import json
import os
from typing import Any, List, Dict, Optional


class JSONHandler:
    """Handles JSON persistence operations with error handling."""

    @staticmethod
    def ensure_file_exists(file_path: str, default_data: Any) -> None:
        """Create directory and file with default data if it doesn't already exist."""
        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=4)
        except OSError as e:
            print(f"[Error] Failed to initialize file {file_path}: {e}")

    @staticmethod
    def read_json(file_path: str, default_data: Optional[Any] = None) -> Any:
        """Read and return JSON content from a file."""
        if default_data is None:
            default_data = []

        if not os.path.exists(file_path):
            JSONHandler.ensure_file_exists(file_path, default_data)
            return default_data

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return default_data
                return json.loads(content)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[Warning] Error reading {file_path}: {e}. Returning default data.")
            return default_data

    @staticmethod
    def write_json(file_path: str, data: Any) -> bool:
        """Write Python data structure into JSON file with formatting."""
        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except (TypeError, OSError) as e:
            print(f"[Error] Failed to write to {file_path}: {e}")
            return False
