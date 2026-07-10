import os
import json
from kivy.app import App


class ConfigManager:
    """Simple JSON config stored in the app's user_data_dir.

    Usage:
        cfg = ConfigManager()
        cfg.set("groq_api_key", "...")
        cfg.get("groq_api_key")
    """

    def __init__(self, filename="config.json"):
        self.filename = filename
        try:
            app = App.get_running_app()
            base = app.user_data_dir if app else os.path.abspath(os.path.dirname(__file__))
        except Exception:
            base = os.path.abspath(os.path.dirname(__file__))
        # ensure directory exists
        try:
            os.makedirs(base, exist_ok=True)
        except Exception:
            pass
        self.path = os.path.join(base, self.filename)
        self._data = {}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            else:
                self._data = {}
        except Exception:
            self._data = {}

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("⚠️ Config save error:", e)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self._save()
