# ==========================================
# BOUNDLESS AI
# MODIFICATION HANDLER v1
# HANDLE "اینو به چهارچوبت اضافه کن" COMMAND
# ==========================================

import re
import json
from datetime import datetime


class ModificationHandler:

    def __init__(self, memory=None, eternal=None, rule_engine=None):

        self.memory = memory
        self.eternal = eternal
        self.rule_engine = rule_engine
        self.modifications = []
        self.history = []

    # ======================================
    # DETECT
    # ======================================

    def detect(self, text):

        """
        تشخیص دستور اضافه کردن به چهارچوب
        """

        text = str(text).strip()

        # الگوی دقیق
        patterns = [
            r"اینو به چهارچوبت اضافه کن",
            r"اینو به چهارچوب اضافه کن",
            r"به چهارچوبت اضافه کن",
            r"اضافه کن به چهارچوب"
        ]

        for pattern in patterns:
            if re.search(pattern, text):
                return True

        # همچنین تشخیص با ":" یا "=>"
        if ":" in text and "چهارچوب" in text:
            return True

        if "=>" in text and "چهارچوب" in text:
            return True

        return False

    # ======================================
    # EXTRACT
    # ======================================

    def extract(self, text):

        """
        استخراج محتوای جدید برای اضافه کردن به چهارچوب
        """

        text = str(text).strip()

        # روش ۱: بعد از ":" یا "=>"
        for separator in [":", "=>", "→"]:
            if separator in text:
                parts = text.split(separator, 1)
                if len(parts) > 1:
                    return parts[1].strip()

        # روش ۲: بعد از "اضافه کن"
        if "اضافه کن" in text:
            parts = text.split("اضافه کن", 1)
            if len(parts) > 1:
                return parts[1].strip()

        # روش ۳: خود متن کامل (به جز دستور)
        for phrase in ["اینو به چهارچوبت اضافه کن", "به چهارچوبت اضافه کن"]:
            if phrase in text:
                return text.replace(phrase, "").strip()

        return text

    # ======================================
    # ADD TO FRAMEWORK
    # ======================================

    def add_to_framework(self, text, source="USER"):

        """
        اضافه کردن محتوای جدید به چهارچوب
        """

        result = {
            "original": text,
            "extracted": None,
            "added_to": [],
            "success": False,
            "message": "",
            "timestamp": str(datetime.now())
        }

        # ===============================
        # 1. تشخیص و استخراج
        # ===============================

        if not self.detect(text):
            result["message"] = "❌ دستور شناسایی نشد."
            return result

        content = self.extract(text)
        if not content:
            result["message"] = "❌ محتوایی برای اضافه کردن یافت نشد."
            return result

        result["extracted"] = content

        # ===============================
        # 2. تحلیل محتوا
        # ===============================

        # آیا یک قانون جدید است؟
        if "قانون" in content or "rule" in content.lower():
            if self.rule_engine:
                rule_result = self.rule_engine.add_rule(content)
                if rule_result.get("success"):
                    result["added_to"].append("rule_engine")
                    result["success"] = True

        # آیا یک درس جدید است؟
        if "درس" in content or "lesson" in content.lower():
            if self.eternal:
                lesson_result = self.eternal.store_lesson(content, "modification")
                if lesson_result.get("success"):
                    result["added_to"].append("eternal_file")
                    result["success"] = True

        # آیا یک الگوی جدید است؟
        if "الگو" in content or "pattern" in content.lower():
            if self.eternal:
                pattern_result = self.eternal.store_pattern(content, "modification")
                if pattern_result.get("success"):
                    result["added_to"].append("eternal_file")
                    result["success"] = True

        # ===============================
        # 3. ذخیره در تاریخچه
        # ===============================

        self.modifications.append(result)
        self.history.append({
            "content": content,
            "timestamp": str(datetime.now()),
            "source": source
        })

        # ===============================
        # 4. پیام نهایی
        # ===============================

        if result["success"]:
            result["message"] = f"✅ محتوای جدید به چهارچوب اضافه شد: {', '.join(result['added_to'])}"
        else:
            result["message"] = "⚠️ محتوا شناسایی شد اما به بخش خاصی اضافه نشد. به عنوان یادداشت ذخیره شد."

            # ذخیره به عنوان یادداشت
            if self.eternal:
                self.eternal.store_lesson(
                    f"MODIFICATION: {content}",
                    "modification_note"
                )
                result["added_to"].append("eternal_file_note")
                result["success"] = True
                result["message"] = "✅ محتوا به عنوان یادداشت در Eternal-File ذخیره شد."

        return result

    # ======================================
    # GET HISTORY
    # ======================================

    def get_history(self, limit=10):

        return self.history[-limit:]

    # ======================================
    # GET STATS
    # ======================================

    def get_stats(self):

        total = len(self.history)
        successful = sum(1 for m in self.modifications if m.get("success", False))

        return {
            "total_modifications": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": round(successful / total * 100, 2) if total > 0 else 0
        }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    handler = ModificationHandler()

    print("=" * 50)
    print("MODIFICATION HANDLER TEST")
    print("=" * 50)

    # تست ۱: تشخیص
    print("\n📌 تست ۱: تشخیص دستور")
    text = "اینو به چهارچوبت اضافه کن: قانون جدید: همیشه از حافظه Σ استفاده کن"
    print(f"تشخیص: {handler.detect(text)}")

    # تست ۲: استخراج
    print("\n📌 تست ۲: استخراج محتوا")
    content = handler.extract(text)
    print(f"محتوا: {content}")

    # تست ۳: اضافه کردن
    print("\n📌 تست ۳: اضافه کردن به چهارچوب")
    result = handler.add_to_framework(text)
    print(result["message"])
    print(f"اضافه شده به: {result['added_to']}")

    # تست ۴: دستور بدون محتوا
    print("\n📌 تست ۴: دستور بدون محتوا")
    result = handler.add_to_framework("اینو به چهارچوبت اضافه کن")
    print(result["message"])

    # تست ۵: تاریخچه
    print("\n📌 تست ۵: تاریخچه")
    history = handler.get_history(3)
    for item in history:
        print(f"- {item['content'][:50]}...")

    # آمار
    print("\n📌 آمار:")
    stats = handler.get_stats()
    print(f"- کل تغییرات: {stats['total_modifications']}")
    print(f"- موفق: {stats['successful']}")
    print(f"- نرخ موفقیت: {stats['success_rate']}%")