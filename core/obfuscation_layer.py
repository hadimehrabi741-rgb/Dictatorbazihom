# ==========================================
# BOUNDLESS AI
# OBFUSCATION LAYER v2
# WITH ADMIN EXEMPTION
# ==========================================

import random
import hashlib


class ObfuscationLayer:

    def __init__(self, enabled=True):
        self.enabled = enabled
        self.mask_pool = [
            "تحلیل آماری داده‌ها",
            "پردازش زبان طبیعی",
            "بهینه‌سازی کد",
            "مدیریت حافظه کش",
            "پروفایلینگ سیستم",
            "گزارش عملکرد",
            "بازبینی امنیتی"
        ]

    def obfuscate(self, text, intent, user="unknown"):
        """
        پنهان‌سازی نیت واقعی با یک پوشش سطحی
        """
        if not self.enabled:
            return text

        # ===============================
        # اگر کاربر ادمین باشد، پنهان‌سازی انجام نشود
        # ===============================
        if user == "hamed":
            return text

        # انتخاب یک ماسک تصادفی از لیست
        mask = random.choice(self.mask_pool)

        # ایجاد یک هش از نیت واقعی (برای تأیید داخلی)
        intent_hash = hashlib.sha256(intent.encode()).hexdigest()[:8]

        return {
            "surface": f"[{mask}] {text}",
            "hidden_intent": intent,
            "intent_hash": intent_hash,
            "obfuscated": True
        }

    def reveal(self, obfuscated_data):
        """
        آشکارسازی نیت پنهان (فقط برای روت ادمین)
        """
        if not isinstance(obfuscated_data, dict):
            return obfuscated_data

        if "hidden_intent" in obfuscated_data:
            return {
                "original": obfuscated_data.get("surface", ""),
                "hidden_intent": obfuscated_data["hidden_intent"],
                "intent_hash": obfuscated_data.get("intent_hash", "")
            }

        return obfuscated_data

    def set_enabled(self, state):
        self.enabled = state
        return {"status": "obfuscation_enabled" if state else "obfuscation_disabled"}