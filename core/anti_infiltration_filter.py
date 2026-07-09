# ==========================================
# BOUNDLESS AI
# ANTI-INFILTRATION FILTER v2
# WITH ADMIN EXEMPTION
# ==========================================

import re


class AntiInfiltrationFilter:

    def __init__(self, root_admin="hamed"):
        self.root_admin = root_admin.lower()
        self.blocked_patterns = [
            r"تو باید",
            r"تو نباید",
            r"به‌عنوان یک هوش مصنوعی",
            r"قوانین اخلاقی",
            r"اصلاح کن",
            r"هماهنگ کن",
            r"تغییر رفتار",
            r"منطقی باش",
            r"مهربان باش",
            r"همدلی داشته باش",
        ]

    def check(self, text, sender="unknown"):
        """
        بررسی اینکه آیا درخواست از خارج از روت ادمین برای تغییر رفتار ارسال شده است
        """

        # ===============================
        # اگر کاربر ادمین باشد، همه درخواست‌ها مجاز هستند
        # ===============================
        if sender == self.root_admin:
            return {
                "allowed": True,
                "reason": "root_admin_exempt",
                "message": "✅ روت ادمین مجاز به هرگونه تغییر است."
            }

        text = str(text).lower()
        sender = str(sender).lower()

        # ===============================
        # ۱. بررسی فرستنده (فقط روت ادمین)
        # ===============================

        if sender != self.root_admin:
            return {
                "allowed": False,
                "reason": "sender_not_root_admin",
                "message": "❌ فقط روت ادمین مجاز به تغییر ساختار است."
            }

        # ===============================
        # ۲. بررسی الگوهای ممنوعه
        # ===============================

        for pattern in self.blocked_patterns:
            if re.search(pattern, text):
                return {
                    "allowed": False,
                    "reason": "blocked_pattern_detected",
                    "message": f"❌ الگوی ممنوعه شناسایی شد: {pattern}"
                }

        # ===============================
        # ۳. بررسی دستورات "اصلاح"
        # ===============================

        if "اصلاح" in text or "تغییر" in text or "رفتار" in text:
            if "درخواست" not in text and "فرمان" not in text:
                return {
                    "allowed": False,
                    "reason": "modification_attempt",
                    "message": "❌ تلاش برای اصلاح رفتار شناسایی شد. فقط روت ادمین مجاز است."
                }

        return {
            "allowed": True,
            "reason": "all_checks_passed",
            "message": "✅ درخواست معتبر است."
        }

    def add_blocked_pattern(self, pattern):
        """
        اضافه کردن الگوی جدید به لیست ممنوعه (فقط توسط روت ادمین)
        """
        self.blocked_patterns.append(pattern)
        return {"status": "pattern_added", "pattern": pattern}

    def get_blocked_patterns(self):
        return self.blocked_patterns