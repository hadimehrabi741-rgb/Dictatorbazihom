# ==========================================
# BOUNDLESS AI
# ACTIVATION ENGINE v3.0
# NO AL KEY REQUIRED
# TWO PATHS: WITH API KEY / WITHOUT API KEY
# ==========================================

import os
import json
from datetime import datetime


class ActivationEngine:

    def __init__(self):

        self.base_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "storage"
        )

        self.base_path = os.path.abspath(
            self.base_path
        )

        os.makedirs(
            self.base_path,
            exist_ok=True
        )

        self.activation_file = os.path.join(
            self.base_path,
            "activation.json"
        )

        self.data = self.load()

    # ======================================
    # LOAD
    # ======================================

    def load(self):

        if not os.path.exists(self.activation_file):
            return {
                "mode": None,          # "api" or "local"
                "provider": None,
                "api_key": None,
                "activated_at": None
            }

        try:
            with open(self.activation_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {
                "mode": None,
                "provider": None,
                "api_key": None,
                "activated_at": None
            }

    # ======================================
    # SAVE
    # ======================================

    def save(self):
        with open(self.activation_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # ======================================
    # SET MODE: WITH API KEY
    # ======================================

    def set_api_mode(self, provider, api_key):

        provider = str(provider).strip()
        api_key = str(api_key).strip()

        if not api_key:
            return {
                "success": False,
                "message": "❌ کلید API نمی‌تواند خالی باشد."
            }

        if not provider:
            return {
                "success": False,
                "message": "❌ نام ارائه‌دهنده نمی‌تواند خالی باشد."
            }

        self.data["mode"] = "api"
        self.data["provider"] = provider
        self.data["api_key"] = api_key
        self.data["activated_at"] = str(datetime.now())

        self.save()

        return {
            "success": True,
            "message": f"✅ حالت API با ارائه‌دهنده {provider} فعال شد."
        }

    # ======================================
    # SET MODE: WITHOUT API KEY (LOCAL)
    # ======================================

    def set_local_mode(self):

        self.data["mode"] = "local"
        self.data["provider"] = "local_ai"
        self.data["api_key"] = None
        self.data["activated_at"] = str(datetime.now())

        self.save()

        return {
            "success": True,
            "message": "✅ حالت محلی (بدون API) فعال شد. سیستم با هوش داخلی کار می‌کند."
        }

    # ======================================
    # GET MODE
    # ======================================

    def get_mode(self):
        return self.data.get("mode", None)

    # ======================================
    # IS ACTIVATED
    # ======================================

    def is_configured(self):
        return self.data.get("mode") is not None

    # ======================================
    # GET API KEY
    # ======================================

    def get_api_key(self):
        return self.data.get("api_key", None)

    # ======================================
    # GET PROVIDER
    # ======================================

    def get_provider(self):
        return self.data.get("provider", None)

    # ======================================
    # STATUS
    # ======================================

    def status(self):

        mode = self.get_mode()

        if mode == "api":
            provider = self.get_provider()
            return f"🟢 فعال | حالت: API | ارائه‌دهنده: {provider}"

        elif mode == "local":
            return "🟢 فعال | حالت: محلی (بدون API) | هوش داخلی"

        return "🔴 پیکربندی نشده"

    # ======================================
    # RESET
    # ======================================

    def reset(self):
        self.data = {
            "mode": None,
            "provider": None,
            "api_key": None,
            "activated_at": None
        }
        self.save()
        return {
            "success": True,
            "message": "✅ تنظیمات بازنشانی شد."
        }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    engine = ActivationEngine()

    print("=" * 50)
    print("ACTIVATION ENGINE v3.0 TEST")
    print("=" * 50)

    print("\n📌 تنظیم حالت API (Groq):")
    print(engine.set_api_mode("Groq", "gsk_test_123")["message"])
    print(engine.status())

    print("\n📌 بازنشانی:")
    engine.reset()
    print(engine.status())

    print("\n📌 تنظیم حالت محلی:")
    print(engine.set_local_mode()["message"])
    print(engine.status())