"""
ColorManager - Loads and saves UI color preferences from JSON config.
"""

import json
import os
import sys

_REPO_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")
_DEFAULTS_FILE = os.path.join(_REPO_CONFIG_DIR, "defaults.json")


def _user_settings_path() -> str:
    """Return the OS-appropriate user-local path for settings.json."""
    app_name = "dm-lawncare"
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return os.path.join(base, app_name, "settings.json")


_SETTINGS_FILE = _user_settings_path()


class ColorManager:
    """Manages UI color settings with JSON persistence."""

    def __init__(self):
        self._defaults = self._load_json(_DEFAULTS_FILE)
        self._settings = self._load_json(_SETTINGS_FILE)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: str) -> str:
        """Return the current color value for *key*, falling back to the default."""
        return self._settings.get(key, self._defaults.get(key, "#000000"))

    def set(self, key: str, value: str) -> None:
        """Update *key* to *value* and persist to settings.json."""
        self._settings[key] = value
        self._save()

    def reset_to_defaults(self) -> None:
        """Restore all colors to factory defaults and persist."""
        self._settings = dict(self._defaults)
        self._save()

    def all_keys(self) -> list:
        """Return all color key names."""
        return list(self._defaults.keys())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_json(path: str) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return {}

    def _save(self) -> None:
        os.makedirs(os.path.dirname(_SETTINGS_FILE), exist_ok=True)
        with open(_SETTINGS_FILE, "w", encoding="utf-8") as fh:
            json.dump(self._settings, fh, indent=4)
